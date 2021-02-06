import os
import sys
import cv2
import time
import getopt
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt

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

def save_history(h, hdir):
    fig = plt.figure("History", figsize=(15, 5))
    fig.suptitle(f"Model: {h.model.name}\n Time: {time.ctime()}")
    fig.subplots_adjust(top=0.85)

    ax_loss = fig.add_subplot(1, 2, 1)
    ax_acc = fig.add_subplot(1, 2, 2)

    ax_loss.set_title("Loss")
    ax_loss.plot(h.history["loss"])
    ax_loss.plot(h.history["val_loss"])
    ax_loss.legend(["loss", "val_loss"])
    ax_loss.set_xlabel("epochs")
 
    ax_acc.set_title("Accuracy")
    ax_acc.plot(h.history["accuracy"])
    ax_acc.plot(h.history["val_accuracy"])
    ax_acc.legend(["acc", "val_acc"])
    ax_acc.set_xlabel("epochs")

    if not os.path.exists(hdir): 
        os.makedirs(hdir)

    path = os.path.join(hdir, f"{h.model.name}-{int(time.time())}.png")
    plt.savefig(path)
    print(f"Model history has been saved -> {path}")

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["name=", "dataset=", "hdir="])
    except getopt.error as err:
        sys.exit(2)

    name = "model.h5"
    hdir = "history"
    root = ""

    for opt, val in opts:
        if opt == "--name": name = val
        elif opt == "--hdir": hdir = val
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
    model._name = name

    model.compile(optimizers.Adam(lr=.01), loss='categorical_crossentropy', metrics=['accuracy'])
    h = model.fit(X_train, y_train, validation_split=.1, epochs=5, batch_size=400, verbose=1, shuffle=1)

    save_history(h, hdir)
    model.save(name)
    print(f"Model has been saved -> {name}")