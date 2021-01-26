from app import app
from glob import glob
import os
from tensorflow import keras
import numpy as np
import tensorflow as tf 
import pickle 
import cv2
from keras.models import Model

modele = keras.models.load_model('app/resources/ResNet50.h5')
new_dict = pickle.load(open('app/resources/new_dict1500.p', 'rb'))
inv_dict = pickle.load(open('app/resources/inv_dict1500.p', 'rb'))
model = keras.models.load_model('app/resources/trainedmodel1500.h5')

def getImage(test_img_path):
    
    test_img = cv2.imread(test_img_path)
    test_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB)

    test_img = cv2.resize(test_img, (224,224))

    test_img = np.reshape(test_img, (1,224,224,3))
    
    return test_img


def get_result():
    images = glob('app/static/img/uploads/' + '*.jpg')
    final_captions = []
    for img in images:

        test_feature = modele.predict(getImage(img)).reshape(1,2048)
        
        test_img = cv2.imread(img)
        test_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB)


        text_inp = ['startofseq']

        count = 0
        caption = ''
        while count < 25:
            count += 1

            encoded = []
            for j in text_inp:
                encoded.append(new_dict[j])

            encoded = [encoded]

            encoded = tf.keras.preprocessing.sequence.pad_sequences(encoded, padding='post', truncating='post', maxlen=36)


            prediction = np.argmax(model.predict([test_feature, encoded]))

            sampled_word = inv_dict[prediction]
            
            if sampled_word == 'endofseq':
                break
            caption = caption + ' ' + sampled_word
                
            text_inp.append(sampled_word)

        final_captions.append(caption)

    return final_captions
