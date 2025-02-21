#include <dummy.h>

//AVOID:
//GPIO0, GPIO1, GPIO3, GPIO6-11, GPIO2, GPIO15
//GPIO34-39 Input-only, cannot be used with digitalWrite()
//TRY USE:
//4, 5, 12-14 16-19, 21-23, 25-27

const int echoPin = 13; //IO13 = echo;
const int trigPin = 18; //IO18 = trig;

//const int co2Pin = 
//const int humidPin = 
//const int thermPin = 
//const int fanPin = 
//const int windowPin = 

//const int ledTrig = 19;

unsigned long previousmillisUS = 0;
const long intervalUS = 1000; //(micro seconds => 1/1000 => 1000 microseconds = 1 second)
int distance;

int usSensor(int trigPin, int echoPin) {
 long distance;
 long duration;
 
 digitalWrite(trigPin, LOW);
 delayMicroseconds(2);
 digitalWrite(trigPin, HIGH);
 delayMicroseconds(10);
 digitalWrite(trigPin, LOW);
 
 duration = pulseIn(echoPin, HIGH);
 distance = duration * 0.034 / 2;
 return distance;
}

void setup() {
  Serial.begin(115200, SERIAL_8N1);
  
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
//  pinMode(ledTrig, OUTPUT);
}

void loop() {
    // Only trigger the US sensor every {intervalUS} ms
    unsigned long currentmillisUS = millis();
    if (currentmillisUS - previousmillisUS >= intervalUS) {
      previousmillisUS = currentmillisUS;
      distance = usSensor(trigPin, echoPin);
      Serial.print("Distance: ");
      Serial.print(distance);
      Serial.println(" cm");
    }
} 
