import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python import BaseOptions

import cv2
import numpy as np

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os

selected_headshot_path = None
selected_background_path = None

model_path = './models/deeplab_v3.tflite'
base_options = BaseOptions(model_asset_path=model_path)
options = vision.ImageSegmenterOptions(base_options=base_options,
                                        output_category_mask=True)

# create my segmenter from my options
segmenter = vision.ImageSegmenter.create_from_options(options)

def getHeadshot ():
    global selected_headshot_path
    selected_headshot_path = filedialog.askopenfilename(title="Select Your Headshot")
    blank, file_type = os.path.splitext(selected_headshot_path)
    valid_types = [".jpg" , ".jpeg", ".png", ".bmp"]

    # check if user cancelled
    if not selected_headshot_path:
        return
    
    # check file is correct format
    if file_type.lower() not in valid_types:
        messagebox.showerror("Error: Invalid file type", "Please enter a valid image file (jpg, jpeg, png, bmp)")
        return
    
    print(f"Headshot selected: {selected_headshot_path}")


def getBackground(bg_file):
    global selected_background_path
    selected_background_path = f'./backgrounds/{bg_file}'
    print(f"Background selected: {bg_file}")
    processHeadshot()


def processHeadshot():
    # Loads user headshot image
    user_headshot = cv2.imread(selected_headshot_path)

    # convert file type to what mp needs
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, 
                        data=user_headshot)

    # segment the image
    segmentation_res = segmenter.segment(mp_image)
    mask = segmentation_res.category_mask
    mask_array = mask.numpy_view()
    fixed_mask = (mask_array > 0).astype(np.uint8)

    # shrink mask to remove white edges
    kernel = np.ones((5, 5), np.uint8)
    fixed_mask = cv2.erode(fixed_mask, kernel, iterations=5)
    fixed_mask = np.expand_dims(fixed_mask, axis=2) # fix resizing issue

    # remove the background by applying the mask to the image
    just_person = user_headshot * fixed_mask

    # load a background image and resize to fit
    backgroundImage = cv2.imread(selected_background_path)
    height, width = user_headshot.shape[:2]
    resize_background = cv2.resize(backgroundImage, (width, height))


    # overlay the new background with the person 
    invert_mask = 1 - fixed_mask
    final_headshot = (just_person) + (invert_mask * resize_background)

    # save new image
    cv2.imwrite('./outputs/final_result.png', final_headshot)
    print("Final Result Saved!")

root = tk.Tk()
root.title("Headshot Background Replacer")
root.geometry("400x400")

# upload heashot button
uploadbtn = tk.Button(root,
                      text="Upload Headshot",
                      command=getHeadshot,
                      width=30, height=2)
uploadbtn.pack(pady=20)

# label
tk.Label(root, text="Select Background:").pack(pady=10)

# background buttons
backgrounds_folder = './backgrounds'
background_files = os.listdir(backgrounds_folder)

for bg_file in background_files:
    btn = tk.Button(root,
                    text=bg_file,
                    command=lambda bg=bg_file: getBackground(bg),
                    width=30)
    btn.pack(pady=5)

root.mainloop()