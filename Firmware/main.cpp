#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>

// --- Configuration ---
#define DHTPIN 15          // ESP32 Pin connected to DHT22 data pin
#define DHTTYPE DHT22      // DHT 22 sensor type

// Public, free MQTT Broker (Perfect for testing and simulation)
const char* mqtt_server = "broker.hivemq.com"; 
const char* mqtt_topic  = "agritech/yash/sensor_data";

// --- Hardware & Network Instances ---
DHT dht(DHTPIN, DHTTYPE);
WiFiClient espClient;
PubSubClient client(espClient);

unsigned long lastMsg = 0;
#define INTERVAL_MS 5000   // Send data every 5 seconds for testing

void setup_wifi() {
  delay(10);
  Serial.println("\nConnecting to Virtual Wi-Fi...");
  
  // Wokwi simulator provides a built-in virtual Wi-Fi network named "Wokwi-GUEST"
  WiFi.begin("Wokwi-GUEST", "", 6);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWi-Fi connected!");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  // Loop until we're reconnected to the MQTT broker
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection to HiveMQ...");
    // Create a unique client ID based on ESP32 chip ID
    String clientId = "ESP32Client-" + String(random(0xffff), HEX);
    
    if (client.connect(clientId.c_str())) {
      Serial.println("connected successfully!");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" trying again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  dht.begin();
  setup_wifi();
  client.setServer(mqtt_server, 1883);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  unsigned long now = millis();
  if (now - lastMsg > INTERVAL_MS) {
    lastMsg = now;

    // Reading temperature or humidity takes about 250 milliseconds
    float h = dht.readHumidity();
    float t = dht.readTemperature();

    // Check if any reads failed and exit early (to try again).
    if (isnan(h) || isnan(t)) {
      Serial.println("Failed to read from DHT sensor!");
      return;
    }

    // Format data into a clean JSON string payload
    String payload = "{\"temperature\":" + String(t, 2) + 
                     ",\"humidity\":" + String(h, 2) + 
                     ",\"device_id\":\"ESP32_FIELD_01\"}";

    Serial.print("Publishing telemetry data: ");
    Serial.println(payload);
    
    // Publish data to the cloud network topic
    client.publish(mqtt_topic, payload.c_str());
  }
}