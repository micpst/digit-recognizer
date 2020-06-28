import cv2
import numpy as np

from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout

from data import X_train, y_train

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

model = create_model()
model.fit(X_train, y_train, validation_split=0.1, epochs=5, batch_size=400, verbose=1, shuffle=1)
model.save('model.h5')