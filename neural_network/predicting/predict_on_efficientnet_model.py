
import efficientnet.keras
import os, glob, cv2
import matplotlib.pyplot as plt

from config import *


def create_one_example(path, img_width, img_height):
    img = plt.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (img_width, img_height))
        
    return img


def normalize_example(img):
    return img[np.newaxis, :]/255.0



def predict_cataract_efficent(image_path):
    loaded_efficientnet_model = tf.keras.models.load_model('../efficientnet-b0_model.h5')
    effi_example = create_one_example(image_path, IMG_WIDTH, IMG_HEIGHT)
    effi_example = normalize_example(effi_example)

    effi_result = loaded_efficientnet_model.predict(effi_example)
    effi_result_percent = ''
    try:
      effi_result_percent = effi_result[0][1] * 100
    except IndexError as e:
      print('Invalid data: {}'.format(e))

    return '{:.2f}%'.format(effi_result_percent)
