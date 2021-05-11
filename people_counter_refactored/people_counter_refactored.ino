
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


WiFiClient client2; //global WiFiClient Secure object

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

static int DIST_THRESHOLD_MAX[] = {0, 0};   // treshold of the two zones
static int MIN_DISTANCE[] = {0, 0};

static int PathTrack[] = {0,0,0,0};
static int PathTrackFillingSize = 1; // init this to 1 as we start from state where nobody is any of the zones
static int LeftPreviousStatus = NOBODY;
static int RightPreviousStatus = NOBODY;

static int center[2] = {0,0}; /* center of the two zones */  
static int Zone = 0;
static int PplCounter = 0;

static int ROI_height = 0;
static int ROI_width = 0;

static int delay_between_measurements = 0;
static int time_budget_in_ms = 0;


void setup_wifi() 
{
  WiFi.begin(network, password);
  while (WiFi.status() != WL_CONNECTED) 
  {
    delay(500);
    Serial.print(".");
    WiFi.begin(network, password);
    Serial.print("Attempting to connect to ");
    Serial.println(network);
    
    if (WiFi.isConnected()) { //if we connected then print our IP, Mac, and SSID we're on
    Serial.println("CONNECTED!");
    Serial.printf("%d:%d:%d:%d (%s) (%s)\n",WiFi.localIP()[3],WiFi.localIP()[2],
                                            WiFi.localIP()[1],WiFi.localIP()[0], 
                                          WiFi.macAddress().c_str() ,WiFi.SSID().c_str());
    delay(0);
  } else { //if we failed to connect just Try again.
    Serial.println("Failed to Connect :/  Going to restart");
    Serial.println(WiFi.status());
    ESP.restart(); // restart the ESP (proper way)
  }
  }
}


void setupSensor(){
    if (distanceSensor.init() == false)
    Serial.println("Sensor online!");

    
//  if (distanceSensor.begin() != 0) //Begin returns 0 on a good init
//  {
//    Serial.println("Sensor failed to begin. Please check wiring. Freezing...");
//    while (1)
//      ;
//  }
//  Serial.println("Sensor online!");

}

void setup() {
      Serial.begin(115200);
      Wire.begin();
      EEPROM.begin(EEPROM_SIZE);
      while (!Serial); // wait for Serial to show up
      setup_wifi();
      setupSensor();
      Serial.println(distanceSensor.getI2CAddress()); 
      zones_calibration();

}

void zones_calibration(){
  }



void loop(){
  getDistance(Zone);
  processPeopleCountingData(distance, Zone);
  post_to_server();
  // do the same to the other zone
  Zone++;
  Zone = Zone%2;
}


void post_to_server(){
    request[0] = '\0'; //set 0th byte to null
    int offset = 0; //reset offset variable for sprintf-ing
    // TODO
    offset += sprintf(request + offset, "POST http://608dev-2.net/sandbox/sc/team21/Server/PLACEHOLDER.py HTTP/1.1\r\n");
    offset += sprintf(request + offset, "Host: 608dev-2.net\r\n");
    offset += sprintf(request + offset, "Content-Type: application/x-www-form-urlencoded\r\n");
    int PplCounter_len = 1;
    if (PplCounter>=10){
      PplCounter_len = 2;
    }
    offset += sprintf(request + offset, "Content-Length: %d\r\n\r\n", 24+strlen(room)+PplCounter_len);
    offset += sprintf(request + offset, "{\"room\":\"%s\", \"capacity\":\"%s\"}\"\r\n", room, PplCounter);
    Serial.println(request);
    do_http_request("608dev-2.net", request, response, OUT_BUFFER_SIZE, RESPONSE_TIMEOUT, true);
    Serial.println("-----------");
    Serial.println(response);
    Serial.println("-----------");
}



void getDistance(int current_zone)
{
  distanceSensor.setROI(ROI_height, ROI_width, center[current_zone]);  // first value: height of the zone, second value: width of the zone
  delay(delay_between_measurements);
  distanceSensor.setTimingBudgetInMs(time_budget_in_ms);
  distanceSensor.startRanging(); //Write configuration bytes to initiate measurement
  distance = distanceSensor.getDistance(); //Get the result of the measurement from the sensor
  distanceSensor.clearInterrupt();
  distanceSensor.stopRanging();
  Serial.print("Zone ");
  Serial.print(current_zone);
  Serial.print("distance: ");
  Serial.println(distance/10.00);
}


void processPeopleCountingData(int16_t Distance, uint8_t zone) {

    int CurrentZoneStatus = NOBODY;
    int AllZonesCurrentStatus = 0;
    int AnEventHasOccured = 0;

  if (Distance < DIST_THRESHOLD_MAX[Zone] && Distance > MIN_DISTANCE[Zone]) {
    // Someone is in !
    CurrentZoneStatus = SOMEONE;
  }

  // left zone
  if (zone == LEFT) {

    if (CurrentZoneStatus != LeftPreviousStatus) {
      // event in left zone has occured
      AnEventHasOccured = 1;

      if (CurrentZoneStatus == SOMEONE) {
        AllZonesCurrentStatus += 1;
      }
      // need to check right zone as well ...
      if (RightPreviousStatus == SOMEONE) {
        // event in left zone has occured
        AllZonesCurrentStatus += 2;
      }
      // remember for next time
      LeftPreviousStatus = CurrentZoneStatus;
    }
  }
  // right zone
  else {

    if (CurrentZoneStatus != RightPreviousStatus) {

      // event in left zone has occured
      AnEventHasOccured = 1;
      if (CurrentZoneStatus == SOMEONE) {
        AllZonesCurrentStatus += 2;
      }
      // need to left right zone as well ...
      if (LeftPreviousStatus == SOMEONE) {
        // event in left zone has occured
        AllZonesCurrentStatus += 1;
        Serial.println(AllZonesCurrentStatus);
      }
      // remember for next time
      RightPreviousStatus = CurrentZoneStatus;
    }
  }

  // if an event has occured
  if (AnEventHasOccured) {
    if (PathTrackFillingSize < 4) {
      PathTrackFillingSize ++;
    }

    // if nobody anywhere lets check if an exit or entry has happened
    if ((LeftPreviousStatus == NOBODY) && (RightPreviousStatus == NOBODY)) {

      // check exit or entry only if PathTrackFillingSize is 4 (for example 0 1 3 2) and last event is 0 (nobobdy anywhere)
      if (PathTrackFillingSize == 4) {
        // check exit or entry. no need to check PathTrack[0] == 0 , it is always the case
        Serial.println();
        if ((PathTrack[1] == 1)  && (PathTrack[2] == 3) && (PathTrack[3] == 2)) {
          // this is an entry
          PplCounter ++ ;
        } else if ((PathTrack[1] == 2)  && (PathTrack[2] == 3) && (PathTrack[3] == 1)) {
          // This an exit
          PplCounter -- ;
          
          }
      }
      Serial.print("People Counter: ");
      Serial.println(PplCounter);
      for (int i=0; i<4; i++){
        PathTrack[i] = 0;
      }
      PathTrackFillingSize = 1;
    }
    else {
      // update PathTrack
      // example of PathTrack update
      // 0
      // 0 1
      // 0 1 3
      // 0 1 3 1
      // 0 1 3 3
      // 0 1 3 2 ==> if next is 0 : check if exit
      PathTrack[PathTrackFillingSize-1] = AllZonesCurrentStatus;
    }
  }
}
