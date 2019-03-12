import cv2

RESIZE_FACTOR = 10

IMG_SIZE_X = (1280 // RESIZE_FACTOR)
IMG_SIZE_Y = (720 // RESIZE_FACTOR)
X_CROP = int(0.25 * IMG_SIZE_X)
Y_CROP = int(0.12 * IMG_SIZE_Y)
Y_Bottom = int(0.07 * IMG_SIZE_Y)


def cropImages(filepath):
    img_array = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    small_img = cv2.resize(img_array, (IMG_SIZE_X, IMG_SIZE_Y))
    cropped_img = small_img[Y_CROP:(IMG_SIZE_Y-Y_Bottom), X_CROP:IMG_SIZE_X]
    img_shape = cropped_img.shape
    return cropped_img.reshape(-1, img_shape[0], img_shape[1], 1)