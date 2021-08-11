# -*- coding: utf-8 -*-
"""
Created on Sat Jun 26 11:45:03 2021

@author: Kashish
"""

import numpy as np
import os
from flask import Flask, request
from flask import Flask, request, jsonify, render_template
import tensorflow as tf
import cv2

app = Flask(__name__)

BASE_PATH = os.getcwd()
UPLOAD_PATH = os.path.join(BASE_PATH,'static/upload/')

model = tf.keras.models.load_model('static/models')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/classify', methods=['POST'])
def classify():
    '''
    For rendering results on HTML GUI
    '''
    upload_file = request.files['image_name']

    filename = upload_file.filename
    print(filename)

    ext = filename.split('.')[-1]
    print('The extension of the filename =', ext)
    if ext.lower() in ['png', 'jpg', 'jpeg']:
        # saving the image
        path_save = os.path.join(UPLOAD_PATH, filename)
        upload_file.save(path_save)
        print('File saved sucessfully')

    # Use the uploaded image

        # load the test image
        image = cv2.imread(path_save)
        output = image.copy()
        image = cv2.resize(image, (128, 128))

        # scale the pixels
        image = image.astype('float') / 255.0

        image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))

        # predict
        pred = model.predict(image)
        animal = 'Cat' if pred[0][0] > pred[0][1] else 'Dog'
        print(animal)

    return render_template('index.html', prediction_text='The animal in the picture seems to be a {}'.format(animal))


if __name__ == '__main__':
    app.run()


