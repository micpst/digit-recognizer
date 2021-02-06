import os
import cv2
import sys
import getopt
import numpy as np
import pandas as pd
import tensorflow as tf

from PIL import Image
from tensorflow.keras import models, Input
from tensorflow.keras import layers
from tensorflow.keras import optimizers

def load_data(path):
    X = np.array([]).reshape((0, 28, 28))
    y = np.array([])
    
    for root, dirs, files in os.walk(path):
        for file in files:
            if ".png" in file:
                img = Image.open(os.path.join(root, file))
                img = np.asarray(img)
                img = cv2.resize(img, (28, 28))
                img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                img = cv2.equalizeHist(img)
                img = img.reshape(1, *img.shape)
                X = np.vstack((X, img))

            elif ".csv" in file:
                data = pd.read_csv(os.path.join(root, file), names=["labels"])
                y = data["labels"].to_numpy()

    return X, y

def preprocess(X, y):  
    X = X.reshape(X.shape[0], 28, 28, 1)
    X = X / 255
    y = tf.keras.utils.to_categorical(y, 10)
    return X, y

def create_model():
    model = models.Sequential(
        [
            Input(shape=(28, 28, 1)),
            layers.Conv2D(30, kernel_size=(5, 5), activation='relu'),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Conv2D(15, kernel_size=(3, 3), activation='relu'),
            layers.MaxPooling2D(pool_size=(2, 2)), 
            layers.Flatten(),
            layers.Dense(500, activation='relu'),
            layers.Dropout(.2),
            layers.Dense(10, activation='softmax')
        ]
    )
    return model

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["name=", "dataset="])
    except getopt.error as err:
        sys.exit(2)

    name = "model.h5"
    root = ""

    for opt, val in opts:
        if opt == "--name": name = val
        elif opt == "--dataset": root = val

    X_train, y_train = load_data(root) if root else tf.keras.datasets.mnist.load_data()[0]
    X_train, y_train = preprocess(X_train, y_train)

    if X_train.shape[0] != y_train.shape[0]:
        print("The number of images is not equal to the number of labels")
        sys.exit(2)

    if X_train.shape[1:-1] != (28, 28):
        print("The dimensions of the images are not 28x28")
        sys.exit(2)

    model = create_model()
    model.compile(optimizers.Adam(lr=.01), loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(X_train, y_train, validation_split=.1, epochs=5, batch_size=400, verbose=1, shuffle=1)
    model.save(name)

    print(f"Model has been saved -> {name}")