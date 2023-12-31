# -*- coding: utf-8 -*-
"""Hard-hat detection

Dataset source: https://universe.roboflow.com/joseph-nelson/hard-hat-workers/dataset/13

Original file is located at
    https://colab.research.google.com/drive/1xcrXVvfjoJ3w3FFcPtg8hDlMIKwNW0YW
"""

!pip install ultralytics

!pip install roboflow

import numpy as np
import pandas as pd
import warnings
import matplotlib.pyplot as plt
from IPython.core.magic import register_line_cell_magic
import yaml
from PIL import Image
import os
import seaborn as sns
from ultralytics import YOLO
from matplotlib.patches import Rectangle
import glob
import cv2

from roboflow import Roboflow
rf = Roboflow(api_key="1Xgfzhg850TcqfnPxclJ")
project = rf.workspace("joseph-nelson").project("hard-hat-workers")
dataset = project.version(13).download("yolov8")

model = YOLO('yolov8n.pt')

model.train(data='/content/Hard-Hat-Workers-13/data.yaml',
task='detect',
imgsz=640,
epochs=3,
batch=8,
mode='train',
name='yolov8n_v1_train')

#selecting best model
model = YOLO('/content/runs/detect/yolov8n_v1_train2/weights/best.pt')

# Load the validation data configuration
data_config = '/content/Hard-Hat-Workers-13/data.yaml'  # Provide the path to your validation data.yaml file

# Perform validation
results = model.val(data=data_config)

# Load the YOLO model for predictions
model = YOLO('/content/runs/detect/yolov8n_v1_train2/weights/best.pt')

# Load the test data configuration
test_data_config = '/content/Hard-Hat-Workers-13/data.yaml'  # Provide the path to your test data.yaml file

results = model.predict(source="/content/Hard-Hat-Workers-13/test/images", save=True)

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline

predicitions = glob.glob(os.path.join("/content/runs/detect/predict", '*'))

n = 10

for i in range(n):
    idx = np.random.randint(0, len(predicitions))
    image = Image.open(predicitions[idx])
    plt.imshow(image)
    plt.grid(False)
    plt.show()

