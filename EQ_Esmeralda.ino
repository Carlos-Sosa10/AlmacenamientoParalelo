//#############################################
//#             Esmeralda                     #
//#############################################

#include <ArduinoJson.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <OneWire.h>                
#include <DallasTemperature.h>

String server = "";

const char *ssid = ".";
const char *password = "G041212s";

const int btnP12 = 4; //D2    
const int btnP1 = 2; //D4    


int p1 = 0;
int act1 = 0;
int p12 = 0;
int act12 = 0;

OneWire ourWire(6);                //Se establece el pin 2  como bus OneWire
DallasTemperature sensors(&ourWire); //Se declara una variable u objeto para nuestro sensor


void setup() {
  
  Serial.begin(115200);

  // led
  pinMode(btnP1, INPUT);
  pinMode(btnP12, INPUT_PULLUP);

  Serial.println("WiFi connected");
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  delay(1000);
  sensors.begin();

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
  }


  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  IPAddress ip = WiFi.localIP();
  Serial.println(ip);

}

void loop() {

sensors.requestTemperatures();   //Se envía el comando para leer la temperatura
float temp= sensors.getTempCByIndex(0); //Se obtiene la temperatura en ºC

  if (WiFi.status() == WL_CONNECTED) {
    if (digitalRead(btnP1) == HIGH) {
      act1 = 1;
      if (p1 != act1) {
        Serial.println("P1 OFF Right");
        Serial.println(temp);
        post("P1", "OFF Right", temp );
        delay(1000);
        p1 = 1;
      }

    }
    else {
      p1 = 0;
      if (p1 != act1) {
        Serial.println("P1 ON Right");
        Serial.println(temp);
        post("p1", "OFF Right", temp );
        delay(1000);
        act1=0;
      }
    }
    
  }

  delay(2000);

}

//-------------------------------------------------------------------------------------

void post(String btn, String pos, float temp) {
  Serial.println("Inicio post");
  HTTPClient http;
  String json;
  server = "http://144.202.34.148:3018/Minip/api";

  StaticJsonDocument<256> doc;
  doc["btn"] = String(btn);
  doc["pos"] = String(pos);
  doc["temp"]= float(temp);
  serializeJson(doc, json);

  http.begin(server);
  http.addHeader("Content-Type", "application/json");
  http.POST(json);
  http.writeToStream(&Serial);
  http.end();
  Serial.println("Termino post");

}
