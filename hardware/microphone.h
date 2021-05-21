#ifndef microphone_h
#define microphone_h
#include "Arduino.h"

class LPIIR {
    public:
        LPIIR(float a);
        float step(float input);
        void set(float input);
        void reset();
    private:
        float alpha;
        float last_val;
};

class Microphone {
    public:
        Microphone(int pin, float sample_rate);
        void update_rate(float sample_rate);
        float raw_read();
        float intensity_read();
        float filtered_intensity(float a);
    private:
        int _pin;
        uint32_t _timer;
        float sample_period;
        float last_val;
};

#endif
