#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

HTTPClient http;

#define DELAY_READ_SENSOR 5000 //Cycle to check the sensor value
#define DELAY_HTTP_REPORT 15000 //Cycle to send the http report
#define VER 190816

const char* web_server_ip = "192.168.1.44";
const char* sensor_id = "2";
const char* ssid = "Home";
const char* password = "ASDFGHQWERTY";
const float threshold_01 = 150.0;
const float threshold_02 = 500.0;

int pin_out_led1 = 16; // D0
int pin_out_led2 = 5; // D1
int pin_out_led3 = 4; // D2
int pin_out_buzzer = 2; // D4

String httpurlconn;
String httpurldata;
float sensorValue;
String ip;
unsigned long last_time;

void setup()
{
    Serial.begin(9600);
    delay(1000);
    WiFi.disconnect();
    delay(2000);
    Serial.println("Start connecting...");
    WiFi.begin(ssid, password);
    while ((!(WiFi.status() == WL_CONNECTED))){
        delay(300);
        Serial.print(".");
      }
    ip = (WiFi.localIP().toString());

    Serial.println("");
    Serial.println("Connected with IP: ");
    Serial.println(ip);

    httpurlconn = "http://";
    httpurlconn += web_server_ip;
    httpurlconn += ":80/connected;sensor=";
    httpurlconn += sensor_id;
    httpurlconn += "&ip=";
    httpurlconn += ip;
    httpurlconn += "&ver=";
    httpurlconn += VER;
    
    http.begin(httpurlconn);
    http.GET();
    http.end();

    pinMode(pin_out_led1, OUTPUT);
    pinMode(pin_out_led2, OUTPUT);
    pinMode(pin_out_led3, OUTPUT);
    pinMode(pin_out_buzzer, OUTPUT);
}

void loop()
{

    digitalWrite(pin_out_led1, LOW);
    digitalWrite(pin_out_led2, LOW);
    digitalWrite(pin_out_led3, LOW);
    digitalWrite(pin_out_buzzer, LOW);

    delay(300);
    
    sensorValue = analogRead(A0);
    Serial.print("Sensor value = ");
    Serial.println(sensorValue);

    if (sensorValue > 0) {
      digitalWrite(pin_out_led1, HIGH);
    }
    
    if (sensorValue > threshold_01) {
      digitalWrite(pin_out_led2, HIGH);
    }
    
    if (sensorValue > threshold_02) {
      digitalWrite(pin_out_led3, HIGH);
      digitalWrite(pin_out_buzzer, HIGH);
      
      httpurldata = "http://";
      httpurldata += web_server_ip;
      httpurldata += ":80/gas;sensor=";
      httpurldata += sensor_id;
      httpurldata += "&sensorValue=";
      httpurldata += String(sensorValue);
      httpurldata += "&type=1";
      
      http.begin(httpurldata);
      http.GET();
      http.end();
    }

    delay(DELAY_READ_SENSOR);

    if (millis() - last_time > DELAY_HTTP_REPORT) {
      httpurldata = "http://";
      httpurldata += web_server_ip;
      httpurldata += ":80/gas;sensor=";
      httpurldata += sensor_id;
      httpurldata += "&sensorValue=";
      httpurldata += String(sensorValue);
      httpurldata += "&type=0";

      http.begin(httpurldata);
      http.GET();
      http.end();

      last_time = millis();
    }
}