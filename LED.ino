#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <FastLED.h>

#define DATA_PIN 4
#define NUM_LEDS 16

CRGB leds[NUM_LEDS];

const char* ssid = "Papa_i_papa";
const char* password = "720804614";
const char* mqtt_server = "broker.emqx.io";
const char* client_id = "esp8255";

WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  // Serial.print("Message arrived [");
  // Serial.print(topic);
  // Serial.print("] ");
  String colorString = "";
  for (int i = 0; i < length; i++) {
    colorString += (char)payload[i];
  }
  
  Serial.println(colorString);
  for (int i = 0; i < NUM_LEDS; i++) {
    String colorCode = colorString.substring(i * 7, (i + 1) * 7);  // Каждый код цвета состоит из 7 символов
    long colorValue = strtol(colorCode.c_str(), NULL, 16);  // Преобразуем строку в цветовой код
    leds[i] = CRGB(colorValue >> 16, (colorValue >> 8) & 0xFF, colorValue & 0xFF);  // Извлекаем значения R, G, B из цветового кода
  }
  
  FastLED.show();
  // Здесь вы можете добавить код для обработки полученного сообщения
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect(client_id)) {
      Serial.println("connected");
      client.subscribe("led/esp8255"); // Замените "your_device_name" на имя вашего устройства
      Serial.println("Subscribed to topic: led/esp8255");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}


void setup() {
  Serial.begin(9600);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}
