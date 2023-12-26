#include <Arduino.h>
#include <WiFi.h>
#include <WiFiClient.h>
#include <Wire.h>
#include <Adafruit_HTS221.h>
#include <Adafruit_BMP280.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>


// const char SSID[] = "AISFibre_B7_703_2.4G";
// const char PASSWD[] = "TU@B7703";
// const char SSID[] = "Denied + L + Ratio";
// const char PASSWD[] = "itgs6981";
const char SSID[] = "coffeeshop-2.4G";
const char PASSWD[] = "airsiam29";

Adafruit_BMP280 bmp280;
Adafruit_HTS221 hts221;

WiFiClient wifiClient;
PubSubClient mqttClient;
DynamicJsonDocument devData(256);
DynamicJsonDocument subData(256);
// DynamicJsonDocument bmpData(256);

#define BROKER_SERVER "broker.hivemq.com"
#define BROKER_PORT 1883
#define SERVER_CONNECTION_TIMEOUT 5000

unsigned long pre = 0;
unsigned long interval = 60000; //milisec

void changeInterval(int hour, int min);
void checkMqttConnection();
void printValue(int *temp, int *humid, int* pressure);

// Callback Function
void on_msg(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrvied in topic: ");
  Serial.println(topic);
  Serial.print("Message: ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  deserializeJson(subData, payload);
  changeInterval(subData["hour"], subData["min"]);
  Serial.println();
  Serial.print("Interval has been set to ");
  Serial.print(interval);
  Serial.println(" ms");
  Serial.println("-------------------------------");
}

void setup() {
  Serial.begin(9600);
  Wire.begin(41, 40, 100000);

  delay(3000);
  Serial.print("Checking HTS221...");
  if (hts221.begin_I2C(0x5F)) {
    Serial.print(" Working\n");
  }
  else {
    Serial.println("\nError: HTS221 not found");
    while (true) {}
  }

  Serial.print("Checking BMP280...");
  if (bmp280.begin(0x76)) {
    Serial.print(" Working\n");
  }
  else {
    Serial.println("\nError: BMP280 not found");
    while (true) {}
  }

  Serial.print("Connecting to ");
  Serial.print(SSID);
  WiFi.begin(SSID, PASSWD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected!");
  
  mqttClient.setClient(wifiClient);
  mqttClient.setServer(BROKER_SERVER, BROKER_PORT);
  mqttClient.setCallback(on_msg);
  checkMqttConnection();
  mqttClient.subscribe("cn466/studentnumber85/setting/device/1");
}

void loop() {
  unsigned long curr = millis();
  if (curr - pre >= interval) {
    pre = curr;
    Serial.println("Reconnecting");
    checkMqttConnection();
    char buffer[256];
    sensors_event_t humid, temp;
    hts221.getEvent(&humid, &temp);
    int t = (int) (temp.temperature * 100);
    int h = humid.relative_humidity;
    int p = (int) bmp280.readPressure();
    devData["temp"] = t;
    devData["humid"] = h;
    devData["pressure"] = p;

    size_t n = serializeJson(devData, buffer);
    if (mqttClient.publish("cn466/bigproj/device/1", buffer, false)) {
      Serial.println("Data is sent with following data:");
      printValue(&t, &h, &p);
      Serial.print("Buffer string \"");
      Serial.print(buffer);
      Serial.println("\"");
      Serial.print("Size: ");
      Serial.print(n);
      Serial.println(" byte");
    }
    else {
      Serial.print("Data send failed!\n");
    }
    
  // n = serializeJson(bmpData, buffer);
  // mqttClient.publish("cn466/studentnumber85/bmp280", buffer, n);
  }
  mqttClient.loop();
  // char buffer[256];
  // sensors_event_t humid, temp;
  // hts221.getEvent(&humid, &temp);
  // float t = temp.temperature;
  // int h = humid.relative_humidity;
  // float p = bmp280.readPressure();

  // Serial.print("Temperature: ");
  // Serial.print(t);
  // Serial.println(" C");
  // Serial.print("Humidity: ");
  // Serial.print(h);
  // Serial.println(" %");
  // Serial.print("Pressure: ");
  // Serial.print(p);
  // Serial.println(" Pa");
  // devData["temp"] = t;
  // devData["humid"] = h;
  // devData["pressure"] = p;

  // size_t n = serializeJson(devData, buffer);
  // Serial.println(buffer);
  // if (mqttClient.publish("cn466/studentnumber85/device/1", buffer, false)) {
  //   Serial.print("Data is sent!\n");
  // }
  // else {
  //   Serial.print("Data send failed!\n");
  // }
  // // n = serializeJson(bmpData, buffer);
  // // mqttClient.publish("cn466/studentnumber85/bmp280", buffer, n);
  // mqttClient.loop();
  // delay(60000);
}

void changeInterval(int hour, int min){
  interval = ((hour * 60) + min) * 60000;
}

void checkMqttConnection() {
  unsigned long curr = millis();
  while (!mqttClient.connect("someone")) {
    if (curr - pre >= SERVER_CONNECTION_TIMEOUT) {
      Serial.println("Connection timeout!");
      while (true){}
    }
  }
  Serial.print("Connection to ");
  Serial.print(BROKER_SERVER);
  Serial.println(" established!");
}

void printValue(int *temp, int *humid, int *pressure) {
  Serial.print("Temperature: ");
  Serial.print(*temp);
  Serial.println(" C");
  Serial.print("Humidity: ");
  Serial.print(*humid);
  Serial.println(" %");
  Serial.print("Pressure: ");
  Serial.print(*pressure);
  Serial.println(" Pa");
}