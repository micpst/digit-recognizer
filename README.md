# Number Guesser

Draw a number and see if machine can guess it.

Program has access to the keras model which has been trained to guess numbers from 0-9. 
If you want you can modify the model and train it using a custom dataset.

Currently, it is recommended to use default model name - model.h5 as the guesser app does not support custom names unless you change it manually in the code :)

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

### Run the guesser
```
py guesser.py 
```

## Dependencies:

- numpy 1.19.5
- pandas 1.2.1
- pillow 8.1.0
- tensorflow 2.4.1
- matplotlib 3.3.4
- opencv-python 4.5.1.48

## License
All my code is MIT licensed. Libraries follow their respective licenses.