from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Sequential

class DNN:
    input_dim = 784

    def __init__(self):
        self.model = Sequential()
        self.model.add(Dense(units=10, activation='relu', input_dim=self.input_dim))
        self.model.add(Dense(units=10, activation='relu'))
        self.model.add(Dense(units=10, activation='softmax'))
        
    def create(self, lr=.01):
        self.model.compile(Adam(lr), loss='categorical_crossentropy', metrics=['accuracy'])
        self.model.summary()

    def inputDataAdjustment(self, X):
        return X.reshape(X.shape[0], self.input_dim)

    def train(self, X_train, y_train, epochs=5):
        X_train = self.inputDataAdjustment(X_train)
        self.history = self.model.fit(X_train, y_train, validation_split=0.1, epochs=epochs, batch_size=200, verbose=1, shuffle=1)

    def test(self, X_test, y_test):
        X_test = self.inputDataAdjustment(X_test)
        self.score = self.model.evaluate(X_test, y_test, verbose=0)

    def predict(self, X):
        X = self.inputDataAdjustment(X)
        return self.model.predict_classes(X)
