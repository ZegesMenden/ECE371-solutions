# Lab1 Buffer Overflow

This lab contains C code for buffer overflow exercises that can run on both test environments (laptop) and Raspberry Pi targets.

## Compilation

### For Test Environment (Laptop)
```bash
# Compile lab1 for laptop testing
make lab1_laptop

# Compile LED test for laptop testing  
make led_test_laptop

# Compile all test targets
make all_tests
```

### For Raspberry Pi Target
```bash
# Compile lab1 for Raspberry Pi
make lab1_target

# Compile LED test for Raspberry Pi
make led_test_target

# Compile all Pi targets
make all_targets
```

## Running

### Test Environment
```bash
./build/lab1.exe
./build/led_test.exe
```

### Raspberry Pi
```bash
./build/lab1
./build/led_test
```

## Notes

- Test builds use the `TEST_ON_LAPTOP` flag and include `dummy-wiringPi.h` instead of the actual wiringPi library
- Raspberry Pi builds use the real `wiringPi.h` library for GPIO control
- All executables are built in the `build/` directory