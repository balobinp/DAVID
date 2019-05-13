#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

String httpurl = "http://192.168.1.44:80/";
String sensor = "sensor=2";
String httpurlconn = httpurl;
String httpurldata;
String ip;
float sensorValue;

HTTPClient http;

const char* ssid = "Home";
const char* password = "ASDFGHQWERTY";

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

    httpurlconn += "connected;";
    httpurlconn += sensor;
    httpurlconn += "&ip=";
    httpurlconn += ip;

    http.begin(httpurlconn);
    http.GET();
    http.end();
}

void loop()
{
    sensorValue = analogRead(A0);
    Serial.print("Sensor value = ");
    Serial.println(sensorValue);

    httpurldata = httpurl;
    httpurldata += "gas;";
    httpurldata += sensor;
    httpurldata += "&sensorValue=";
    httpurldata += String(sensorValue);

    http.begin(httpurldata);
    http.GET();
    http.end();

    delay(900000);
}