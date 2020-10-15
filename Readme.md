


## RUN IMAGE FROM GHCR 

```sh
docker run --gpus all -it --env-file .env ghcr.io/semantic-search/keras_tesser_ocr
```

- Make sure you have `.env` file with following parameters
```.env
KAFKA_HOSTNAME=
KAFKA_PORT=
MONGO_HOST=
MONGO_PORT=
MONGO_DB=
MONGO_USER=
MONGO_PASSWORD=
KAFKA_CLIENT_ID=
KAFKA_USERNAME=
KAFKA_PASSWORD=
DASHBOARD_URL=
CLIENT_ID=151515
```

To build the docker image locally, run: 

Clone 

```git
git clone --recurse-submodules https://github.com/semantic-search/keras-ocr.git
```

```
docker build -t keras-tesserocr .
```

Run 

```
docker run --gpus all --env-file .env -it keras-tesserocr bash
```

