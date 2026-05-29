# Firmware

Arduino sketch for ECG data acquisition.

## Setup
- Board: Arduino UNO R4 Minima
- Baud rate: 115200
- Sampling rate: 533Hz (validated)

## Pin Configuration
- A0: ECG signal output from AD8232
- D10: Lead-off detection LO+
- D11: Lead-off detection LO-
- 3.3V: Power to AD8232
- GND: Ground

## Arduino Code

```cpp
void setup() {
  Serial.begin(115200);
  pinMode(10, INPUT);
  pinMode(11, INPUT);
}

void loop() {
  if (digitalRead(10) == 1 || digitalRead(11) == 1) {
    Serial.println('!');
  } else {
    Serial.println(analogRead(A0));
  }
}
```

## Notes
- Close Serial Monitor/Plotter before running Python scripts
- Actual sampling rate is 533Hz due to Arduino R4 Minima 48MHz processor
- Signal is inverted due to electrode polarity -- corrected in software