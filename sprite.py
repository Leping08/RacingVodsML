import numpy as np
import matplotlib.pyplot as plt
import cv2
import glob
import os, math, time
from PIL import Image


RESIZE_FACTOR = 6

#all_image_paths = list(glob.glob('training/images/*/*.jpg'))

IMG_SIZE_X = (1280 // RESIZE_FACTOR)
IMG_SIZE_Y = (720 // RESIZE_FACTOR)

# small_images = []

# for i, img in enumerate(all_image_paths):  # iterate over each image per dogs and cats
#     img_array = cv2.imread(img,0)  # convert to array
#     small_images.append(cv2.resize(img_array, (IMG_SIZE_X, IMG_SIZE_Y)))

# print(len(small_images))









max_frames_row = 2.0
frames = []
tile_width = 0
tile_height = 0

spritesheet_width = 0
spritesheet_height = 0

#files = list(glob.glob('training/images/*/*.jpg'))
files = list(glob.glob('testing/images/test/*.jpg'))
files.sort()
print(files)

for current_file in files :
    try:
        with Image.open(current_file) as im :
            #im = im.resize((IMG_SIZE_Y, IMG_SIZE_X), Image.ANTIALIAS)
            frames.append(im.getdata())
    except:
        print(current_file + " is not a valid image")

tile_width = frames[0].size[0] 
tile_height = frames[0].size[1]

if len(frames) > max_frames_row :
    spritesheet_width = tile_width * max_frames_row
    required_rows = math.ceil(len(frames)/max_frames_row)
    spritesheet_height = tile_height * required_rows
else:
    spritesheet_width = tile_width*len(frames)
    spritesheet_height = tile_height
    
print(spritesheet_height)
print(spritesheet_width)

spritesheet = Image.new("RGBA",(int(spritesheet_width), int(spritesheet_height)))

for current_frame in frames :
    top = tile_height * math.floor((frames.index(current_frame))/max_frames_row)
    left = tile_width * (frames.index(current_frame) % max_frames_row)
    bottom = top + tile_height
    right = left + tile_width
    
    box = (left,top,right,bottom)
    box = [int(i) for i in box]
    cut_frame = current_frame.crop((0,0,tile_width,tile_height))
    
    spritesheet.paste(cut_frame, box)
    
spritesheet.save("spritesheet" + time.strftime("%Y-%m-%dT%H-%M-%S") + ".png", "PNG")