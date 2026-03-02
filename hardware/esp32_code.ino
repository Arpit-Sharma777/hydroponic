#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "YOUR_WIFI";
const char* password = "YOUR_PASSWORD";
const char* serverName = "http://YOUR_PC_IP:5000/predict";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
  }
}

void loop() {

  float pH = 6.5;
  float TDS = 1200;
  float water_level = 50;
  float DHT_temp = 28;
  float DHT_humidity = 65;
  float water_temp = 24;

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");

    String jsonData = "{";
    jsonData += "\"pH\":" + String(pH) + ",";
    jsonData += "\"TDS\":" + String(TDS) + ",";
    jsonData += "\"water_level\":" + String(water_level) + ",";
    jsonData += "\"DHT_temp\":" + String(DHT_temp) + ",";
    jsonData += "\"DHT_humidity\":" + String(DHT_humidity) + ",";
    jsonData += "\"water_temp\":" + String(water_temp);
    jsonData += "}";

    int httpResponseCode = http.POST(jsonData);

    http.end();
  }

  delay(10000);
}