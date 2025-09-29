#if defined(TEST_ON_LAPTOP)
#include "dummy-wiringPi.h"
#else
#include <wiringPi.h>
#endif

#include <stdio.h>

#define RED_LED 2     // Red LED connected to GPIO pin 2

int main() {
    wiringPiSetup();

    pinMode(RED_LED, OUTPUT);

    // Start with OFF
    digitalWrite(RED_LED, LOW);

    printf("System COMPROMISED: Turning RED LED ON...\n");
    digitalWrite(RED_LED, HIGH);
    delay(1000);

    // Reset OFF
    digitalWrite(RED_LED, LOW);

    printf("Done.\n");
    return 0;
}
