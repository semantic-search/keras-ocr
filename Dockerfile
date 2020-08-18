FROM tensorflow/tensorflow:latest-gpu

RUN apt-get update && apt-get install -y \
  libsm6 \
  libxext6 \
  libxrender-dev\
  tesseract-ocr\
  libtesseract-dev\ 
  libleptonica-dev\ 
  pkg-config

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 80

COPY . /app

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
