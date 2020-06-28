import numpy as np

from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import load_model 
from tensorflow.keras.utils import to_categorical

from data import X_test, y_test

model = load_model('model.h5')
loss, acc = model.evaluate(X_test, y_test, verbose=0)

print(f'Model loss: {loss}')
print(f'Model acc: {acc}')