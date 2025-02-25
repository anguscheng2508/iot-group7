#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// WiFi Credentials
const char* ssid = "eir53845773";       // Replace with your WiFi SSID
const char* password = "9fXt7kJEHT"; // Replace with your WiFi password

// AWS EC2 API URL (Use your actual API endpoint)
const char* serverUrl = "http://ec2-54-171-174-135.eu-west-1.compute.amazonaws.com:8000/sensor-data";

// Sensor Pins
const int echoPin = 13;
const int trigPin = 18;

// Timing Variables
unsigned long previousMillis = 0;
const long interval = 5000; // Send data every 5 seconds
int distance;

// Function to Measure Distance
int usSensor(int trigPin, int echoPin) {
    long duration;
    long distance;
    
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
}

// Send Sensor Data to AWS EC2
void sendSensorData(int sensorValue) {
    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        http.begin(serverUrl);
        http.addHeader("Content-Type", "application/json");

        // Create JSON Data
        StaticJsonDocument<200> jsonDoc;
        jsonDoc["sensor"]["device_id"] = 1;
        jsonDoc["sensor"]["sensor_type"] = "Ultrasonic";
        jsonDoc["timestamp"] = "2025-02-21T15:22:36.050Z";  // Ideally, get real-time
        jsonDoc["value"] = sensorValue;

        String requestBody;
        serializeJson(jsonDoc, requestBody);
        
        // Send HTTP POST request
        int httpResponseCode = http.POST(requestBody);
        Serial.print("HTTP Response code: ");
        Serial.println(httpResponseCode);
        
        if (httpResponseCode > 0) {
            String response = http.getString();
            Serial.println("Response:");
            Serial.println(response);
        }
        
        http.end();
    } else {
        Serial.println("WiFi Disconnected, cannot send data.");
    }
}

void setup() {
    Serial.begin(115200);
    
    pinMode(trigPin, OUTPUT);
    pinMode(echoPin, INPUT);
    
    connectWiFi();
}

void loop() {
    unsigned long currentMillis = millis();
    if (currentMillis - previousMillis >= interval) {
        previousMillis = currentMillis;
        
        distance = usSensor(trigPin, echoPin);
        
        Serial.print("Distance: ");
        Serial.print(distance);
        Serial.println(" cm");
        
        sendSensorData(distance);
    }
}
