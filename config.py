import os
import numpy as np
import tensorflow as tf


# # Mounting Google drive
# # This will require authentication
# drive.mount('/content/drive')


SEED = 42
# EPOCHS = 100
# BATCH_SIZE = 32
IMG_HEIGHT = 192
IMG_WIDTH = 256


def seed_everything(seed):
    np.random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    tf.random.set_seed(seed)


seed_everything(SEED)


# input_shape = (IMG_HEIGHT, IMG_WIDTH, 3)


APP_PATH = os.curdir


def get_full_path(*pathes):
    path = ''.join(map(str, pathes))
    return os.path.join(APP_PATH, path)

# # cataract dataset
# IMG_ROOT = 'input/dataset/'
# IMG_DIR = [IMG_ROOT+'1_normal', 
#            IMG_ROOT+'2_cataract', 
#            IMG_ROOT+'2_glaucoma', 
#            IMG_ROOT+'3_retina_disease']

# ocular-disease-recognition dataset
OCU_ROOT = APP_PATH
OCU_IMG_ROOT = APP_PATH

# FULL_IMG_ROOT = get_full_path(IMG_ROOT)
FULL_OCU_ROOT = get_full_path(OCU_ROOT)
FULL_OCU_IMG_ROOT = get_full_path(OCU_IMG_ROOT)
# FULL_OCU_DATA_ROOT = get_full_path(FULL_OCU_ROOT, "data.xlsx")

# ocu_df = pd.read_excel(
#      FULL_OCU_DATA_ROOT,
#      engine='openpyxl',
# )
