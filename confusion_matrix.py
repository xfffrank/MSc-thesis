# -*- coding: utf-8 -*-
"""confusion matrix.ipynb

Automatically generated by Colaboratory.

"""

"""
Create confusion matrices for the result of classification.
"""

import cv2
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy import ndimage
import time

import keras
from keras.layers import Dense,GlobalAveragePooling2D
from keras.applications import ResNet50, InceptionV3, inception_v3, resnet50, mobilenet_v2, MobileNetV2
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Model
from keras.optimizers import Adam, RMSprop
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint
from keras.models import load_model
from keras import backend as K

from sklearn.metrics import classification_report, confusion_matrix

import random
import cv2
import tensorflow as tf
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.image as mpimg

# from google.colab import drive
# drive.mount('/content/drive')

def get_img_generators(test_path, preprocess_input, batch_sz=32, target_sz=(256, 256)):
    print('target shape:', target_sz)
    print('batch size:', batch_sz)
    height, width = target_sz
    test_gen = ImageDataGenerator(preprocessing_function=preprocess_input)

    test_generator = test_gen.flow_from_directory(test_path,
                                                   target_size=(height, width),
                                                   color_mode='rgb',
                                                   class_mode='categorical',
                                                   batch_size=batch_sz,
                                                   shuffle=False)
    return test_generator


def plot_confusion_matrix(y_true, y_pred, classes,
                          normalize=False,
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    mpl.rcParams["font.size"] = 18

    plt.rcParams['xtick.labelsize']=16
    plt.rcParams['ytick.labelsize']=16
    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    # Only use the labels that appear in the data
    # classes = classes[unique_labels(y_true, y_pred)]
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    fig, ax = plt.subplots(figsize=(8,8))
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes)
    
    plt.xlabel('True classes', fontsize=16)
    plt.ylabel('Predicted classes', fontsize=16)

    # Rotate the tick labels and set their alignment.
    # plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
    #          rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    return ax

plot_confusion_matrix(test_generator.classes, y_preds, ['Whole food', 'Refined food'], normalize=True)

"""## Food/Non-food"""

filepath="drive/My Drive/MSc dataset/food5k/Food-5K/models/resnet50_last_6_256.best.hdf5"
food_model = load_model(filepath)

test_path = "drive/My Drive/MSc dataset/food5k/Food-5K/evaluation"
test_generator = get_img_generators(test_path, resnet50.preprocess_input)

test_generator.class_indices

y_preds = np.load('drive/My Drive/MSc dataset/food5k/Food-5K/best_predictions.npy')

"""## Whole/Refined Food"""

filepath="drive/My Drive/MSc dataset/food11/models/resnet50_last_6_undersampling.best.hdf5"
model = load_model(filepath)

test_path = "drive/My Drive/MSc dataset/food11-balanced-undersample/evaluation"
test_generator = get_img_generators(test_path, resnet50.preprocess_input)

y_preds = np.load('drive/My Drive/MSc dataset/food11/best_predictions.npy')

"""## Visualisation && Save results"""

test_generator.class_indices

TP_index = [] 
TN_index = []
FP_index = []
FN_index = []
# {'food': 0, 'non-food': 1}
# {'refined food': 0, 'whole food': 1}

for i, pred in enumerate(y_preds):
    if pred == 1 and test_generator.classes[i] == 1:
        TP_index.append(test_generator.filenames[i])
    elif pred == 1 and test_generator.classes[i] == 0:
        FP_index.append(test_generator.filenames[i])
    elif pred == 0 and test_generator.classes[i] == 0:
        TN_index.append(test_generator.filenames[i])
    elif pred == 0 and test_generator.classes[i] == 1:
        FN_index.append(test_generator.filenames[i])

# shuffle lists
from random import shuffle

shuffle(TP_index)
shuffle(TN_index)
shuffle(FP_index)
shuffle(FN_index)

# Get image subsets of TP, TN, FP, FN

print(TP_index[0:10])
print(TN_index[0:10])
print(FP_index[0:10])
print(FN_index[0:10])

def save_img(img_path, filename):
    img = mpimg.imread(img_path)
    plt.axis('off')
    plt.imshow(img)
    plt.savefig(filename, bbox_inches='tight')
    #plt.show()

# save images
for i in range(5):
    img_path = 'drive/My Drive/MSc dataset/food11-balanced-undersample/evaluation/' + FP_index[i]
    #img_path = "drive/My Drive/MSc dataset/food5k/Food-5K/evaluation/" + FP_index[i]
    save_img(img_path, str(i))