import os
import keras_ocr
import tesserocr
from PIL import Image


def recognize_keras(img):
    pipeline = keras_ocr.pipeline.Pipeline(scale=3)
    # actually here's only 1 image in this list
    images = [keras_ocr.tools.read(img)]
    predictions = pipeline.recognize(images)

    return predictions

def predict(file_name, doc=False):

    predictions = recognize_keras(file_name)
    tesser_res = tesserocr.image_to_text(file_name)

    text = []
    coords = []
    for idx, prediction in enumerate(predictions):
        for word, array in prediction:
            text.append(word)
            coords.append(array.tolist())
    if doc:
        response = {
            "keras_ocr" : text, 
            "tesser_ocr" : tesser_res
        }
    else:
        response = {
            "file_name": file_name,
            "is_doc_type": False,
            "text": {
                    "keras_ocr" : text,
                    "tesser_ocr" : tesser_res
                    }
        }

    os.remove(file_name)

    return response