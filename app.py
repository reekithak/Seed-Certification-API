from flask import Flask ,render_template , request
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_cors import CORS, cross_origin
from preprocess import predict
from tensorflow.keras.preprocessing.image import load_img

np.set_printoptions(suppress=True)
app = Flask(__name__)
cors = CORS(app,resources={r"/upload/*": {"origins":"*"}})

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
@app.route('/seedbase',methods=['GET','POST'])
@cross_origin()
def seedbase():
    model = tensorflow.keras.models.load_model(r'Models\Seed-Classification\Base_Model.h5')
    if request.method == 'POST' and  'photo' in request.files:
        filename = photos.save(request.files['photo'])    
        image = load_img('./static/img/'+filename,target_size=(224,224))
        prediction = predict(image,model)
        answer = "Excellent:{},Good:{},Average:{},Bad:{},Worst:{}".format(prediction[0][0],
        prediction[0][1],
        prediction[0][2],
        prediction[0][3],
        prediction[0][4])

        return answer

    return render_template('upload.html')





#SEED-COLOR
@app.route('/seedcolor',methods=['GET','POST'])
@cross_origin()
def seedcolor():
    model = tensorflow.keras.models.load_model(r'Models\Seed-Color\Color_Model.h5')
    if request.method == 'POST' and  'photo' in request.files:
        filename = photos.save(request.files['photo']) 
        image = load_img('./static/img/'+filename,target_size=(224,224))
        prediction = predict(image,model)
        answer = "Colored Seed:{},Good Seed:{}".format(prediction[0][0],
        prediction[0][1]
       )

        return answer

    return render_template('upload.html')



#SEED-CRACK
@app.route('/seedcrack',methods=['GET','POST'])
@cross_origin()
def seedcrack():
    model = tensorflow.keras.models.load_model(r'Models\Seed-Crack\Crack_Model.h5')
    if request.method == 'POST' and  'photo' in request.files:
        filename = photos.save(request.files['photo']) 
        image = load_img('./static/img/'+filename,target_size=(224,224))
        prediction = predict(image,model)
        answer = "Cracked Seed :{},Good Seed :{}".format(prediction[0][0],
        prediction[0][1]
        )

        return answer

    return render_template('upload.html')


