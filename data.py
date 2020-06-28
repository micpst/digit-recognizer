from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical

def preprocess(X, y):
    X = X.reshape(X.shape[0], 28, 28, 1)
    X = X / 255
    y = to_categorical(y, 10)
    return X, y

(X_train, y_train), (X_test, y_test) = mnist.load_data()

assert(X_train.shape[0] == y_train.shape[0]), 'The number of images is not equal to the number of labels'
assert(X_test.shape[0] == y_test.shape[0]), 'The number of images is not equal to the number of labels'
assert(X_train.shape[1:] == (28, 28)), 'The dimensions of the images are not 28x28'
assert(X_test.shape[1:] == (28, 28)), 'The dimensions of the images are not 28x28'

X_train, y_train = preprocess(X_train, y_train)
X_test, y_test = preprocess(X_test, y_test)