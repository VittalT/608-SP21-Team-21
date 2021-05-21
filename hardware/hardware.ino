
#include <Wire.h>
#include "SparkFun_VL53L1X.h"
#include <ESPmDNS.h>
#include <WiFiClient.h>
#include <WiFiUdp.h>
#include <ArduinoOTA.h>
#include <EEPROM.h>
#include <WiFi.h> //Connect to WiFi Network
#include <SPI.h>
#include<math.h>


//MICROPHONE STUFF #####################
#include "microphone.h"

int last_time_noise_posted = 0;

const int sampling_rate = 100; // microphone sampling rate in Hertz
const int sampling_period = (int)(1e6 / sampling_rate);
const int posting_period = 3e6; // how often to POST sound data, in milliseconds

const int MIC_PIN = A0; // pin no. of microphone

float filter_val; // history variable for IIR filter
int mic_timer; // timer variable for microphone
int post_timer; // timer variable for HTTP POSTs

Microphone mic = Microphone(A0, sampling_rate);
LPIIR averaging_filter = LPIIR(0.9995);
float avg;

// MICROPHONE STUFF ##########################



WiFiClient client2; //global WiFiClient Secure object

int timer = millis();

const int RESPONSE_TIMEOUT = 6000; //ms to wait for response from host
const uint16_t IN_BUFFER_SIZE = 2000; //size of buffer to hold HTTP request
const uint16_t OUT_BUFFER_SIZE = 2800; //size of buffer to hold HTTP response
char request[IN_BUFFER_SIZE]; //char array buffer to hold HTTP request
char response[OUT_BUFFER_SIZE]; //char array buffer to hold HTTP response

char network[] = "MIT";
char password[] = "";
uint8_t channel = 1; //network channel on 2.4 GHz

char room[] = "1-115";

const int threshold_percentage = 80;

// this value has to be true if the sensor is oriented as in Duthdeffy's picture
static bool advised_orientation_of_the_sensor = true;

// parameters which define the time between two different measurements in longRange mode
static int delay_between_measurements_long = 55;
static int time_budget_in_ms_long = 50;

// parameters which define the time between two different measurements in longRange mode
static int time_budget_in_ms_short = 20;
static int delay_between_measurements_short = 22;

// value which defines the threshold which activates the short distance mode (the sensor supports it only up to a distance of 1300 mm)
static int short_distance_threshold = 1300;

int distance=0;

#define EEPROM_SIZE 8

SFEVL53L1X distanceSensor;//, SHUTDOWN_PIN, INTERRUPT_PIN);

static int NOBODY = 0;
static int SOMEONE = 1;
static int LEFT = 0;
static int RIGHT = 1;

static int DIST_THRESHOLD_MAX[] = {400, 400};   // treshold of the two zones //HERE
static int MIN_DISTANCE[] = {30, 30}; //HERE

static int PathTrack[] = {0,0,0,0};
static int PathTrackFillingSize = 1; // init this to 1 as we start from state where nobody is any of the zones
static int LeftPreviousStatus = NOBODY;
static int RightPreviousStatus = NOBODY;

//TODO: CALIBRATION
static int center[2] = {28,226}; /* zone1, zone0: center of the two zones */  //HERE
/* Works: 87, 85, 84
Faulty: 50, 80, 83, 88, 89 90, 150 */
static int Zone = 0;
static int old_PplCounter = 0;
static int PplCounter = 0;

static int ROI_height = 8;
static int ROI_width = 4;

static int delay_between_measurements = 0;
static int time_budget_in_ms = 0;


void setup_wifi() 
{
  WiFi.begin(network, password);
  while (WiFi.status() != WL_CONNECTED) 
  {
    delay(500);
    // // Serial.print(".");
    WiFi.begin(network, password);
    // // Serial.print("Attempting to connect to ");
    // // Serial.println(network);
    
    if (WiFi.isConnected()) { //if we connected then print our IP, Mac, and SSID we're on
    // // Serial.println("CONNECTED!");
    //Serial.printf("%d:%d:%d:%d (%s) (%s)\n",WiFi.localIP()[3],WiFi.localIP()[2], WiFi.localIP()[1],WiFi.localIP()[0], WiFi.macAddress().c_str() ,WiFi.SSID().c_str());
    delay(0);
  } else { //if we failed to connect just Try again.
    // // Serial.println("Failed to Connect :/  Going to restart");
    // // Serial.println(WiFi.status());
    ESP.restart(); // restart the ESP (proper way)
  }
  }
}


