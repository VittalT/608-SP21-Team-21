#include "microphone.h"
#include "Arduino.h"

LPIIR::LPIIR(float a) {
    alpha = a;
    reset();
}

float LPIIR::step(float input) {
    float avg = alpha*last_val + (1-alpha)*input;
    set(avg);
    return avg;
}

void LPIIR::set(float input) {
    last_val = input;
}

void LPIIR::reset() {
    last_val = 0;
}

Microphone::Microphone(int pin, float sample_rate) {
    _pin = pin;
    pinMode(_pin, INPUT);
    _timer = micros();
    update_rate(sample_rate);
}

void Microphone::update_rate(float sample_rate) {
    /*
    *  Updates the sampling rate of the microphone,
    *  sample_rate should be a frequency in Hertz
    */
    sample_period = (int)(1e6 / sample_rate);
}

float Microphone::raw_read() {
    /*
    *  Reads the bin value being read from the
    *  microphone pin ADC
    */
    if (micros() - _timer > sample_period) {
        _timer = micros();
        return analogRead(_pin);
    }
}

float Microphone::intensity_read() {
    if (micros() - _timer > sample_period) {
        _timer = micros();
        return abs(analogRead(A0)-1995);
    }
}

float Microphone::filtered_intensity(float a) {
    if (micros() - _timer > sample_period) {
        float avg = a*last_val + (1-a)*abs(analogRead(A0)-1995);
        last_val = avg;
        _timer = micros();
        return avg;
    }
}
