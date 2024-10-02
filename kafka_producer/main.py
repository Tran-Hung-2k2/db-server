from kafka import KafkaProducer
import os
import json
import time
import random
from datetime import datetime

TOPIC = os.getenv("TOPIC", "test")
BOOTSTRAP_SERVERS = os.getenv("BOOTSTRAP_SERVERS", "localhost:9092")
INTERVAL = os.getenv("INTERVAL", 0.1)


index = 0

# Create Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)


# Function to produce messages continuously
def produce_messages():
    global index
    while True:
        # Generate a message with random data
        index = index + 1
        message = generate_message(index)
        print(f"Sent message {index}.")
        # Produce the message
        producer.send(TOPIC, value=message)

        # Flush any remaining messages
        producer.flush()

        # Wait for a short interval before producing the next message
        time.sleep(float(INTERVAL))


# Function to generate a message with random data
def generate_message(index):
    # Sample data generation (replace with your own logic)
    now = datetime.now().isoformat()

    message = {
        "index": index,
        "MESSAGE_TYPE": random.randint(0, 3),
        "DEVICE_ID": "device123",
        "IMEI": "123456789012345",
        "IMSI": "123456789012345",
        "TRACKER_STATE": random.randint(0, 1),
        "TRACKER_CREATE_DATE": now,
        "TRACKER_SPEED": random.uniform(0, 100),
        "SOS_STATE": random.randint(0, 1),
        "TRACKER_DIRECTION": random.uniform(0, 360),
        "LATITUDE": random.uniform(-90, 90),
        "LONGTITUDE": random.uniform(-180, 180),
        "SPEEDOMETER_SPEED": random.uniform(0, 100),
        "DOOR1": random.randint(0, 1),
        "DOOR2": random.randint(0, 1),
        "DOOR3": random.randint(0, 1),
        "DOOR4": random.randint(0, 1),
        "CREATE_DATE": now,
        "FUEL_PERCENT": random.uniform(0, 100),
        "ADC1": random.randint(0, 1023),
        "ADC2": random.randint(0, 1023),
        "VOLTAGE": random.uniform(0, 24),
        "TEMPERATURE": random.randint(-40, 80),
        "CAR_MOTOR_STATE": random.randint(0, 1),
        "AIR_STATE": random.randint(0, 1),
        "TRANSPORT_ID": random.randint(0, 100),
        "PASSENGER_STATE": random.randint(0, 1),
        "GSM_SIGNAL": random.randint(0, 100),
        "GPS_SATNUM": random.randint(0, 20),
        "PULSES": random.randint(0, 100),
    }
    return message


# Produce messages continuously
produce_messages()
