import json
import time
import datetime

from kafka import KafkaProducer
from uuid import uuid4
import numpy as np

from dotenv import load_dotenv
import os

load_dotenv()

producer = KafkaProducer(
    bootstrap_servers=f'{os.getenv("DOCKER_HOST_IP")}:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

geo_madrid = (40.4168, -3.7038)

NUM_DRONES = 50
DISPERSION = 0.01
MOVEMENT = 0.001

def create_random_drone(center, dispersion):
    return {
        "drone_id": str(uuid4()),
        "location": {
             'type': 'Point',
             'coordinates': [
                 center[1] + np.random.normal(0, dispersion), 
                 center[0] + np.random.normal(0, dispersion)
             ]
        }
    }

drones = [create_random_drone(geo_madrid, DISPERSION) for _ in range(NUM_DRONES)]

def update_drone(drone):
    # Only moves at a 50% prob
    if np.random.uniform() > 0.5:
        location = {
             'type': 'Point',
             'coordinates': [
                 drone["location"]["coordinates"][0] + np.random.normal(0, MOVEMENT), 
                 drone["location"]["coordinates"][1] + np.random.normal(0, MOVEMENT), 
             ]
        }
    else:
        location = drone["location"]
        
    return {
        "drone_id": drone["drone_id"],
        "location": location
    }

while(True):
    drones = [update_drone(d) for d in drones]
    for d in drones:
        
        message = {
            "event": "drone_update",
            "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
            "data": d
        }
        
        producer.send(
            'cabifly.drones', 
            key=d["drone_id"].encode("utf-8"), 
            value=message
        )

    time.sleep(max(np.random.normal(2, 0.5), 0))