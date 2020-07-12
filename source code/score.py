import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img

def load_model():
    global model
    model = tf.keras.models.load_model("./outputs/keras_simple.h5")

def load_image(filename):
    img = load_img(filename, target_size=(150, 150))
    img = img_to_array(img)
    img = img.reshape(1, 150, 150, 3)
    img = img.astype('float32')
    return img

def run():
    try:
        for filename in os.listdir('./dog_cat_images/'):
            img = load_image('./dog_cat_images/' + filename)
            result = model.predict(img)
            if result[0] == 0:
                os.rename('./dog_cat_images/' + filename, './dog_cat_images/cat_' + filename)
            else:
                os.rename('./dog_cat_images/' + filename, './dog_cat_images/dog_' + filename)
        print("FINISH")
    except Exception as e:
        print("EXCEPTION", e)

if __name__ == "__main__":
    load_model()
    run()