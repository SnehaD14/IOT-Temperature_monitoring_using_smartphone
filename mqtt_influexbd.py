import ssl
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime

# ---------------- InfluxDB Configuration ----------------
influx_url = "http://localhost:8086"
influx_token = "ipYYfuDYAZMqVHV1LiX1bCb_FbhZ88Jg1mauLVteTyXHkp24BfrSazEJRAJksRC2h_oYKAWiGaumUEJGEMCN3w=="
influx_org = "iot_org"
influx_bucket = "temperature_data"

client = InfluxDBClient(url=influx_url, token=influx_token, org=influx_org)
write_api = client.write_api(write_options=SYNCHRONOUS)

# ---------------- MQTT Configuration -------------------
mqtt_broker = "49bff703f52e499b8fb2dc7430d93d3c.s1.eu.hivemq.cloud"
mqtt_port = 8883
mqtt_username = "Iot19"
mqtt_password = "Teamiot19"
mqtt_topic = "iot/temperature"

# ---------------- MQTT Event Handlers -------------------
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to HiveMQ Cloud MQTT Broker")
        client.subscribe(mqtt_topic)
    else:
        print(f"❌ MQTT connection failed with code {rc}")

def on_message(client, userdata, msg):
    payload = msg.payload.decode().strip()
    print(f"📥 Received: {payload}")

    try:
        # Skip non-data/debug messages
        if not any(char.isdigit() for char in payload) or ',' not in payload:
            print("⚠️ Skipped non-data message.")
            return

        parts = payload.split(",")
        if len(parts) != 4 or not parts[0].strip().isdigit():
            print("⚠️ Skipped invalid format.")
            return

        # Extract and clean values
        serial_number = int(parts[0].strip())
        timestamp_str = parts[1].strip()
        temperature = float(parts[2].strip())
        condition = parts[3].strip()

        # Create InfluxDB point
        point = (
            Point("temperature_data")
            .tag("condition", condition)
            .field("serial_number", serial_number)
            .field("timestamp", timestamp_str)
            .field("temperature", temperature)
            .time(datetime.utcnow())
        )

        write_api.write(bucket=influx_bucket, org=influx_org, record=point)
        print("✅ Data written to InfluxDB")

    except Exception as e:
        print(f"❗ Error processing message: {e}")

# ---------------- Start MQTT Client ------------------
mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(mqtt_username, mqtt_password)
mqtt_client.tls_set(tls_version=ssl.PROTOCOL_TLS)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

print("🔁 Connecting to HiveMQ Cloud...")
mqtt_client.connect(mqtt_broker, mqtt_port)
mqtt_client.loop_forever()
