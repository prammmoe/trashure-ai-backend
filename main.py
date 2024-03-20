from flask import Flask, session, redirect, url_for, render_template, request, escape
from models.model import load_model
import os
import sys
import glob
import re
from werkzeug.utils import secure_filename
from keras.preprocessing import image
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
import numpy as np
from keras.models import load_model
import tensorflow as tf


app = Flask(__name__)

model = load_model()
print('Model loaded. Start serving ...')

@app.route('/')
def home_page():
    return '<h1>Trashure-AI Backend</h1>'

@app.route('/predict', methods=["GET", "POST"])
def predict(img_path, model, class_names):
    treshold = .6
    img = image.load_img(img_path, target_size=(299, 299))
    img = np.array(img) / 255.

    preds = model.predict_classes(img)
    return preds

def load_model():
    model = tf.keras.load_model('./model.h5')
    class_names = np.load('./nama_kelas.npy')
    return model, class_names
    

def upload():
    if request.method == 'POST':
        # Get the image file from POST req
        f = request.files['file']

        # Save file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        preds = predict(file_path, model)

        #  Arrange the correct return 

    
    


if __name__ == '__main__':
    app.run(debug=True, port=8001)