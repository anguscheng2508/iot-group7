#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// WiFi Credentials
const char* ssid = "eir53845773";       // Replace with your WiFi SSID
const char* password = "9fXt7kJEHT"; // Replace with your WiFi password

// AWS EC2 API URL (Use your actual API endpoint)
const char* serverUrl = "https://8601-89-101-47-26.ngrok-free.app";

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
void sendSensorData(int sensorValue, String sensorName) {
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
        jsonDoc["device_id"] = 1;        // Moved device_id to root level
        
        // Get current timestamp (if you have a way to get real time)
        jsonDoc["timestamp"] = "2025-02-21T15:22:36.050Z";  
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
        
        sendSensorData(distance, "Distance");
        
    }
}