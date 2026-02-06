import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python import BaseOptions
import cv2
import numpy as np


model_path = './models/deeplab_v3.tflite'
base_options = BaseOptions(model_asset_path=model_path)
options = vision.ImageSegmenterOptions(base_options=base_options,
                                       output_category_mask=True)

# create my segmenter from my options
segmenter = vision.ImageSegmenter.create_from_options(options)

# Loads test headshot image
userHeadshot_path = './test_images/sample_headshot.jpg'
user_headshot = cv2.imread(userHeadshot_path)

# convert file type to what mp needs
mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, 
                    data=user_headshot)

# segment the image
segmentation_res = segmenter.segment(mp_image)

# get the mask
mask = segmentation_res.category_mask

# convert the mask to something that cv2 is able to use
mask_array = mask.numpy_view()

# covert mask from 0 - 15 to 0 - 1
fixed_mask = (mask_array > 0).astype(np.uint8)

# remove the background by applying the mask to the image
just_person = user_headshot * fixed_mask

# save output (lacation and name, to be saved)
cv2.imwrite('./outputs/mask.png', just_person)


print("Mask saved to outputs/mask.png")