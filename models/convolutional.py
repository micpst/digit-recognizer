from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout

class LeNet:
    input_shape = (28, 28, 1)

    def __init__(self): 
        self.model = Sequential()
        self.model.add(Conv2D(filters=30, kernel_size=(5, 5), activation='relu', input_shape=self.input_shape))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        
        self.model.add(Conv2D(filters=15, kernel_size=(3, 3), activation='relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        
        self.model.add(Flatten())
        self.model.add(Dense(units=500, activation='relu'))
        self.model.add(Dropout(rate=.2))
        self.model.add(Dense(units=10, activation='softmax'))
   
    def create(self, lr=.01):
        self.model.compile(Adam(lr), loss='categorical_crossentropy', metrics=['accuracy'])
        self.model.summary()

    def inputDataAdjustment(self, X): return X.reshape(X.shape[0], *self.input_shape)

    def train(self, X_train, y_train, epochs=4):
        X_train = self.inputDataAdjustment(X_train)
        self.history = self.model.fit(X_train, y_train, validation_split=0.1, epochs=epochs, batch_size=400, verbose=1, shuffle=1)

    def test(self, X_test, y_test):
        X_test = self.inputDataAdjustment(X_test)
        self.score = self.model.evaluate(X_test, y_test, verbose=0)

    def predict(self, X):
        X = self.inputDataAdjustment(X)
        return self.model.predict_classes(X)
