import os
import shutil
import time

from fastapi import FastAPI, File, UploadFile
import uuid

from predict_on_efficientnet_model import predict_cataract_efficent

app = FastAPI()

@app.get('/')
def init():
    return {'msg': 'hello'}


@app.post("/cataract/detect")
async def cataract_detect(file: UploadFile = File(...)):
    with open(file.filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_filename = str(uuid.uuid4()) + '.' + file.filename.split('.')[-1]
    os.renames(file.filename, new_filename)
    probability = predict_cataract_efficent(new_filename)
    # TODO: Use model to predict cataract
    return {"result": True, "cataract_probability": probability}
