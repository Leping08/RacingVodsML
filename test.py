import cv2
import tensorflow as tf
import glob
from prepImgs import cropImages

CATEGORIES = ['daytona', 'sebring', 'longBeach', 'midOhio', 'belleIsle', 'watkinsGlen']

model = tf.keras.models.load_model("models/resize-factor-10-2019-02-25 19:46:49.713816.model")

imagePaths = list(glob.glob('testing/images/daytona/*.jpg'))

c={}

for i, category in enumerate(CATEGORIES):
    c[category] = 0

for i, imagePath in enumerate(imagePaths):
    prediction = model.predict([cropImages(imagePath)])
    index = [i for i, x in enumerate(prediction[0]) if x]
    c[CATEGORIES[index[0]]] += 1

print(c)