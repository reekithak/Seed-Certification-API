import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import io
import base64
from flask import request
from flask import jsonify
from flask import Flask
from tensorflow.keras.preprocessing.image import load_img


def preprocess_image(image,target_size=(224, 224)):
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = ImageOps.fit(image, (224,224), Image.ANTIALIAS)
    image_array = np.asarray(image)
    image = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = image 
    
    return data


def predict(image,model):
    processed_image = preprocess_image(image,target_size=(224,224))
    prediction = model.predict(processed_image).tolist()
    return prediction