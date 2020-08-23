from Util.Azure import getData

import keras_ocr
from PIL import Image
from pathlib import Path


# imports for env kafka
from dotenv import load_dotenv
from kafka import KafkaProducer
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


RECEIVE_TOPIC = 'KERAS_OCR'
SEND_TOPIC_FULL = "IMAGE_RESULTS"
SEND_TOPIC_TEXT = "TEXT"

print(f"kafka : {KAFKA_HOSTNAME}:{KAFKA_PORT}")

# Redis initialize
r = redis.StrictRedis(host=REDIS_HOSTNAME, port=REDIS_PORT,
                      password=REDIS_PASSWORD, ssl=True)

# To receive img data to process
consumer_kerasocr = KafkaConsumer(
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


def recognize(img):
    pipeline = keras_ocr.pipeline.Pipeline(scale=3)
    # actually here's only 1 image in this list
    images = [keras_ocr.tools.read(img)]
    predictions = pipeline.recognize(images)
    return predictions


for message in consumer_kerasocr:
    print('xxx--- inside consumer_kerasocr---xxx')
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
    predictions = recognize(image)

    # delete the image after use
    os.remove(image_path)

    full_res = {
        'blob_name': blob_name
    }
    text_res = {
        'blob_name': blob_name
    }
    text = []
    coords = []
    for idx, prediction in enumerate(predictions):
        for word, array in prediction:
            text.append(word)
            coords.append(array.tolist())

    full_res["data"] = {"text": text, "coords": coords}
    text_res["data"] = {"text": text}
    print(text_res)

    # sending full and text res(without cordinates or probability) to kafka
    producer.send(SEND_TOPIC_FULL, value=full_res)
    producer.send(SEND_TOPIC_TEXT, value=text_res)

    producer.flush()
