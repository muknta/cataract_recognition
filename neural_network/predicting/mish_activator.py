"""
  Need to be install
"""
# !pip install openpyxl

import os, glob, cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.utils import get_custom_objects

from mish_activator import *
from config import *


get_custom_objects().update({'mish': mish})


def create_one_example(path, img_width, img_height):
    img = plt.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (img_width, img_height))

    return img


def normalize_example(img):
    return img[np.newaxis, :]/255.0


def predict_cataract(image_path):
    model_path = get_full_path('../custom_model_with_activator.h5')

    loaded_model = tf.keras.models.load_model(
          model_path,
          custom_objects={'mish': mish})

    example = create_one_example(image_path, IMG_WIDTH, IMG_HEIGHT)
    example = normalize_example(example)

    result = loaded_model.predict(example)
    try:
      result_percent = result[0][1] * 100
    except IndexError as e:
      print('Invalid data: {}'.format(e))

    print('Custom Model\nDiagnosis: cataract with {:.2f}% probability'.format(result_percent))
    return result_percent
    
