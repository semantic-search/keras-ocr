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

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 80

COPY . /app

