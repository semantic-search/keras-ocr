FROM tensorflow/tensorflow:latest-gpu

RUN apt-get update && apt-get install -y \
  libsm6 \
  libxext6 \
  libxrender-dev\
  tesseract-ocr\
  libtesseract-dev\ 
  libleptonica-dev\ 
  pkg-config\
  libgl1-mesa-glx

COPY ./requirements.txt /app/requirements.txt
COPY ./craft_mlt_25k.h5 /root/.keras-ocr/craft_mlt_25k.h5
COPY ./crnn_kurapan.h5 /root/.keras-ocr/crnn_kurapan.h5

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

