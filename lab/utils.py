import random
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

class InputProfile:
    def __init__(self, X, y, data):
        self.X = X
        self.y = y
        self.data = data
        self.figure = plt.figure('Input profile', figsize=(20, 10))      
        self.grid = GridSpec(10, 19, figure=self.figure, hspace=.6)

    def show(self):
        n_samples = []
        
        for i in range(5):
            for j in range(10):
                x_selected = self.X[self.y == j]
                ax_input = self.figure.add_subplot(self.grid[j, i])
                ax_input.imshow(x_selected[random.randint(0, len(x_selected - 1)), :, :])
                ax_input.axis('off')
                if i == 2:
                    ax_input.set_title(str(j))
                    n_samples.append(len(x_selected))

        ax_dist = self.figure.add_subplot(self.grid[0:4, 6:])
        ax_dist.bar(range(0, 10), n_samples)
        ax_dist.set_title('Distribution of training dataset')
        ax_dist.set_xlabel('Class number')
        ax_dist.set_ylabel('Number of images')

class History:
    def __init__(self, h):
        self.history = h.history
        self.figure = plt.figure('History', figsize=(15, 5))

    def show(self):
        ax_loss = self.figure.add_subplot(1, 2, 1)
        ax_loss.plot(self.history['loss'])
        ax_loss.plot(self.history['val_loss'])
        ax_loss.legend(['loss', 'val_loss'])
        ax_loss.set_title('Loss')
        ax_loss.set_xlabel('epoch')

        ax_acc = self.figure.add_subplot(1, 2, 2)    
        ax_acc.plot(self.history['accuracy'])
        ax_acc.plot(self.history['val_accuracy'])
        ax_acc.legend(['acc', 'val_acc'])
        ax_acc.set_title('Accuracy')
        ax_acc.set_xlabel('epoch')