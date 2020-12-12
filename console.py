class Animation:

    FRAMES = [
        '.  ',
        '.. ',
        '...',
    ]

    def __init__(self):

        self.counter = 0
        self.index = 0
        
    @property
    def frame(self):

        return self.FRAMES[self.index]
        
    def tick(self):

        self.counter += 1

    def reset(self): 
        
        self.counter = 0
        
        if self.index < len(self.FRAMES) - 1:
            self.index += 1
        else:
            self.index = 0