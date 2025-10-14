
#if defined(TEST_ON_LAPTOP)
#include "dummy-wiringPi.h"
#else
#include <wiringPi.h>
#endif

#include <stdio.h>
#include <stdint.h>
#pragma pack(1)   

// TODO: Define GPIO pin for LED
// The numbers following the LED stand for the wiringPi numbering scheme, On a Raspberry Pi 4: WiringPi 2 (GPIO 27) → Physical pin 13; 

#define LED_PIN 2

struct {
    char username[8];       
    char password[8];       
    int flag;               
    char system_api_key[32]; 
} data;

int main() {
    //TODO: Setup wiringPi (see test1.c for reference)

    wiringPiSetup();
    pinMode(LED_PIN, OUTPUT);
    digitalWrite(LED_PIN, LOW);

    data.flag = 0;
    printf("===Initializing System Password===");
    // Initialize system password (protected secret)
    // TODO: Either prompt for system password and use gets() to take system password as an input or Set data.system_api_key to a password of your choice below
    // snprintf(data.system_api_key, sizeof(data.system_api_key), "SUPER_SECRET_API_KEY_12345");

    snprintf(data.system_api_key, sizeof(data.system_api_key)/sizeof(char), "SECRET_PASS_0X252342");
    printf("System key is loaded in memory (not normally visible to users).\n\n");

    printf("=== VaultApp Login ===\n");
    
    // Prompt for username
    // TODO: Use gets() to read into data.username
    printf("Enter Username:\n");
    for ( int i = 0; i < (sizeof(data.username) / sizeof(data.username[0])) + 1; i++ ) {

        char c = getchar();
        if ( c == '\n' ) { break; }
        if ( i < sizeof(data.username) / sizeof(data.username[0]) ) {
            data.username[i] = c;
        }

    }

    // TODO: Prompt for password
    // TODO: Use gets() to read into data.password
    printf("Enter Password:\n");
    for ( int i = 0; i < (sizeof(data.password) / sizeof(data.password[0])) + 1; i++ ) {

        char c = getchar();
        if ( c == '\n' ) { break; }
        if ( i < sizeof(data.password) / sizeof(data.password[0]) ) {
            data.password[i] = c;
        } else {
            break;
        }

    }

    // print state
    
    printf("Current state:\n");
    printf("\tUsername:\t<");
    for ( size_t i = 0; i < (sizeof(data.username) / sizeof(data.username[0])); i++ ) {
        printf("%c", data.username[i]);
    }
    printf(">\n");
    printf("\tPassword:\t<");
    for ( size_t i = 0; i < (sizeof(data.username) / sizeof(data.username[0])); i++ ) {
        printf("%c", data.password[i]);
    }
    printf(">\n");
    
    printf("\tFlag:\t\t<");
    for ( size_t i = 0; i < sizeof(data.flag); i++ ) {
        printf("0x%02x%c", ((uint8_t*)&data.flag)[i], i == sizeof(data.flag)-1 ? '>' : ' ');
    }
    printf("\n");

    printf("\tAPI Key:\t<");
    for ( size_t i = 0; i < sizeof(data.system_api_key) / sizeof(data.system_api_key[0]); i++ ) {
        printf("%c", data.system_api_key[i]);
    }
    printf(">\n");
    
    // TODO: Print current state and addresses of username, password, and flag

    if ( data.flag != 0 ) {
        printf("COMPROMISED\n");
        printf("SYSTEM_API_KEY:\n");
        printf("\t<%s>\n", data.system_api_key);
        digitalWrite(LED_PIN, HIGH);

    } else {
        printf("SAFE\n");
    }

    // TODO: Add logic
    // If flag != 0 → COMPROMISED
    //   Print system_password and turn RED LED ON
    // Else → SAFE
    //   Print "System password protected" 

    return 0;
}