void setupSensor(){
    if (distanceSensor.init() == false);
    // // Serial.println("Sensor online!");

    
//  if (distanceSensor.begin() != 0) //Begin returns 0 on a good init
//  {
//    // // Serial.println("Sensor failed to begin. Please check wiring. Freezing...");
//    while (1)
//      ;
//  }
//  // // Serial.println("Sensor online!");

}

void setup() {
      Serial.begin(115200);
      Wire.begin();
      EEPROM.begin(EEPROM_SIZE);
      while (!Serial); // wait for // Serial to show up
      setup_wifi();
      setupSensor();
      // // Serial.println(distanceSensor.getI2CAddress()); 
      zones_calibration();

      // MICROPHONE ##########
      mic_timer = micros();
      // MICROPHONE ##########
      PplCounter = 2;
}

void zones_calibration(){
  }


void checkOptical(){
  for (int i = 84; i<257; i++){
      distanceSensor.setROI(ROI_height, ROI_width, i);  // first value: height of the zone, second value: width of the zone
      distanceSensor.startRanging(); //Write configuration bytes to initiate measurement
      distance = distanceSensor.getDistance(); //Get the result of the measurement from the sensor
      distanceSensor.stopRanging();
      // // Serial.print("i at ");
      // // Serial.println(i);
      // // Serial.print("Distance at: ");
      // // Serial.println(distance);
  }
}

void loop(){
//    getDistancetest();

//    checkOptical();
//    delay(9999999);

    //## UNCOMMENT THIS CHUCK

//    center[0] = i;
//    center[1] = i;
//    i++;
    if (millis()-timer>100){
      timer = millis();
      getDistance(Zone);
      
      processPeopleCountingDataREFACTORED(distance, Zone);
      if (PplCounter!= old_PplCounter){ //only posts when the occupancy changes
          post_to_server_occupancy();
          old_PplCounter = PplCounter;
      }
      // do the same to the other zone
      Zone++;
      Zone = Zone%2;
    }
    
    if (micros() - mic_timer >= sampling_period) {
    float intensity = mic.filtered_intensity(0.75);
    avg = averaging_filter.step(intensity);
    
    Serial.printf("%f,%f\n", intensity, avg);
    
    mic_timer = micros();
    if  (millis()-last_time_noise_posted > 30000){
      last_time_noise_posted = millis();
      post_to_server_noise();
    }
  }

    
}



void post_to_server_occupancy(){
    request[0] = '\0'; //set 0th byte to null
    int offset = 0; //reset offset variable for sprintf-ing
    // TODO
    char body[100];
    sprintf(body, "task=updateOccupancy&roomNum=%s&occupancy=%d\r\n", room, PplCounter);
    offset += sprintf(request + offset, "POST http://608dev-2.net/sandbox/sc/team21/Server/APIs/HardwareServerAPI.py HTTP/1.1\r\n");
    offset += sprintf(request + offset, "Host: 608dev-2.net\r\n");
    offset += sprintf(request + offset, "Content-Type: application/x-www-form-urlencoded\r\n");
    offset += sprintf(request + offset, "Content-Length: %d\r\n\r\n", strlen(body));
    offset += sprintf(request + offset, "%s", body);
    // // Serial.println(request);
    
    do_http_request("608dev-2.net", request, response, OUT_BUFFER_SIZE, RESPONSE_TIMEOUT, true);
    // // Serial.println("-----------");
    // // Serial.println(response);
    // // Serial.println("-----------");
}

