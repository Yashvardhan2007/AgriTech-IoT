# AgriTech-IoT

# AgriTech IoT - Smart Tomato Farm Alert System 🍅

This project connects a virtual smart farming sensor to a cloud automation system. It automatically monitors the temperature of a tomato farm and flags an instant warning if the weather gets too hot or too cold for the crops.

---

## 🔗 Live Simulation Link
You can see and test the virtual hardware setup directly in your browser here:
👉 **[Launch Wokwi Smart Farm Simulation](https://wokwi.com/projects/467540381680330753)**

---

## 🗺️ How the System Works (Simply Put)

1. **The Sensor (Wokwi):** A virtual ESP32 microchip reads temperature and humidity data from a green climate sensor on the farm.
2. **The Cloud Highway:** The chip sends this data over the internet using a public cloud network (HiveMQ).
3. **The Alarm Brain (Python):** A Python script running in the cloud listens to that highway. If it notices the temperature spike, it throws an emergency alert.

---

## 🚀 How to Test This Live

You can run this complete end-to-end network test in less than 2 minutes using your terminal:

### 1. Launch the Live Alarm Brain
Open your terminal window and run these quick commands to download the project and start listening for the farm data:

```bash
# Clone this project repository
git clone [https://github.com/Yashvardhan2007/AgriTech-IoT.git](https://github.com/Yashvardhan2007/AgriTech-IoT.git)
cd AgriTech-IoT

# Install the required network library
pip install -r requirements.txt

# Start the alerting system
python gateway/alert_system.py
