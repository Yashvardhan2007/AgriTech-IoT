import json
import time
import paho.mqtt.client as mqtt

# --- Configuration ---
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "agritech/yash/sensor_data"

# Mock User Profile: Simulated crop threshold preferences
USER_CROP_INTERESTS = {
    "crop_name": "Tomato",
    "max_temp_threshold": 35.0,  # Tomatoes struggle above 35°C
    "min_temp_threshold": 10.0   # Tomatoes freeze/stunt below 10°C
}

def on_connect(client, userdata, flags, rc):
    """Callback triggered when connecting to the cloud broker."""
    if rc == 0:
        print("✅ Successfully connected to HiveMQ Cloud Broker!")
        # Subscribe to the topic your virtual hardware is publishing to
        client.subscribe(MQTT_TOPIC)
        print(f"📡 Listening for live AgriTech IoT data on: {MQTT_TOPIC}\n")
    else:
        print(f"❌ Connection failed with code {rc}")

def on_message(client, userdata, msg):
    """Callback triggered whenever new sensor telemetry arrives."""
    try:
        # Decode the incoming JSON string from the virtual ESP32
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)
        
        device_id = data.get("device_id", "Unknown")
        temp = data.get("temperature")
        humidity = data.get("humidity")
        
        print(f"📥 [DATA RECEIVED] Device: {device_id} | Temp: {temp}°C | Humidity: {humidity}%")
        
        # Check temperature against user's crop interests
        evaluate_crop_safety(temp, humidity)

    except Exception as e:
        print(f"⚠️ Error parsing incoming data: {e}")

def evaluate_crop_safety(current_temp, current_humidity):
    """Evaluates climate conditions and raises high-visibility alerts."""
    crop = USER_CROP_INTERESTS["crop_name"]
    max_thresh = USER_CROP_INTERESTS["max_temp_threshold"]
    min_thresh = USER_CROP_INTERESTS["min_temp_threshold"]
    
    print(f"🧐 Evaluating climate for Target Crop: {crop}...")
    
    if current_temp > max_thresh:
        print(f"🚨 [CRITICAL ALERT] Heat Wave Warning for your {crop} farm!")
        print(f"   -> Current Temp: {current_temp}°C exceeds max limit of {max_thresh}°C!")
        print(f"   -> Suggestion: Activate automated cooling misters immediately.\n")
        
    elif current_temp < min_thresh:
        print(f"🚨 [CRITICAL ALERT] Frost Warning for your {crop} farm!")
        print(f"   -> Current Temp: {current_temp}°C drops below min limit of {min_thresh}°C!")
        print(f"   -> Suggestion: Deploy greenhouse thermal shields.\n")
        
    else:
        print(f"💚 [STATUS: OPTIMAL] Climate conditions are stable for growing {crop}.\n")

# --- Main Execution Layout ---
if __name__ == "__main__":
    print("🚀 Starting AgriTech IoT Gateway Alerting Engine...")
    
    # Initialize the MQTT client instance
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    
    # Connect to the cloud network broker
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    
    # Keep the script running continuously to listen for alerts
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n👋 Gateway Engine stopped safely.")