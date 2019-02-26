import cv2
import tensorflow as tf
import glob

CATEGORIES = ['daytona', 'sebring', 'long-beach', 'mid-ohio', 'belle-isle', 'watkins-glen']

RESIZE_FACTOR = 10

IMG_SIZE_X = (1280 // RESIZE_FACTOR)
IMG_SIZE_Y = (720 // RESIZE_FACTOR)
X_CROP = int(0.25 * IMG_SIZE_X)
Y_CROP = int(0.12 * IMG_SIZE_Y)
Y_Bottom = int(0.07 * IMG_SIZE_Y)


def prepare(filepath):
    img_array = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    small_img = cv2.resize(img_array, (IMG_SIZE_X, IMG_SIZE_Y))
    cropped_img = small_img[Y_CROP:(IMG_SIZE_Y-Y_Bottom), X_CROP:IMG_SIZE_X]
    img_shape = cropped_img.shape
    #new_array = cv2.resize(img_array, (IMG_SIZE_X, IMG_SIZE_Y))
    #cropped_img = small_img[Y_CROP:(IMG_SIZE_Y-Y_Bottom), X_CROP:IMG_SIZE_X]
    return cropped_img.reshape(-1, img_shape[0], img_shape[1], 1)


model = tf.keras.models.load_model("models/resize-factor-10-2019-02-25 19:46:49.713816.model")

imagePaths = list(glob.glob('testing/images/daytona/*.jpg'))

# print(imagePaths)

daytonaTotal = 0
sebringTotal = 0
longbeachTotal = 0
midohioTotal = 0
belleisleTotal = 0
watkinsglenTotal = 0


for i, imagePath in enumerate(imagePaths):
    prediction = model.predict([prepare(imagePath)])
    # print(prediction[0])
    index = [i for i, x in enumerate(prediction[0]) if x]
    # print(CATEGORIES[index[0]])
    if(index[0] == 0):
        daytonaTotal+=1
    if(index[0] == 1):
        sebringTotal+=1
    if(index[0] == 2):
        longbeachTotal+=1
    if(index[0] == 3):
        midohioTotal+=1
    if(index[0] == 4):
        belleisleTotal+=1
    if(index[0] == 5):
        watkinsglenTotal+=1


print("Daytona = " + str(daytonaTotal))
print("Sebring = " + str(sebringTotal))
print("Longbeach = " + str(longbeachTotal))
print("Midohio = " + str(midohioTotal))
print("Belleisle = " + str(belleisleTotal))
print("Watkinsglen = " + str(watkinsglenTotal))