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

from removebg import RemoveBg
from dotenv import load_dotenv

import requests

load_dotenv()

# load api key from .env
REMOVEBG_API_KEY = os.getenv('REMOVEBG_API_KEY')
rmbg = RemoveBg(REMOVEBG_API_KEY, error_log_file='errors.log')

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
    output_path = './outputs/no_bg.png'

    try:
        
        # call api using requests
        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': open(selected_headshot_path, 'rb')},
            data={'size': 'auto'},
            headers={'X-Api-Key': REMOVEBG_API_KEY},
        )
        
        print(f"API Response status: {response.status_code}")
        
        if response.status_code == 200:
            # save result
            with open(output_path, 'wb') as out:
                out.write(response.content)
            print(f"Background removed, saved to: {output_path}")
        else:
            raise Exception(f"API Error {response.status_code}: {response.text}")

        # load image
        person_rgba = cv2.imread(output_path, cv2.IMREAD_UNCHANGED)

        if person_rgba is None:
            raise Exception(f"Failed to load {output_path}")
        
        # load and resize background
        background = cv2.imread(selected_background_path)
        height, width = person_rgba.shape[:2]
        background_resized = cv2.resize(background, (width, height))

        if person_rgba.shape[2] == 4:
            bgr = person_rgba[:, :, :3]
            alpha = person_rgba[:, :, 3:] / 255.0
            final = (bgr * alpha + background_resized * (1 - alpha)).astype(np.uint8)
        else:
            final = person_rgba
        
        # save new image
        cv2.imwrite('./outputs/final_result.png', final)
        messagebox.showinfo("Success", "Background replaced!")
        print("Final Result Saved!")

    except Exception as e:
        messagebox.showerror("Error", f"Failed: {str(e)}")
        print(f"Error details: {e}")
    

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