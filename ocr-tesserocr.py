import tesserocr
from PIL import Image


def predict(file_name, doc=False):
    image = Image.open(image_path)
    res = tesserocr.image_to_text(image)

   
    response = {
        'blob_name': blob_name,
        'data': res
    }

    print(response)

    os.remove(image_path)


