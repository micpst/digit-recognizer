import cv2
import numpy as np

from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout

from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical

def create_model():
    model = Sequential()
    
    model.add(Conv2D(filters=30, kernel_size=(5, 5), activation='relu', input_shape=(28, 28, 1)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    
    model.add(Conv2D(filters=15, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    
    model.add(Flatten())
    model.add(Dense(units=500, activation='relu'))
    model.add(Dropout(rate=.2))
    model.add(Dense(units=10, activation='softmax'))

    model.compile(Adam(lr=.01), loss='categorical_crossentropy', metrics=['accuracy'])
    return model

def preprocess(X, y):
    X = X.reshape(X.shape[0], 28, 28, 1)
    X = X / 255
    y = to_categorical(y, 10)
    return X, y

(X_train, y_train), _ = mnist.load_data()

assert(X_train.shape[0] == y_train.shape[0]), 'The number of images is not equal to the number of labels'
assert(X_train.shape[1:] == (28, 28)), 'The dimensions of the images are not 28x28'

X_train, y_train = preprocess(X_train, y_train)

model = create_model()
model.fit(X_train, y_train, validation_split=0.1, epochs=5, batch_size=400, verbose=1, shuffle=1)
model.save('model.h5')