#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

String  httpurlconn;
String  httpurldata;
String  ip;

HTTPClient http;

void setup()
{
Serial.begin(9600);

WiFi.disconnect();
delay(3000);
Serial.println("Start connecting");
WiFi.begin("Home","ASDFGHQWERTY");
while ((!(WiFi.status() == WL_CONNECTED))){
    delay(300);
    Serial.print(".");
  }
Serial.println("Connected with IP:");
ip = (WiFi.localIP().toString());
Serial.println(ip);

httpurlconn = "http://192.168.1.44:80/connected;sensor=3&ip=";
httpurlconn+=ip;
http.begin(httpurlconn);
http.GET();
http.end();

pinMode(4, INPUT);
pinMode(5, OUTPUT);

}
void loop()
{
    if (1 == digitalRead(4)) {
      digitalWrite(5,HIGH);
      httpurldata = "http://192.168.1.44:80/motion;sensor=3";
      http.begin(httpurldata);
      http.GET();
      http.end();
      delay(15000);
    } else {
      digitalWrite(5,LOW);
    }
    delay(1000);
}