// firmware/w07_rtos_jitter/freertos_main.c
//
// Purpose:
//   Measure 10 ms periodic TX-event jitter on Raspberry Pi Pico using FreeRTOS.
//   TX task has highest priority.
//   RX task generates simulated receive workload.
//   STATE task receives TX events through a queue and prints CSV after capture.
//
// CSV schema:
//   mode,board,sample_index,period_target_us,timestamp_us,delta_us,jitter_us,
//   queue_latency_us,deadline_miss_count
//
// Notes:
//   - Do not print from tx_task during measurement.
//   - USB serial output is done only after SAMPLE_COUNT timestamps are captured.
//   - queue_latency_us is measured as:
//       state_task_receive_time_us - tx_task_queue_send_time_us

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

#include "pico/stdlib.h"
#include "pico/time.h"

#include "FreeRTOS.h"
#include "queue.h"
#include "semphr.h"
#include "task.h"

#define SAMPLE_COUNT 1000u
#define PERIOD_TARGET_US 10000u

#define TX_TASK_PRIORITY 3u
// Keep the queue consumer above the continuously ready simulated RX workload.
// taskYIELD() does not yield to lower-priority ready tasks.
#define STATE_TASK_PRIORITY 2u
#define RX_TASK_PRIORITY 1u

#define TX_TASK_STACK_WORDS 512u
#define RX_TASK_STACK_WORDS 512u
#define STATE_TASK_STACK_WORDS 1024u

#define TX_PERIOD_MS 10u
#define QUEUE_LENGTH 16u
#define QUEUE_TIMEOUT_MS 50u

// Adjust this to change simulated RX workload.
#define RX_WORKLOAD_ITERS 20000u

typedef struct {
    uint32_t sample_index;
    uint64_t timestamp_us;
    uint64_t queue_send_time_us;
} tx_event_t;

static uint64_t g_timestamps_us[SAMPLE_COUNT];
static int64_t g_delta_us[SAMPLE_COUNT];
static int64_t g_jitter_us[SAMPLE_COUNT];
static int64_t g_queue_latency_us[SAMPLE_COUNT];

static volatile uint32_t g_sample_count = 0;
static volatile uint32_t g_deadline_miss_count = 0;
static volatile bool g_capture_done = false;

static QueueHandle_t g_tx_event_queue = NULL;
static SemaphoreHandle_t g_capture_done_sem = NULL;

static void fatal_blink(void)
{
    const uint led_pin = PICO_DEFAULT_LED_PIN;
    gpio_init(led_pin);
    gpio_set_dir(led_pin, GPIO_OUT);

    while (true) {
        gpio_put(led_pin, 1);
        sleep_ms(100);
        gpio_put(led_pin, 0);
        sleep_ms(100);
    }
}

static void simulated_rx_workload(void)
{
    volatile uint32_t acc = 0;

    for (uint32_t i = 0; i < RX_WORKLOAD_ITERS; i++) {
        acc += i;
        acc ^= (acc << 1);
    }

    (void)acc;
}

static void tx_task(void *param)
{
    (void)param;

    TickType_t last_wake = xTaskGetTickCount();
    const TickType_t period_ticks = pdMS_TO_TICKS(TX_PERIOD_MS);

    for (uint32_t i = 0; i < SAMPLE_COUNT; i++) {
        const uint64_t now_us = time_us_64();

        g_timestamps_us[i] = now_us;
        g_sample_count = i + 1u;

        tx_event_t event = {
            .sample_index = i,
            .timestamp_us = now_us,
            .queue_send_time_us = time_us_64(),
        };

        // Do not block in the timing-critical task.
        BaseType_t sent = xQueueSend(g_tx_event_queue, &event, 0);
        if (sent != pdPASS) {
            g_queue_latency_us[i] = -1;
        }

        BaseType_t was_delayed = xTaskDelayUntil(&last_wake, period_ticks);
        if (was_delayed == pdFALSE) {
            g_deadline_miss_count++;
        }
    }

    g_capture_done = true;
    xSemaphoreGive(g_capture_done_sem);

    vTaskSuspend(NULL);
}

static void rx_task(void *param)
{
    (void)param;

    while (true) {
        if (g_capture_done) {
            vTaskSuspend(NULL);
        }

        simulated_rx_workload();
        taskYIELD();
    }
}

static void state_task(void *param)
{
    (void)param;

    tx_event_t event;
    uint32_t received_events = 0;

    while (received_events < SAMPLE_COUNT) {
        BaseType_t received = xQueueReceive(
            g_tx_event_queue,
            &event,
            pdMS_TO_TICKS(QUEUE_TIMEOUT_MS));

        if (received == pdPASS) {
            const uint64_t receive_time_us = time_us_64();

            if (event.sample_index < SAMPLE_COUNT &&
                g_queue_latency_us[event.sample_index] != -1) {
                g_queue_latency_us[event.sample_index] =
                    (int64_t)(receive_time_us - event.queue_send_time_us);
            }
            received_events++;
            continue;
        }

        if (g_capture_done) {
            break;
        }
    }

    xSemaphoreTake(g_capture_done_sem, portMAX_DELAY);

    g_delta_us[0] = 0;
    g_jitter_us[0] = 0;

    for (uint32_t i = 1; i < SAMPLE_COUNT; i++) {
        g_delta_us[i] = (int64_t)(g_timestamps_us[i] - g_timestamps_us[i - 1]);
        g_jitter_us[i] = g_delta_us[i] - (int64_t)PERIOD_TARGET_US;
    }

    // Wait for USB CDC serial after capture; this is outside the measurement window.
    vTaskDelay(pdMS_TO_TICKS(2000));

    printf("mode,board,sample_index,period_target_us,timestamp_us,delta_us,jitter_us,queue_latency_us,deadline_miss_count\r\n");

    for (uint32_t i = 0; i < SAMPLE_COUNT; i++) {
        printf("freertos,pico,%lu,%u,%llu,%lld,%lld,%lld,%lu\r\n",
               (unsigned long)(i + 1u),
               PERIOD_TARGET_US,
               (unsigned long long)g_timestamps_us[i],
               (long long)g_delta_us[i],
               (long long)g_jitter_us[i],
               (long long)g_queue_latency_us[i],
               (unsigned long)g_deadline_miss_count);
    }

    fflush(stdout);

    vTaskSuspend(NULL);
}

int main(void)
{
    stdio_init_all();

    for (uint32_t i = 0; i < SAMPLE_COUNT; i++) {
        g_queue_latency_us[i] = -2;
    }

    g_tx_event_queue = xQueueCreate(QUEUE_LENGTH, sizeof(tx_event_t));
    if (g_tx_event_queue == NULL) {
        fatal_blink();
    }

    g_capture_done_sem = xSemaphoreCreateBinary();
    if (g_capture_done_sem == NULL) {
        fatal_blink();
    }

    BaseType_t ok;

    ok = xTaskCreate(tx_task, "TX", TX_TASK_STACK_WORDS, NULL, TX_TASK_PRIORITY, NULL);
    if (ok != pdPASS) {
        fatal_blink();
    }

    ok = xTaskCreate(rx_task, "RX", RX_TASK_STACK_WORDS, NULL, RX_TASK_PRIORITY, NULL);
    if (ok != pdPASS) {
        fatal_blink();
    }

    ok = xTaskCreate(state_task, "STATE", STATE_TASK_STACK_WORDS, NULL, STATE_TASK_PRIORITY, NULL);
    if (ok != pdPASS) {
        fatal_blink();
    }

    vTaskStartScheduler();

    fatal_blink();

    return 0;
}
