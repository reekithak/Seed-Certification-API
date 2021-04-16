from flask import Flask,render_template, request, jsonify
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_cors import CORS, cross_origin
from preprocess import predict
from tensorflow.keras.preprocessing.image import load_img
import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import io
import base64
import os
from tensorflow.keras.preprocessing.image import load_img


app = Flask(__name__)
cors = CORS(app,resources={
    r"/upload/*": {"origins":"*"},
    r"/seedbase/upload/*": {"origins":"*"},
    r"/seedcolor/upload/*": {"origins":"*"},
    r"/seedcrack/upload/*": {"origins":"*"}
})

app.config['CORS_HEADERS'] = 'Content-Type'
photos = UploadSet('photos',IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = './static/img'
configure_uploads(app,photos)

seed_quality_model = tensorflow.keras.models.load_model('Models/Seed-Classification/Base_Model.h5')
seed_color_model = tensorflow.keras.models.load_model('Models/Seed-Color/Color_Model.h5')
seed_crack_model = tensorflow.keras.models.load_model('Models/Seed-Crack/Crack_Model.h5')

#HOME
@app.route('/home',methods=['GET','POST'])
def home():
    welcome = "Hey Welcome to the Multi-Model Seed-Certification Project!"
    return welcome

#BASE MODEL
@app.route('/seedbase/upload',methods=['GET','POST'])
@cross_origin()
def seed_quality(image_fnames=None):
    if request.method == 'POST' and  'photo' in request.files:
        filenames = image_fnames or [photos.save(image) for image in list(request.files.lists())[0][1]]
        predictions = []

        for filename in filenames:
            image = load_img('./static/img/' + filename, target_size=(224,224))
            prediction = predict(image, seed_quality_model)

            answer = {
                "excellent": prediction[0][0],
                "good": prediction[0][1],
                "average": prediction[0][2],
                "bad": prediction[0][3],
                "worst": prediction[0][4],
                "filenames": filenames
            }

            predictions.append(answer)

            if not image_fnames:
                os.remove('./static/img/' + filename)

        excellent = sum([prediction['excellent'] for prediction in predictions]) / len(predictions)
        good = sum([prediction['good'] for prediction in predictions]) / len(predictions)
        average = sum([prediction['average'] for prediction in predictions]) / len(predictions)
        bad = sum([prediction['bad'] for prediction in predictions]) / len(predictions)
        worst = sum([prediction['worst'] for prediction in predictions]) / len(predictions)

        return {
            "excellent": excellent,
            "good": good,
            "average": average,
            "bad": bad,
            "worst": worst
        }

    return render_template('upload.html')

#SEED-COLOR
@app.route('/seedcolor/upload',methods=['GET','POST'])
@cross_origin()
def seed_color(image_fnames=None):
    if request.method == 'POST' and  'photo' in request.files:
        filenames = image_fnames or [photos.save(image) for image in list(request.files.lists())[0][1]]
        predictions = []

        for filename in filenames:
            image = load_img('./static/img/' + filename, target_size=(224,224))
            prediction = predict(image, seed_color_model)

            answer = {
                "dull": prediction[0][0],
                "colored": prediction[0][1]
            }

            predictions.append(answer)

            if not image_fnames:
                os.remove('./static/img/' + filename)

        colored = sum([prediction['colored'] for prediction in predictions]) / len(predictions)
        dull = sum([prediction['dull'] for prediction in predictions]) / len(predictions)

        return {
            "colored": colored,
            "dull": dull
        }

    return render_template('upload.html')

#SEED-CRACK
@app.route('/seedcrack/upload',methods=['GET','POST'])
@cross_origin()
def seed_crack(image_fnames=None):
    if request.method == 'POST' and  'photo' in request.files:
        filenames = image_fnames or [photos.save(image) for image in list(request.files.lists())[0][1]]
        predictions = []

        for filename in filenames:
            image = load_img('./static/img/' + filename, target_size=(224,224))
            prediction = predict(image, seed_crack_model)

            answer = {
                "cracked": prediction[0][0],
                "notCracked": prediction[0][1]
            }

            predictions.append(answer)

            if not image_fnames:
                os.remove('./static/img/' + filename)

        cracked = sum([prediction['cracked'] for prediction in predictions]) / len(predictions)
        notCracked = sum([prediction['notCracked'] for prediction in predictions]) / len(predictions)

        return {
            "cracked": cracked,
            "notCracked": notCracked
        }

    return render_template('upload.html')

@app.route('/upload',methods=['GET','POST'])
@cross_origin()
def upload():
    if request.method == 'POST' and  'photo' in request.files:
        files = list(request.files.lists())[0][1]
        filenames = [photos.save(image) for image in files]

        seedbase_api = seed_quality(filenames)
        seedcolor_api = seed_color(filenames)
        seedcrack_api = seed_crack(filenames)

        for image in filenames:
            os.remove('./static/img/' + image)
        
        data = {
            "quality": seedbase_api.json,
            "color": seedcolor_api.json,
            "crack": seedcrack_api.json
        }
        
        return data

    return render_template('upload.html')


if __name__ == "__main__":
    app.run(port=5000,debug=True)