#define FASTLED_ESP8266_RAW_PIN_ORDER
#define FASTLED_ESP8266_NODEMCU_PIN_ORDER
#define FASTLED_ALLOW_INTERRUPTS 0

#define FASTLED_SPI_DEVICE 1
#define FASTLED_SPI_BYTE_ORDER 0
#define FASTLED_SPI_BIT_ORDER 1
#define FASTLED_USE_SPI 1

#define FASTLED_DATA_RATE_KHZ 1000
#define FASTLED_SPI_CLOCK_MHZ 26
#define FASTLED_HAVE_HWSPI


#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <FastLED.h>

#define DATA_PIN 4
#define NUM_LEDS 11

CRGB leds[NUM_LEDS];

const char* ssid = "zababulin";
const char* password = "12345678";
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
  FastLED.addLeds<WS2812B, DATA_PIN, GRB>(leds, NUM_LEDS);
  
  Serial.println(colorString);
 for (int i = 0; i < NUM_LEDS; i++) {
    String colorCode = colorString.substring(i * 7 + 1, (i + 1) * 7);  // Подстрока с 1 по 6 символы каждого кода цвета
    long colorValue = strtol(colorCode.c_str(), NULL, 16);  // Преобразуем строку в цветовой код
    // Serial.print("R: ");
    // Serial.print((colorValue >> 16) & 0xFF, HEX);
    // Serial.print(", G: ");
    // Serial.print((colorValue >> 8) & 0xFF, HEX);
    // Serial.print(", B: ");
    // Serial.println(colorValue & 0xFF, HEX);
    leds[i] = CRGB((colorValue >> 16) & 0xFF, (colorValue >> 8) & 0xFF, colorValue & 0xFF);  // Извлекаем значения R, G, B из цветового кода
}
  // Serial.print(leds);s


  
  FastLED.show();

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
