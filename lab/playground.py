#%% Modules:
import cv2
import requests
import numpy as np
import matplotlib.pyplot as plt

from tensorflow.keras.utils import to_categorical
from tensorflow.keras.datasets import mnist
from tensorflow.keras import Model
from PIL import Image

from utils import InputProfile, History
from models.convolutional import LeNet
from models.standard import DNN

#%% Loading a train and test data:
(X_train, y_train), (X_test, y_test) = mnist.load_data()

assert(X_train.shape[0] == y_train.shape[0]), 'The number of images is not equal to the number of labels'
assert(X_test.shape[0] == y_test.shape[0]), 'The number of images is not equal to the number of labels'
assert(X_train.shape[1:] == (28, 28)), 'The dimensions of the images are not 28x28'
assert(X_test.shape[1:] == (28, 28)), 'The dimensions of the images are not 28x28'

#%% Preprocessing of input:
def preprocess(X, y):
    X = X / 255
    y = to_categorical(y, 10)
    return X, y

X_train, y_train = preprocess(X_train, y_train)
X_test, y_test = preprocess(X_test, y_test)

profile_figure = InputProfile(X_train, y_train)
profile_figure.show()

#%% Creating the standard model based on a deep neural network:
model = DNN()
model.create()
model.train(X_train, y_train)
model.test(X_test, y_test)

h_figure = History(model.history)
h_figure.show()

#%% Creating the leNet model based on a convolutional deep neural network:
leNet = LeNet()
leNet.create()
leNet.train(X_train, y_train)
leNet.test(X_test, y_test)

h_figure = History(leNet.history)
h_figure.show()

#%% Loading a custom image:
url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcSQVE6SuSxz_RW3YCd0ea7kUk5nDUuK139vop2RnaJd_D2Bwdpa&usqp=CAU'
response = requests.get(url, stream=True)
img = Image.open(response.raw)
img_array = np.asarray(img)
resized = cv2.resize(img_array, (28, 28))
gray_scale = cv2.cvtColor(resized, cv2.COLOR_RGB2GRAY)
image = cv2.bitwise_not(gray_scale)
image = image.reshape(1, *image.shape)
image = image / 255 

plt.figure('Input')
plt.imshow(img)
plt.axis('off')

#%% The standard model prediction:
prediction = model.predict(image)
print(f'Predicted number: {prediction}')

#%% The leNet model prediction:
prediction = leNet.predict(image)
print(f'Predicted number: {prediction}')

#%% Extracting filters from convolutional layers:
layer1 = Model(
    inputs=leNet.model.layers[0].input, 
    outputs=leNet.model.layers[0].output
)
layer2 = Model(
    inputs=leNet.model.layers[0].input, 
    outputs=leNet.model.layers[2].output
)

visual_layer1, visual_layer2 = layer1.predict(image), layer2.predict(image)

plt.figure(figsize=(10,6))
for i in range(30):
    plt.subplot(6, 5, i+1)
    plt.imshow(visual_layer1[0, :, :, i], cmap=plt.get_cmap('jet'))
    plt.axis('off')

plt.figure(figsize=(10,6))
for i in range(15):
    plt.subplot(3, 5, i+1)
    plt.imshow(visual_layer2[0, :, :, i], cmap=plt.get_cmap('jet'))
    plt.axis('off')

#%%