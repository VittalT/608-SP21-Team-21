#include <WiFi.h>
#include "microphone.h"

const int sampling_rate = 100; // microphone sampling rate in Hertz
const int sampling_period = (int)(1e6 / sampling_rate);
const int posting_period = 3e6; // how often to POST sound data, in milliseconds

const int MIC_PIN = A0; // pin no. of microphone

float filter_val; // history variable for IIR filter
int mic_timer; // timer variable for microphone
int post_timer; // timer variable for HTTP POSTs

Microphone mic = Microphone(A0, sampling_rate);
LPIIR averaging_filter = LPIIR(0.9995);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  WiFi.begin("MIT", "");
  mic_timer = micros();
}

void loop() {
  // put your main code here, to run repeatedly:
  if (micros() - mic_timer >= sampling_period) {
    float intensity = mic.filtered_intensity(0.75);
    float avg = averaging_filter.step(intensity);
    Serial.printf("%f,%f\n", intensity, avg);
    mic_timer = micros();
  }
}
