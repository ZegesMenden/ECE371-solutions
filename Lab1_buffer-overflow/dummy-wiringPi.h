#pragma once

#include <stdint.h>
#include <stdio.h>

#define HIGH 1
#define LOW 0

#define OUTPUT 1

void wiringPiSetup() {
    printf("Dummy wiringPiSetup complete.\n");
}

void pinMode(int pin, int mode) {
    printf("Dummy pinMode called for pin %d with mode %d.\n", pin, mode);
}

void digitalWrite(int pin, int value) {
    const char* state = (value == 0) ? "LOW" : "HIGH";
    printf("Dummy digitalWrite called for pin %d: %s.\n", pin, state);
}

#ifdef _WIN32
#include <windows.h>
#else
#include <time.h>
#include <errno.h>
#endif

static inline void delay(uint32_t ms) {

    // I actually have no clue if this works on linux
#ifdef _WIN32
    Sleep(ms);
#else
    struct timespec req, rem;
    req.tv_sec = ms / 1000;
    req.tv_nsec = (ms % 1000) * 1000000L;
    while (nanosleep(&req, &rem) == -1 && errno == EINTR) {
        req = rem;
    }
#endif
}