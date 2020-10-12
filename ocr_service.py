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

def predict(file_name):

    predictions = recognize_keras(file_name)
    tesser_res = tesserocr.file_to_text(file_name)

    keras_text = []
    # coords = []
    for idx, prediction in enumerate(predictions):
        for word, array in prediction:
            keras_text.append(word)
            # coords.append(array.tolist())
    
    response = ' '.join(keras_text) + ' ' + tesser_res 

    os.remove(file_name)

    return response