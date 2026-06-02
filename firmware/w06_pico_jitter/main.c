#include <stdbool.h>
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>

#include "pico/stdlib.h"
#include "pico/time.h"

#define PERIOD_TARGET_US 10000u
#define SAMPLE_COUNT 1000u
#define STARTUP_SETTLE_MS 2000u

static const char *kEnvName = "pico";
static const char *kBoardName = "raspberry_pi_pico";

static repeating_timer_t capture_timer;
static volatile uint64_t captured_timestamps_us[SAMPLE_COUNT];
static volatile uint32_t captured_count = 0;
static volatile bool capture_complete = false;
static volatile bool capture_primed = false;
static volatile uint64_t reference_timestamp_us = 0;

static bool capture_timer_callback(repeating_timer_t *timer) {
    const uint64_t now_us = time_us_64();
    (void)timer;

    // IRQ context: only capture timer-derived timestamps and update state.
    if (!capture_primed) {
        reference_timestamp_us = now_us;
        capture_primed = true;
        return true;
    }

    if (captured_count >= SAMPLE_COUNT) {
        capture_complete = true;
        return false;
    }

    captured_timestamps_us[captured_count] = now_us;
    captured_count += 1;

    if (captured_count >= SAMPLE_COUNT) {
        capture_complete = true;
        return false;
    }

    return true;
}

static bool start_capture(void) {
    captured_count = 0;
    capture_complete = false;
    capture_primed = false;
    reference_timestamp_us = 0;

    return add_repeating_timer_us(
        -(int64_t)PERIOD_TARGET_US,
        capture_timer_callback,
        NULL,
        &capture_timer);
}

static void emit_csv(void) {
    uint64_t previous_timestamp_us = reference_timestamp_us;

    printf("env,board,sample_index,period_target_us,timestamp_us,delta_us,jitter_us\n");
    for (uint32_t i = 0; i < SAMPLE_COUNT; ++i) {
        const uint64_t timestamp_us = captured_timestamps_us[i];
        const int64_t delta_us = (int64_t)(timestamp_us - previous_timestamp_us);
        const int64_t jitter_us = delta_us - (int64_t)PERIOD_TARGET_US;

        printf(
            "%s,%s,%" PRIu32 ",%u,%" PRIu64 ",%" PRId64 ",%" PRId64 "\n",
            kEnvName,
            kBoardName,
            i + 1u,
            PERIOD_TARGET_US,
            timestamp_us,
            delta_us,
            jitter_us);

        previous_timestamp_us = timestamp_us;
    }

    fflush(stdout);
}

int main(void) {
    stdio_init_all();

    // Allow the host to open USB CDC before the timer starts.
    sleep_ms(STARTUP_SETTLE_MS);

    if (!start_capture()) {
        while (true) {
            tight_loop_contents();
        }
    }

    while (!capture_complete) {
        tight_loop_contents();
    }

    emit_csv();

    while (true) {
        tight_loop_contents();
    }
}
