from flask import Flask ,render_template , request
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
from flask import request
from flask import jsonify
from flask import Flask
from tensorflow.keras.preprocessing.image import load_img
from flask import jsonify, make_response


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

#HOME
@app.route('/home',methods=['GET','POST'])
def home():
    welcome = "Hey Welcome to the Multi-Model Seed-Certification Project!"
    return welcome

#BASE MODEL
@app.route('/seedbase/upload',methods=['GET','POST'])
@cross_origin()
def seedbase(image_fname=None):
    model = tensorflow.keras.models.load_model(r'Models\Seed-Classification\Base_Model.h5')
    if request.method == 'POST' and  'photo' in request.files:
        filename = image_fname or photos.save(request.files['photo'])
        image = load_img('./static/img/'+filename,target_size=(224,224))
        prediction = predict(image,model)
        answer = {
            "Excellent":prediction[0][0],
            "Good":prediction[0][1],
            "Average":prediction[0][2],
            "Bad":prediction[0][3],
            "Worst":prediction[0][4]
        }

        if not image_fname:
            os.remove('./static/img/' + filename)

        return answer

    return render_template('upload.html')

#SEED-COLOR
@app.route('/seedcolor/upload',methods=['GET','POST'])
@cross_origin()
def seedcolor(image_fname=None):
    model = tensorflow.keras.models.load_model(r'Models\Seed-Color\Color_Model.h5')
    if request.method == 'POST' and  'photo' in request.files:
        filename = image_fname or photos.save(request.files['photo'])
        #return {"method": request.method, "url": request.url, "dir": dir(request), "files_len": len(list(request.files.lists())[0][1]), "filename": filename}
        image = load_img('./static/img/'+filename,target_size=(224,224))
        prediction = predict(image,model)
        answer = {"Colored Seed":prediction[0][0],"Good Seed":prediction[0][1]}

        if not image_fname:
            os.remove('./static/img/' + filename)


        return answer

    return render_template('upload.html')

#SEED-CRACK
@app.route('/seedcrack/upload',methods=['GET','POST'])
@cross_origin()
def seedcrack(image_fname=None):
    model = tensorflow.keras.models.load_model(r'Models\Seed-Crack\Crack_Model.h5')
    if request.method == 'POST' and  'photo' in request.files:
        filename = image_fname or photos.save(request.files['photo'])
        image = load_img('./static/img/'+filename,target_size=(224,224))
        prediction = predict(image,model)
        answer = {"Cracked Seed":prediction[0][0],"Good Seed":prediction[0][1]}

        if not image_fname:
            os.remove('./static/img/' + filename)

        return answer

    return render_template('upload.html')

@app.route('/upload',methods=['GET','POST'])
@cross_origin()
def upload():
    if request.method == 'POST' and  'photo' in request.files:
        image = request.files['photo']
        filename = photos.save(image)
        
        seedbase_api = seedbase(filename)
        seedcolor_api = seedcolor(filename)
        seedcrack_api = seedcrack(filename)

        os.remove('./static/img/' + filename)
        
        data = {
            "seedbase": seedbase_api.json,
            "seedcolor": seedcolor_api.json,
            "seedcrack": seedcrack_api.json
        }
        
        return data

    return render_template('upload.html')


if __name__ == "__main__":
    app.run(port=5000,debug=True)