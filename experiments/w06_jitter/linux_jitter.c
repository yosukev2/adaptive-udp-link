#define _POSIX_C_SOURCE 200809L

#include <errno.h>
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <time.h>

enum {
    kSampleCount = 1000,
    kTargetPeriodUs = 10000,
    kTargetPeriodNs = 10000000
};

static uint64_t timespec_to_us(const struct timespec *ts) {
    return (uint64_t)ts->tv_sec * UINT64_C(1000000) + (uint64_t)(ts->tv_nsec / 1000);
}

static void timespec_add_ns(struct timespec *ts, uint64_t ns) {
    ts->tv_sec += (time_t)(ns / UINT64_C(1000000000));
    ts->tv_nsec += (long)(ns % UINT64_C(1000000000));

    if (ts->tv_nsec >= 1000000000L) {
        ts->tv_sec += 1;
        ts->tv_nsec -= 1000000000L;
    }
}

static int sleep_until_monotonic(const struct timespec *deadline) {
    int rc;

    do {
        rc = clock_nanosleep(CLOCK_MONOTONIC, TIMER_ABSTIME, deadline, NULL);
    } while (rc == EINTR);

    if (rc != 0) {
        errno = rc;
        return -1;
    }

    return 0;
}

int main(void) {
    struct timespec start_ts = {0};
    struct timespec next_deadline = {0};
    struct timespec sample_ts = {0};
    uint64_t previous_timestamp_us;

    if (clock_gettime(CLOCK_MONOTONIC, &start_ts) != 0) {
        perror("clock_gettime");
        return 1;
    }

    next_deadline = start_ts;
    timespec_add_ns(&next_deadline, kTargetPeriodNs);
    previous_timestamp_us = timespec_to_us(&start_ts);

    puts("env,board,sample_index,period_target_us,timestamp_us,delta_us,jitter_us");

    for (int sample_index = 1; sample_index <= kSampleCount; sample_index++) {
        uint64_t timestamp_us;
        uint64_t delta_us;
        int64_t jitter_us;

        if (sleep_until_monotonic(&next_deadline) != 0) {
            perror("clock_nanosleep");
            return 1;
        }

        if (clock_gettime(CLOCK_MONOTONIC, &sample_ts) != 0) {
            perror("clock_gettime");
            return 1;
        }

        timestamp_us = timespec_to_us(&sample_ts);
        delta_us = timestamp_us - previous_timestamp_us;
        jitter_us = (int64_t)delta_us - (int64_t)kTargetPeriodUs;

        printf(
            "linux_rpi5,raspberry_pi_5,%d,%d,%" PRIu64 ",%" PRIu64 ",%" PRId64 "\n",
            sample_index,
            kTargetPeriodUs,
            timestamp_us,
            delta_us,
            jitter_us
        );

        previous_timestamp_us = timestamp_us;
        timespec_add_ns(&next_deadline, kTargetPeriodNs);
    }

    return 0;
}
