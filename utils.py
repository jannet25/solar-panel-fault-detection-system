import os
import numpy as np
from glob import glob
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import serial
import time

#off
#aud=serial.Serial(port="COM3", baudrate=115200, timeout=.1)
aud=None
"""
If device is connected and you want to run Flask with hardware
aud = serial.Serial(port="COM3", baudrate=115200, timeout=.1)
If no device is connected but you want to run Flask without hardware 
aud = None
"""

_model = None

def get_model():
    global _model
    if _model is None:
        _model = load_model('solar.h5')
    return _model

labels = {0:'not_crack', 1:'crack'}


def pipeline_model(path):
    model = get_model()                                                   #Load model
    img = image.load_img(path, target_size=(150, 150))                    #Load and preprocess the image, 150×150 pixels
    img = image.img_to_array(img) / 255.0                                 #0–255 to 0–1       
    img = np.expand_dims(img, axis=0)                                     #new dimension (150,150,3 (rgb)) to (1,150,150,3) 1 batch of images.

    pred = model.predict(img)
    pred = np.squeeze(pred) 

    top_indices = np.argsort(pred)[::-1] 
    max_preds = [[labels[idx], round(pred[idx] * 100, 2)] for idx in top_indices]
    
    #off

    if pred[1] == 1:
        aud.write(b"a")
        print("crack.datasend")
        time.sleep(2)
    
        

    paths = sorted(glob('static/uploads/*'), key=os.path.getctime)   
    if len(paths) > 5:                                              #Keeps only the latest 5 images. Deletes older ones to avoid memory issues.
        for path in paths[:-5]:
            try:
                if os.path.exists(path):
                    os.remove(path)
            except Exception as e:
                print(f"Error removing file {path}: {e}")

    return max_preds


#give ' flask run ' in terminal , if want to stop  ' ctrl+c '.