import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
import glob
import pathlib
import random
from datetime import datetime
import sys


import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Flatten
from tensorflow.keras.layers import Conv2D



np.set_printoptions(threshold=np.inf)  #Uncomment if you want to see a full np array

BATCH_SIZE = 5
EPOCHS = 2
RESIZE_FACTOR = 10
NAME = "resize-factor-10-2-" + str(datetime.now())




all_image_paths = list(glob.glob('training/images/*/*.jpg'))
#all_image_paths = list(glob.glob('testing/images/test/*/*.jpg'))

label_names = ['daytona', 'sebring', 'long-beach', 'mid-ohio', 'watkins-glen', 'belle-isle']

label_to_index = dict((name, index) for index,name in enumerate(label_names))
all_image_labels = [label_to_index[pathlib.Path(path).parent.name]
                    for path in all_image_paths]

#print(all_image_labels)

IMG_SIZE_X = (1280 // RESIZE_FACTOR)
IMG_SIZE_Y = (720 // RESIZE_FACTOR)
X_LEFT = int(0.25 * IMG_SIZE_X)
Y_TOP = int(0.12 * IMG_SIZE_Y)
Y_BOTTOM = int(0.07 * IMG_SIZE_Y)


training_data = []

for i, img in enumerate(all_image_paths):  # iterate over each image per dogs and cats
    img_array = cv2.imread(img,0)  # convert to array
    small_img = cv2.resize(img_array, (IMG_SIZE_X, IMG_SIZE_Y))
    cropped_img = small_img[Y_TOP:(IMG_SIZE_Y-Y_BOTTOM), X_LEFT:IMG_SIZE_X]
    # print(small_img)
    # plt.imshow(cropped_img, cmap='gray')  # graph it
    # plt.show()  # display!
    # print(cropped_img.shape)
    # if(i == 10):
    #     break  # we just want one for now so break
    img_shape = cropped_img.shape
    training_data.append([cropped_img, all_image_labels[i]])


#print(training_data)


random.shuffle(training_data)
print(len(training_data))
# for sample in training_data[:40]:
#     print(sample[1])




X = []
y = []


for features,label in training_data:
    X.append(features)
    y.append(label)


# print(X)
# print(y)

num_classes = len(label_names)

y_test = keras.utils.to_categorical(y, num_classes)

#X = np.array(X).reshape(-1, IMG_SIZE_X, IMG_SIZE_Y, 1)
X = np.array(X).reshape(-1, img_shape[0], img_shape[1], 1)
X = X/255.0



tensorboard = TensorBoard(log_dir="logs/" + format(NAME)) 
                            #embeddings_data=training_data,
                            #histogram_freq=1,  
                            #write_graph=True, write_grads=True, write_images=True,
                            #embeddings_freq=1,
                            #embeddings_layer_names=['features'],
                            #embeddings_metadata='metadata.tsv')


model = Sequential()

model.add(Conv2D(32, (3, 3), input_shape=X.shape[1:]))
model.add(Activation('relu'))

model.add(Conv2D(16, (3, 3)))
model.add(Activation('relu'))


model.add(Flatten())  # this converts our 3D feature maps to 1D feature vectors

model.add(Dense(num_classes, activation='softmax', name='features'))

model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

model.fit(X, y_test, batch_size=BATCH_SIZE, epochs=EPOCHS, validation_split=0.1, callbacks=[tensorboard])


model.save('models/' + NAME + '.model')

model.summary()