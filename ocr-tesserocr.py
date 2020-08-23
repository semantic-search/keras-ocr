from Util.Azure import getData

import tesserocr
from PIL import Image
from pathlib import Path

# imports for env kafka
from dotenv import load_dotenv
from kafka import  KafkaProducer
from kafka import KafkaConsumer
from json import loads
import base64
import json
import os
import redis


load_dotenv()


KAFKA_HOSTNAME = os.getenv("KAFKA_HOSTNAME")
KAFKA_PORT = os.getenv("KAFKA_PORT")
REDIS_HOSTNAME = os.getenv("REDIS_HOSTNAME")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
ConnectionString = os.getenv("ConnectionString")


RECEIVE_TOPIC = 'TESSER_OCR'
SEND_TOPIC_FULL = "IMAGE_RESULTS"
SEND_TOPIC_TEXT = "TEXT"

print(f"kafka : {KAFKA_HOSTNAME}:{KAFKA_PORT}")

# Redis initialize
r = redis.StrictRedis(host=REDIS_HOSTNAME, port=REDIS_PORT,
                      password=REDIS_PASSWORD, ssl=True)

# To receive img data to process
consumer_tesserocr = KafkaConsumer(
    RECEIVE_TOPIC,
    bootstrap_servers=[f"{KAFKA_HOSTNAME}:{KAFKA_PORT}"],
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="my-group",
    value_deserializer=lambda x: loads(x.decode("utf-8")),
)

# For Sending processed img data further 
producer = KafkaProducer(
    bootstrap_servers=[f"{KAFKA_HOSTNAME}:{KAFKA_PORT}"],
    value_serializer=lambda x: json.dumps(x).encode("utf-8"),
)

for message in consumer_tesserocr:
    print('xxx--- inside consumer_tesserocr---xxx')
    print(f"kafka - - : {KAFKA_HOSTNAME}:{KAFKA_PORT}")

    
    folder_path = "image/"
    message = message.value

    container_name = message['container_name']
    blob_name = message['blob_name']

    blob_data = getData(ConnectionString, container_name, blob_name)
    # Setting image-id to topic name(container name), so we can know which image it's currently processing
    r.set(RECEIVE_TOPIC, blob_name)

    # set image path and check if folder exist
    image_path = folder_path+blob_name
    Path(folder_path).mkdir(parents=True, exist_ok=True)

    with open(image_path, "wb") as fh:
        fh.write(blob_data)

    image = Image.open(image_path)
    res = tesserocr.image_to_text(image)

    # delete the image after use
    os.remove(image_path)

    response = {
        'blob_name': blob_name,
        'data': res
    }

    print(response)

    # sending full and text res(without cordinates or probability) to kafka
    producer.send(SEND_TOPIC_FULL, value=response)
    producer.send(SEND_TOPIC_TEXT, value=response)

    producer.flush()


