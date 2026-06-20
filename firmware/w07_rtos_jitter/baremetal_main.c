// firmware/w07_rtos_jitter/baremetal_main.c
//
// Purpose:
//   Measure 10 ms periodic TX-event jitter on Raspberry Pi Pico without RTOS.
//   This is the bare-metal comparison target for W07.
//
// CSV schema:
//   mode,board,sample_index,period_target_us,timestamp_us,delta_us,jitter_us

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

#include "pico/stdlib.h"
#include "pico/time.h"

#define SAMPLE_COUNT 1000u
#define PERIOD_TARGET_US 10000u

// Match the FreeRTOS rx_task simulated workload. Tune only after real measurements.
#define RX_WORKLOAD_ITERS 20000u

static uint64_t timestamps_us[SAMPLE_COUNT];

static void simulated_rx_workload(void)
{
    volatile uint32_t dummy = 0;

    for (uint32_t i = 0; i < RX_WORKLOAD_ITERS; i++) {
        dummy += i;
        dummy ^= (dummy << 1);
    }

    (void)dummy;
}

static void output_csv(void)
{
    printf("mode,board,sample_index,period_target_us,timestamp_us,delta_us,jitter_us\r\n");

    for (uint32_t i = 0; i < SAMPLE_COUNT; i++) {
        int64_t delta_us = 0;
        int64_t jitter_us = 0;

        if (i > 0) {
            delta_us = (int64_t)(timestamps_us[i] - timestamps_us[i - 1]);
            jitter_us = delta_us - (int64_t)PERIOD_TARGET_US;
        }

        printf("baremetal,pico,%lu,%u,%llu,%lld,%lld\r\n",
               (unsigned long)(i + 1u),
               PERIOD_TARGET_US,
               (unsigned long long)timestamps_us[i],
               (long long)delta_us,
               (long long)jitter_us);
    }

    fflush(stdout);
}

int main(void)
{
    stdio_init_all();

    // Wait for USB CDC serial before measurement; this is outside the jitter window.
    sleep_ms(2000);

    uint32_t sample_index = 0;

    // Absolute schedule: delays do not accumulate into the next target.
    uint64_t target_time_us = time_us_64();

    while (sample_index < SAMPLE_COUNT) {
        const uint64_t now_us = time_us_64();

        if (now_us >= target_time_us) {
            timestamps_us[sample_index] = now_us;
            sample_index++;

            target_time_us += PERIOD_TARGET_US;
        }

        // Single-loop RX-like load can delay the next TX event check.
        simulated_rx_workload();
    }

    output_csv();

    while (true) {
        tight_loop_contents();
    }

    return 0;
}
