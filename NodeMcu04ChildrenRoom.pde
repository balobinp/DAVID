#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include "DHT.h"

HTTPClient http;

// Uncomment one of the lines below for whatever DHT sensor type you're using!
#define DHTTYPE DHT11   // DHT 11
//#define DHTTYPE DHT21   // DHT 21 (AM2301)
//#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321
#define VER 190923

const char* web_server_ip = "192.168.1.44";
const char* sensor_id = "4";
const char* ssid = "Home";
const char* password = "ASDFGHQWERTY";

// DHT Sensor GPIO2 ESP01
const int DHTPin = 2;

// Initialize DHT sensor.
DHT dht(DHTPin, DHTTYPE);

String  httpurlconn;
String  httpurldata;

void setup()
{
  Serial.begin(9600);
  delay(100);
  dht.begin();
//  pinMode(2, OUTPUT);
  delay(2000);
  WiFi.disconnect();
  delay(1000);
  Serial.println("Start connecting...");
  WiFi.begin(ssid, password);
  while ((!(WiFi.status() == WL_CONNECTED))){
    delay(300);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("Connected with IP: ");
  Serial.println((WiFi.localIP().toString()));
  
  httpurlconn = "http://";
  httpurlconn += web_server_ip;
  httpurlconn += ":80/connected;sensor=";
  httpurlconn += sensor_id;
  httpurlconn += "&ip=";
  httpurlconn += WiFi.localIP().toString();
  httpurlconn += "&ver=";
  httpurlconn += VER;
  http.begin(httpurlconn);
  http.GET();
  http.end();
}
void loop()
{
//    digitalWrite(2,LOW);
//    delay(1000);
//    digitalWrite(2,HIGH);

    int i = 0;

    // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
    float h = dht.readHumidity();
    // Read temperature as Celsius (the default)
    float t = dht.readTemperature();

    if (isnan(h) && isnan(t)) {
    do {
      h = dht.readHumidity();
      t = dht.readTemperature();  
      i += 1;
      delay(250);
      Serial.print("Failed! Iter No. ");
      Serial.print(i);
      Serial.print(". Var. h is ");
      Serial.print(h);
      Serial.print(", var. t is ");
      Serial.println(t);
    } while ((isnan(h) && isnan(t) && i < 200));
    }

    // Check if any reads failed and exit early (to try again).
    if (isnan(h) && isnan(t)) {
      Serial.println("Failed to read from DHT sensor!");
            }
    else{
      Serial.print("Humidity: ");
      Serial.print(h);
      Serial.print(" %, Temperature: ");
      Serial.print(t);
      Serial.println(" *C ");
    }

    httpurldata = "http://";
    httpurldata += web_server_ip;
    httpurldata += ":80/climate;sensor=";
    httpurldata += sensor_id;
    httpurldata += "&readattempt=";
    httpurldata += i;
    httpurldata += "&temperature=";
    httpurldata += t;
    httpurldata += "&humidity=";
    httpurldata += h;
    http.begin(httpurldata);
    http.GET();
    http.end();
    
//    delay(15000);
    
    delay(900000);
}