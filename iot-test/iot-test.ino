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


// WiFi Credentials
//const char* ssid = "eir53845773";       // Replace with your WiFi SSID
//const char* password = "9fXt7kJEHT"; // Replace with your WiFi password

//const char* ssid = "devolo-978";       // Replace with your WiFi SSID
//const char* password = "k4szrk7x"; // Replace with your WiFi password

const char* ssid = "Gwishy";       // Replace with your WiFi SSID
const char* password = "angus321"; // Replace with your WiFi password

// AWS EC2 API URL (Use your actual API endpoint)
const char* serverUrl = "https://8601-89-101-47-26.ngrok-free.app";

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
  
    // Set up WebSocket
//  webSocket.begin("your.server.ip.or.url", 80, "/ws"); // Replace with your server IP/domain and port/path
//  webSocket.onEvent(webSocketEvent);
//  webSocket.setReconnectInterval(5000);
}


// Send Sensor Data to AWS EC2
void sendSensorData(String sensorName, String timestamp, int sensorValue) {
    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        
        // You might need to append a specific path to your base URL
        String endpoint = String(serverUrl) + "/sensor-data";  // Modify this path as needed
        Serial.print("Sending data to: ");
        Serial.println(endpoint);
        
        http.begin(endpoint);
        http.addHeader("Content-Type", "application/json");

        // Create JSON Data
        StaticJsonDocument<200> jsonDoc;
        jsonDoc["sensor"] = sensorName;  // Changed from object to string with valid enum value
        
        // Get current timestamp (if you have a way to get real time)
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
  
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(lampPin, OUTPUT);

  pinMode(fanPin, OUTPUT);
  digitalWrite(fanPin, HIGH);

  pinMode(tempPin, INPUT);
  windowServo.attach(windowPin);
  
  pinMode(alarmPin, OUTPUT);

  myStepper.setMaxSpeed(1500);     // steps/sec
  myStepper.setAcceleration(100);  // steps/sec^2
  myStepper.setCurrentPosition(0);
}


void loop() {
//  webSocket.loop();
  Serial.println("------------------------------------------------------------");
  String timestamp = getTimestamp();
  if (Serial.available()) {
    inputString = Serial.readStringUntil('\n');
    inputString.trim();
  }

//  unsigned long currentMillis = millis();
//  if (currentMillis - previousMillis >= interval) {
//    previousMillis = currentMillis;
//    // Simulate receiving a message (you can change this string each time)
//    const char* incomingJson = "{\"device\":\"FAN\",\"action\":\"ON\"}";
//    // Parse and act
//    StaticJsonDocument<200> doc;
//    DeserializationError error = deserializeJson(doc, incomingJson);
//
//    if (error) {
//      Serial.print("JSON Parse failed: ");
//      Serial.println(error.c_str());
//      return;
//    }
//
//    String device = doc["device"];
//    String action = doc["action"];
//
//    if (device == "FAN") {
//      if (action == "ON") {
//        digitalWrite(fanPin, LOW);
//        Serial.println("Fan turned ON");
//      } else if (action == "OFF") {
//        digitalWrite(fanPin, HIGH);
//        Serial.println("Fan turned OFF");
//      }
//    }
//  }

//   Only trigger the US sensor every {intervalUS} ms
  // ULTRASONIC SENSOR
  unsigned long currentmillisUS = millis();
  if (currentmillisUS - previousmillisUS >= intervalUS) {
    previousmillisUS = currentmillisUS;
    distance = usSensor(trigPin, echoPin);
    sendSensorData("Distance", timestamp, distance);
    Serial.print("Distance: ");
    Serial.print(distance);
    Serial.println(" cm");
    if (distance < 5) {
      digitalWrite(lampPin, HIGH);
//      Serial.println("Motion detected within Xcm. Turn LAMP ON");
    }
    if (distance > 5) {
      digitalWrite(lampPin, LOW);
    }
  }

  // THERMOMETER
  unsigned long currentmillisTHERM = millis();
  if (currentmillisTHERM - previousmillisTHERM >= intervalTHERM) {
    previousmillisTHERM = currentmillisTHERM;
    int rawValue = analogRead(tempPin);
    double voltage = rawValue * (3.3 / 4095.0);
    double resistance = (3.3 - voltage) * 10000 / voltage;
    double temperature = 1 / (log(resistance / 10000) / 3950 + 1 / 298.15) - 273.15;
    Serial.print("Temperature: ");
    Serial.print(temperature);
    Serial.println(" °C");
    sendSensorData("Temperature", timestamp, temperature);
    
    if (temperature > 15 || inputString == "tempOVER") {
      digitalWrite(fanPin, LOW);
//      Serial.println("Turn Fan ON");
      if (pumpIsOn == false) {
        targetPos += 2048;          // Half rotation forward
        myStepper.moveTo(targetPos);
        pumpIsOn = true;
//        Serial.println("Turn Water Pump ON");
      }
    }
    if (temperature < 15 || inputString == "tempUNDER") {
      digitalWrite(fanPin, HIGH);
//      Serial.println("Turn Fan OFF");
      if (pumpIsOn == true) {
        targetPos -= 2048;          // Half rotation backward
        myStepper.moveTo(targetPos);
        pumpIsOn = false;
//        Serial.println("Turn Water Pump OFF");
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
    sendSensorData("CO2", timestamp, airValue);
    if (airValue > 700 || inputString == "airOVER") {
      windowServo.write(180);
      digitalWrite(alarmPin, HIGH);
//      Serial.println("Air quality bad. OPEN WINDOW. ALARM ON");      
    }
    if (airValue < 700 || inputString == "airUNDER") {
      windowServo.write(0);
      digitalWrite(alarmPin, LOW);
//      Serial.println("Air quality within threshold. CLOSE WINDOW. ALARM OFF");
    }
  }
  myStepper.run();

}
