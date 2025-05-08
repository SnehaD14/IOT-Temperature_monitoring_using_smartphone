import serial
import time
import ssl
import paho.mqtt.client as mqtt

# Serial Bluetooth Settings
bluetooth_port = 'COM9'  # Update to your HC-05 COM port
baud_rate = 9600
ser = serial.Serial(bluetooth_port, baud_rate, timeout=2)
time.sleep(2)

# HiveMQ Cloud MQTT Settings
broker = "49bff703f52e499b8fb2dc7430d93d3c.s1.eu.hivemq.cloud"
port = 8883
topic = "iot/temperature"
mqtt_username = "Iot19"
mqtt_password = "Teamiot19"

# MQTT Client Setup
client = mqtt.Client()
client.username_pw_set(username=mqtt_username, password=mqtt_password)
client.tls_set(tls_version=ssl.PROTOCOL_TLS)
client.connect(broker, port)
client.loop_start()  # ✅ Start loop in background

print("🔌 Connected to HiveMQ Cloud. Listening to Bluetooth and sending data...")

try:
    while True:
        if ser.in_waiting > 0:
            try:
                line = ser.readline().decode("utf-8").strip()
                if line and line[0].isdigit():  # simple validation
                    print(f"📤 Publishing: {line}")
                    client.publish(topic, line)
            except UnicodeDecodeError:
                print("⚠️ Decode error: Skipping invalid line")
except KeyboardInterrupt:
    print("❌ Stopped by user.")
finally:
    ser.close()
    client.loop_stop()
    client.disconnect()
