from fastapi import FastAPI, File, UploadFile
import os
import keras_ocr
import tesserocr
from PIL import Image
from dotenv import load_dotenv
from kafka import  KafkaProducer
import redis
import json

load_dotenv()

REDIS_HOSTNAME = os.getenv("REDIS_HOSTNAME")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
KAFKA_HOSTNAME = os.getenv("KAFKA_HOSTNAME")
KAFKA_PORT = os.getenv("KAFKA_HOSTNAME")

# Redis initialize
r = redis.StrictRedis(host=REDIS_HOSTNAME, port=REDIS_PORT,
                      password=REDIS_PASSWORD, ssl=True)
# Kafka initialize
producer = KafkaProducer(bootstrap_servers=[f'{KAFKA_HOSTNAME}:{KAFKA_PORT}'],
                        value_serializer=lambda x: json.dumps(x).encode('utf-8'))

app = FastAPI()

pipeline = keras_ocr.pipeline.Pipeline(scale=3)


@app.post("/kerasocr/")
def create_upload_file(file: UploadFile = File(...), image_id):
    
    # Redis Stuff
    r.set("Keras_Container", "BUSY")
    
    fileName = file.filename
    predictions = recognize(file.file)

    response = {
        'image_id': image_id
    }
    text = []
    coords = []
    for idx, prediction in enumerate(predictions):
        for word, array in prediction:
            text.append(word)
            coords.append(array.tolist())

    response[fileName] = {"text": text, "coords" :coords}
    
    # Redis Kafka Stuff
    r.set("Keras_Container", "FREE")
    producer.send('CONTAINER_TOPIC', value=response)

    return response


def recognize(img):
    # actually here's only 1 image in this list
    images = [keras_ocr.tools.read(img)]
    predictions = pipeline.recognize(images)
    return predictions


@app.post("/tesserocr/")
async def upload_file(file: UploadFile = File(...)):

    # # Redis Stuff NOT NEEEDED AS CPU
    # r.set("Keras_Container", "BUSY")

    image = Image.open(file.file)
    res = tesserocr.image_to_text(image)

    # Redis Kafka Stuff
    # r.set("Keras_Container", "FREE")
    producer.send('CONTAINER_TOPIC', value=res)

    return res
