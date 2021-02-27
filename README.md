# Digit Recognizer

Digit Recognizer is a basic painting application extended with graphs to observe model predictions and pre-processed inputs to better understand what is happening under the hood of handwritten digit processing.
There are also scripts to train and test a keras model with a mnist or custom dataset, so you don't have to build the entire model from scratch.
If you are more experienced, you can load a self-designed model, the h5 file with the weights saved is enough.

Hopefully this project will help you get started with AI and you will be better able to understand how the input selection affects the precision of the model and whole output.

The project is still in development, so new features will be coming soon.

## Quick start:

### Install requirements
```
pip install -r requirements.txt
```

### Train and save the model
```
# default setup:
py train-model.py

# custom setup:
py train-model.py --name=my_model.h5 --dataset=train_dataset_dir
```

### Run the test suite
```
# default setup:
py test-model.py

# custom setup:
py test-model.py --name=my_model.h5 --dataset=test_dataset_dir
```

### Run the recognizer
```
py recognizer.py 
```

## Dependencies:

- numpy 1.19.5
- pandas 1.2.1
- pillow 8.1.0
- tensorflow 2.4.1
- matplotlib 3.3.4

## License
All my code is MIT licensed. Libraries follow their respective licenses.