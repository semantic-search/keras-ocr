import os
import keras_ocr
import tesserocr
from PIL import Image

pipeline = keras_ocr.pipeline.Pipeline(scale=3)

def recognize_keras(img):
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
    
    response = ' '.join(keras_text) + ' ' + ' '.join(tesser_res.split()) 

    os.remove(file_name)

    return response
