#include <ESP32Servo.h>
#include <dummy.h>
#include <math.h>
#include <Stepper.h>
#include <Arduino.h>
#include <AccelStepper.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <time.h>
#include <WebSocketsClient.h>

// WiFi Credentials
//const char* ssid = "eir53845773";       // Replace with your WiFi SSID
//const char* password = "9fXt7kJEHT"; // Replace with your WiFi password

//const char* ssid = "devolo-978";       // Replace with your WiFi SSID
//const char* password = "k4szrk7x"; // Replace with your WiFi password

const char* ssid = "Gwishy";       // Replace with your WiFi SSID
const char* password = "angus321"; // Replace with your WiFi password

// AWS EC2 API URL 
const char* serverUrl = "f858-134-226-214-245.ngrok-free.app";

WebSocketsClient webSocket;

// Recommended PWM GPIO pins on the ESP32 include 2,4,12-19,21-23,25-27,32-33 
const int trigPin = 13;
const int echoPin = 14;
const int lampPin = 15;
int distance;

const int gasPin = 2;
const int alarmPin = 17;
const int windowPin = 18; 
Servo windowServo;

const int tempPin = 1;
const int fanPin = 4;

AccelStepper myStepper(AccelStepper::FULL4WIRE, 5, 6, 7, 8);
long targetPos = 0;
bool pumpIsOn = false;

bool overrideLamp = false;
bool overrideFan = false;
bool overridePump = false;
bool overrideAlarm = false;
bool overrideWindow = false;


unsigned long previousmillisUS = 0;
const long intervalUS = 500; //(micro seconds => 1/1000 => 1000 microseconds = 1 second)

unsigned long previousmillisTHERM = 0;
const long intervalTHERM = 1000;

unsigned long previousmillisAIR = 0;
const long intervalAIR = 1000;

String inputString = "";  // stores the user input


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


void webSocketEvent(WStype_t type, uint8_t *payload, size_t length) {
  if (type == WStype_TEXT) {
    Serial.print("Received: ");
    Serial.println((char*)payload);

    StaticJsonDocument<200> doc;
    DeserializationError error = deserializeJson(doc, payload);
    if (error) {
      Serial.print("JSON parse failed: ");
      Serial.println(error.c_str());
      return;
    }

    // Handle "message":"Connected"
    if (doc.containsKey("message")) {
      String msg = doc["message"];
      if (msg == "Connected") {
        Serial.println("Server acknowledged connection.");
      }
    }

    // Handle "device":"device" style messages too
    if (doc.containsKey("device") && doc.containsKey("action")) {
      String device = doc["device"];
      String action = doc["action"];

      
      if (device == "LAMP") {
        if (action == "ON") {
          digitalWrite(lampPin, HIGH);
          overrideLamp = true;
          Serial.println("Lamp turned ON");
          
        } else if (action == "OFF") {
          digitalWrite(lampPin, LOW);
          overrideLamp = true;
          Serial.println("Lamp turned OFF");
          
        } else if (action == "AUTO") {
          overrideLamp = false;
          Serial.println("Lamp control back to automatic.");
        }
      }

      if (device == "ALARM") {
        if (action == "ON") {
          digitalWrite(alarmPin, HIGH);
          overrideAlarm = true;
          Serial.println("Alarm turned ON");
          
        } else if (action == "OFF") {
          digitalWrite(alarmPin, LOW);
          overrideAlarm = true;
          Serial.println("Alarm turned OFF");
          
        } else if (action == "AUTO") {
          overrideAlarm = false;
          Serial.println("Alarm control back to automatic.");
        }
      }

      if (device == "FAN") {
        if (action == "ON") {
          digitalWrite(fanPin, LOW);
          overrideFan = true;
          Serial.println("Fan turned ON");
          
        } else if (action == "OFF") {
          digitalWrite(fanPin, HIGH);
          overrideFan = true;
          Serial.println("fan turned OFF");
          
        } else if (action == "AUTO") {
          overrideFan = false;
          Serial.println("Fan control back to automatic.");
        }
      }

      if (device == "PUMP") {
        if (action == "ON") {
          overridePump = true;
          targetPos += 2048; 
          myStepper.moveTo(targetPos);
          Serial.println("Pump turned ON");
          
        } else if (action == "OFF") {
            overridePump = true;
            targetPos -= 2048;          
            myStepper.moveTo(targetPos);
            Serial.println("Pump turned OFF");
            
        } else if (action == "AUTO") {
          overridePump = false;
          Serial.println("Pump control back to automatic.");
        }
      }

      if (device == "WINDOW") {
        if (action == "ON") {
          windowServo.write(180);
          overrideWindow = true;
          Serial.println("Window opened");
          
        } else if (action == "OFF") {
          windowServo.write(0);
          overrideWindow = true;
          Serial.println("Window closed");
          
        } else if (action == "AUTO") {
          overrideWindow = false;
          Serial.println("Window control back to automatic.");
        }
      }
    }
  }
}


// Connect ESP32 to WiFi
void connectWiFi() {
  Serial.print("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
  }
  
  Serial.println("\nConnected to WiFi!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  configTime(0, 0, "pool.ntp.org", "time.nist.gov");

  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
    Serial.println("Failed to obtain time");
    return;
  }

  Serial.println(&timeinfo, "Time: %Y-%m-%d %H:%M:%S");
}


