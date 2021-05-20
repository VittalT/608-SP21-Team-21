
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
static int ROI_width = 2;

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


void checkOptical(){
  for (int i = 84; i<257; i++){
      distanceSensor.setROI(ROI_height, ROI_width, i);  // first value: height of the zone, second value: width of the zone
      distanceSensor.startRanging(); //Write configuration bytes to initiate measurement
      distance = distanceSensor.getDistance(); //Get the result of the measurement from the sensor
      distanceSensor.stopRanging();
      Serial.print("i at ");
      Serial.println(i);
      Serial.print("Distance at: ");
      Serial.println(distance);
  }
}

int i=1;

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
      Serial.println(PplCounter);
      if (PplCounter!= old_PplCounter){ //only posts when the occupancy changes
          Serial.println("People count changed!");
  //        post_to_server();
          old_PplCounter = PplCounter;
      }
      // do the same to the other zone
      Zone++;
      Zone = Zone%2;
    }

    
//    Serial.print("Distance at ");
//    Serial.print(center[0]);
//    Serial.print(" is ");
//    Serial.println(distance);


// UNCOMMENT ENDS HERE
}


void post_to_server(){
    request[0] = '\0'; //set 0th byte to null
    int offset = 0; //reset offset variable for sprintf-ing
    // TODO
    offset += sprintf(request + offset, "POST http://608dev-2.net/sandbox/sc/team21/Server/APIs/UserServerAPI.py HTTP/1.1\r\n"); //TO CHANGE, TEMP
    offset += sprintf(request + offset, "Host: 608dev-2.net\r\n");
    offset += sprintf(request + offset, "Content-Type: application/JSON\r\n");
    int PplCounter_len = 1;
    if (PplCounter>=10 || PplCounter <= 0){
      PplCounter_len = 2;
    }
    if (PplCounter <= -10){
      PplCounter_len = 3;
    }
//    PplCounter_len = strlen(char(PplCounter));
    offset += sprintf(request + offset, "Content-Length: %d\r\n\r\n", 25+strlen(room)+PplCounter_len);
    offset += sprintf(request + offset, "{\"room\":\"%s\",\"occupancy\":\"%d\"}\r\n", room, PplCounter);
    Serial.println(request);
    
    do_http_request("608dev-2.net", request, response, OUT_BUFFER_SIZE, RESPONSE_TIMEOUT, true);
    Serial.println("-----------");
    Serial.println(response);
    Serial.println("-----------");
}

void getDistancetest(){
  distanceSensor.startRanging(); //Write configuration bytes to initiate measurement
  distance = distanceSensor.getDistance(); //Get the result of the measurement from the sensor
  distanceSensor.clearInterrupt();
  distanceSensor.stopRanging();
  Serial.print("distance: ");
  Serial.println(distance/10.00);
}

void getDistance(int current_zone)
{
  distanceSensor.setROI(ROI_height, ROI_width, center[current_zone]);  // first value: height of the zone, second value: width of the zone
  distanceSensor.startRanging(); //Write configuration bytes to initiate measurement
  distance = distanceSensor.getDistance(); //Get the result of the measurement from the sensor
  distanceSensor.stopRanging();
  Serial.print("Zone ");
  Serial.print(current_zone);
  Serial.print(", distance: ");
  Serial.println(distance);
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
      Serial.println("left present");
    }
    else if (Distance - left_old_distance > 100){
      left_person = ABSENT;
      Serial.println("left absent");
    }
    left_old_distance = Distance;
  }

  else if (zone == 1) {
    if (Distance - right_old_distance < -100){
      right_person = PRESENT;
      Serial.println("right present");
    }
    else if (Distance - right_old_distance > 100){
      right_person = ABSENT;
      Serial.println("right absent");
    }
    right_old_distance = Distance;
  }
  
  // state switcher for keeping track of the two areas
  
  if (left_person == ABSENT && right_person == ABSENT){
    both_present = 0;
    Serial.println("nobody seen");
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
    Serial.println("both present");
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

  Serial.print("People counter: ");
  Serial.println(PplCounter);

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
    Serial.println("Pathtrack: ");
    Serial.println(PathTrack[0]);
    Serial.println(PathTrack[1]);
    Serial.println(PathTrack[2]);
    Serial.println(PathTrack[3]);
  }
}
