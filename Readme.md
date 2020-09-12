Build

```
docker build -t keras-tesserocr .
```

Run 

```
docker run --gpus all --env-file .env -it keras-tesserocr bash
```

Clone 

```git
git clone --recurse-submodules https://github.com/semantic-search/keras-ocr.git
```