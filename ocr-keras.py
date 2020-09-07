import keras_ocr
from PIL import Image


def recognize(img):
    pipeline = keras_ocr.pipeline.Pipeline(scale=3)
    # actually here's only 1 image in this list
    images = [keras_ocr.tools.read(img)]
    predictions = pipeline.recognize(images)
    return predictions


def predict():
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
