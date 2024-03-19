import tensorflow as tf
import numpy as np

def load_model():
    model = tf.keras.load_model('')
    class_names = np.load('')
    return model, class_names