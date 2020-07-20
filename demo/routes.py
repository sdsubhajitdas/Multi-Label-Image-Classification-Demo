# Flask Imports
from flask import render_template, url_for, redirect, flash, request
from demo import *
from demo.forms import UploadForm

# Python Imports
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

# Project Imports
import tensorflow as tf
import numpy as np
from PIL import Image

# Loading the pretrained custom model.
model = tf.keras.models.load_model(MODEL_PATH)

if DEBUG_MODE:
    print(f'Device Used: { tf.config.experimental.list_physical_devices()}')
    print(f'Tensorflow Version: {tf.__version__}')

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = UploadForm()
    # Home page.
    if request.method == "GET":
        return render_template("index.html", form=form)

    # Generating and showing results here.
    elif request.method == "POST":
        
        if form.validate_on_submit():
            if DEBUG_MODE:print(f"Filename:\t\t{form.image.data}")

            # No input file.
            if form.image.data.filename in [None," ",""] :
                if DEBUG_MODE: print("FileNotFoundException Caught")
                flash("No file selected","danger")
                return redirect(url_for('home'))

            # Checking if input is image
            if (form.image.data.mimetype.split('/').pop(0) != "image"):
                if DEBUG_MODE: print(f"Not Image(MIME Type):{form.image.data.mimetype}")
                flash("File selected is not supported. Please choose an image","warning")
                return redirect(url_for('home'))
                
            # File selected is valid and good to get processed.
            if form.image.data != None:
                imageName = saveUploadImage(form.image.data)
                predictions = generatePredictions(imageName)
                classes, preds = filterByThreshold(CLASSES,predictions,75)

            return render_template("index.html",imagePath=f"demo_images/{imageName}",classes=classes, preds=preds)

def filterByThreshold(labels, predictions,threshhold=1):
    ''' Fliters the prediction by a certain threshold & creates a new set of lists.'''
    newLabels, newPredictions = list(), list()
    for i in range(len(labels)):
        if predictions[i] >= threshhold:
            newLabels.append(labels[i])
            newPredictions.append(predictions[i])
    return newLabels, newPredictions

def generatePredictions(imageName):
    ''' Reads the image and generates result from pretrained model '''
    imagePath = os.path.join('demo','static', 'demo_images', imageName)
    modelPath = os.path.join('demo','static', 'model', 'demo_model.h5')
    
    # Reading image from storage.
    image = Image.open(imagePath).convert('RGB')
    image = tf.cast(np.array(image), tf.float16)
    image = image/255
    image = tf.image.resize(image, (256,256))
    image = tf.reshape(image, (1,256,256,3))
    
    if DEBUG_MODE:
        print(f"IMAGE PATH:\t\t{imagePath}")
        print(f"MODEL INPUT SHAPE:\t\t{image.shape}")
    # Generating the predictions.
    prediction = model.predict(image)
    prediction = np.round(prediction,2) * 100
    prediction = prediction.astype(int)
    if DEBUG_MODE:
        print(f"MODEL PREDICTION:\t\t{prediction}")
    # Result is  a 2D array we need the 1st array.
    return prediction[0]

def saveUploadImage(pictureData):
    ''' Saves the uploaded image inside internal folder. '''
    picName = pictureData.filename
    picPath = os.path.join(app.root_path,'static', 'demo_images', picName)
    pictureData.save(picPath)
    if DEBUG_MODE:
        print(f"Profile picture saved at location {picPath}")
    return picName