// Send Sensor Data to AWS EC2
void sendSensorData(String sensorName, String timestamp, int sensorValue) {
    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        
        String endpoint = "https://" + String(serverUrl) + "/sensor-data";  // Modify this path as needed
        Serial.print("Sending data to: ");
        Serial.println(endpoint);
        
        http.begin(endpoint);
        http.addHeader("Content-Type", "application/json");

        // Create JSON Data
        StaticJsonDocument<200> jsonDoc;
        jsonDoc["sensor"] = sensorName;
        jsonDoc["timestamp"] = timestamp;  
        jsonDoc["value"] = sensorValue;

        String requestBody;
        serializeJson(jsonDoc, requestBody);
        
        Serial.print("Request body: ");
        Serial.println(requestBody);
        
        // Send HTTP POST request
        int httpResponseCode = http.POST(requestBody);
        Serial.print("HTTP Response code: ");
        Serial.println(httpResponseCode);
        
        if (httpResponseCode > 0) {
            String response = http.getString();
            Serial.println("Response:");
            Serial.println(response);
        } else {
            Serial.print("Error sending HTTP request: ");
            Serial.println(http.errorToString(httpResponseCode));
        }
        
        http.end();
    } else {
        Serial.println("WiFi Disconnected, cannot send data.");
        connectWiFi();  // Attempt to reconnect
    }
}


String getTimestamp() {
    struct tm timeinfo;
    time_t now;
    time(&now);              // get current time in seconds
    now += 3600;             // add 1 hour (3600 seconds)
    localtime_r(&now, &timeinfo);
    char buffer[30];
    strftime(buffer, sizeof(buffer), "%Y-%m-%dT%H:%M:%SZ", &timeinfo);  // outputs in UTC format
    return String(buffer);
}



void setup() {
  Serial.begin(115200);
  connectWiFi();
//  String websocketString = "wss://" + String(serverUrl); //"wss://" + "f858-134-226-214-245.ngrok-free.app";
//  webSocket.beginSSL(websocketString, 443, "/ws/connect/ok");
  webSocket.beginSSL("4ac9-134-226-214-244.ngrok-free.app", 443, "/ws/connect/ok");
  webSocket.onEvent(webSocketEvent);
  webSocket.setReconnectInterval(5000);
  
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(lampPin, OUTPUT);

  pinMode(fanPin, OUTPUT);
  digitalWrite(fanPin, HIGH);

  pinMode(tempPin, INPUT);
  windowServo.attach(windowPin);
  
  pinMode(alarmPin, OUTPUT);

  myStepper.setMaxSpeed(200);     // steps/sec
  myStepper.setAcceleration(100);  // steps/sec^2
  myStepper.setCurrentPosition(0);
}


void loop() {
//  Serial.println("------------------------------------------------------------");
  webSocket.loop();
  myStepper.run();  // must be called often!

  String timestamp = getTimestamp();
  if (Serial.available()) {
    inputString = Serial.readStringUntil('\n');
    inputString.trim();
  }

//   Only trigger the US sensor every {intervalUS} ms
  // ULTRASONIC SENSOR
  unsigned long currentmillisUS = millis();
  if (currentmillisUS - previousmillisUS >= intervalUS) {
    previousmillisUS = currentmillisUS;
    distance = usSensor(trigPin, echoPin);
    Serial.println("Distance: " + String(distance) + " cm");
//    sendSensorData("Distance", timestamp, distance);

    if (overrideLamp == false) {
      if (distance < 5) {
        digitalWrite(lampPin, HIGH);
      }
      if (distance > 5) {
        digitalWrite(lampPin, LOW);
      }
    }
  }

  // THERMOMETER
  unsigned long currentmillisTHERM = millis();
  if (currentmillisTHERM - previousmillisTHERM >= intervalTHERM) {
    previousmillisTHERM = currentmillisTHERM;

  double BETA = 3950.0;
  double raw_value = analogRead(tempPin); 
  // Read out the voltage using an analog value
  double voltage = raw_value * 5.0 / 1023.0;
  // Calculation of the temperature using the voltage
  double temperature = ((voltage / 5.0) * 10000.0) / (1.0 - (voltage / 5.0));
  temperature = 1.0 / ((1.0 / 298.15) + (1.0 / BETA) * log(temperature / 10000.0));
  temperature = temperature - 273.15;
  // Output of the measured value
  Serial.println("Temperature: " + String(temperature) + " C");
//  sendSensorData("Temperature", timestamp, temperature);
  
    if (inputString == "tempOVER") {
      if (overrideFan == false) {
        digitalWrite(fanPin, LOW);
      }
    
      if (pumpIsOn == false && overridePump == false) {
//        targetPos += 2048;
//        myStepper.moveTo(targetPos);
        myStepper.moveTo(1024);
        pumpIsOn = true;
      }
    }
    
    if (inputString == "tempUNDER") {
      if (overrideFan == false) {
        digitalWrite(fanPin, HIGH);
      }
    
      if (pumpIsOn == true && overridePump == false) {
//        targetPos -= 2048;
//        myStepper.moveTo(targetPos);
        myStepper.moveTo(0);
        pumpIsOn = false;
      }
    }
  }

  // GAS SENSOR
  unsigned long currentmillisAIR = millis();
  if (currentmillisAIR - previousmillisAIR >= intervalAIR) {
    previousmillisAIR = currentmillisAIR;
    int airValue = analogRead(gasPin);
    Serial.print("Air quality value: ");
    Serial.println(airValue);  // Print raw sensor value
//    sendSensorData("CO2", timestamp, airValue);

    if (inputString == "airOVER") {
      if (overrideAlarm == false) {
        digitalWrite(alarmPin, HIGH);
      }
    
      if (overrideWindow == false) {
        windowServo.write(180);
      }
    }
    
    if (inputString == "airUNDER") {
      if (overrideAlarm == false) {
        digitalWrite(alarmPin, LOW);
      }
    
      if (overrideWindow == false) {
        windowServo.write(0);
      }
    }
  }
  

}