void post_to_server_noise(){
    request[0] = '\0'; //set 0th byte to null
    int offset = 0; //reset offset variable for sprintf-ing
    // TODO
    char body[100];
//    // // Serial.println("NOISE AVERAGE");
//    // // Serial.println(avg);
    sprintf(body, "task=updateNoiseLevel&roomNum=%s&noiseLevel=%4.2f\r\n", room, avg);
    offset += sprintf(request + offset, "POST http://608dev-2.net/sandbox/sc/team21/Server/APIs/HardwareServerAPI.py HTTP/1.1\r\n");
    offset += sprintf(request + offset, "Host: 608dev-2.net\r\n");
    offset += sprintf(request + offset, "Content-Type: application/x-www-form-urlencoded\r\n");
    offset += sprintf(request + offset, "Content-Length: %d\r\n\r\n", strlen(body));
    offset += sprintf(request + offset, "%s", body);
    // // Serial.println(request);
    
    do_http_request("608dev-2.net", request, response, OUT_BUFFER_SIZE, RESPONSE_TIMEOUT, true);
    // // Serial.println("-----------");
    // // Serial.println(response);
    // // Serial.println("-----------");
}


void getDistancetest(){
  distanceSensor.startRanging(); //Write configuration bytes to initiate measurement
  distance = distanceSensor.getDistance(); //Get the result of the measurement from the sensor
  distanceSensor.clearInterrupt();
  distanceSensor.stopRanging();
//  // // Serial.print("distance: ");
  // // Serial.println(distance/10.00);
}

void getDistance(int current_zone)
{
  distanceSensor.setROI(ROI_height, ROI_width, center[current_zone]);  // first value: height of the zone, second value: width of the zone
  distanceSensor.startRanging(); //Write configuration bytes to initiate measurement
  distance = distanceSensor.getDistance(); //Get the result of the measurement from the sensor
  distanceSensor.stopRanging();
  // // Serial.print("Zone ");
  // // Serial.print(current_zone);
  // // Serial.print(", distance: ");
  // // Serial.println(distance);
}

int ABSENT = 0;
int PRESENT = 1;

int left_old_distance = 0;
int right_old_distance = 0;

int left_person = ABSENT;
int right_person = ABSENT;

int both_present = 0; // the number of boxes that has stuff in. both absent : 0; left check right not : 1; right check left not: 2; both check : 3
int left_first = 0; //1: left first; 2: right first


void processPeopleCountingDataREFACTORED(int16_t Distance, uint8_t zone){

  if (zone == 0) {
    if (Distance - left_old_distance < -100){
      left_person = PRESENT;
      // // Serial.println("left present");
    }
    else if (Distance - left_old_distance > 100){
      left_person = ABSENT;
      // // Serial.println("left absent");
    }
    left_old_distance = Distance;
  }

  else if (zone == 1) {
    if (Distance - right_old_distance < -100){
      right_person = PRESENT;
      // // Serial.println("right present");
    }
    else if (Distance - right_old_distance > 100){
      right_person = ABSENT;
      // // Serial.println("right absent");
    }
    right_old_distance = Distance;
  }
  
  // state switcher for keeping track of the two areas
  
  if (left_person == ABSENT && right_person == ABSENT){
    both_present = 0;
    // // Serial.println("nobody seen");
  }
  else if (both_present == 0){
    if (left_person == PRESENT){
      both_present = 1;
      left_first = 1;
    }
    else if (right_person == PRESENT){
      both_present = 2;
      left_first = 2;
    }
  }

  else if ((both_present == 1 && right_person == PRESENT) or (both_present == 2 && left_person == PRESENT)){ //one persons has been present, need to check whether the other's present
    both_present = 3;
    // // Serial.println("both present");
  }

  // INCREMENT PEOPLE COUNT
  if (both_present == 3 && left_first == 1){

    PplCounter ++;

    both_present = 0;
    left_first = 0;
    left_person = ABSENT;
    right_person = ABSENT;
  }
  else if (both_present == 3 && left_first == 2){

    PplCounter --;
    
    both_present = 0;
    left_first = 0;
    left_person = ABSENT;
    right_person = ABSENT;
  }
}
