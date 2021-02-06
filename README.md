# Number Guesser

Draw a number and see if machine can guess it.

Program has access to the keras model which has been trained to guess numbers from 0-9. 
If you want you can modify the model and train it using a custom dataset.

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
# default setup:
py guesser.py 

# custom setup:
py guesser.py my_model.h5
```

## User guide:

### Change background color:
- `1` → black
- `2` → white
- `n` → new canvas

### Set pen color:
- `q` → black
- `w` → white
- `r` → red
- `g` → green
- `b` → blue

### Set pen or rubber thickness:
- `SCROLL_UP`   → increase up to 20
- `SCROLL_DOWN` → decrease down to 10

### Tools:
- `LEFT_MOUSE_BUTTON`  → pen
- `RIGHT_MOUSE_BUTTON` → rubber

Press `ENTER` to guess the number.

## Dependencies:

- numpy 1.19.5
- pygame 2.0.1
- pandas 1.2.1
- pillow 8.1.0
- tensorflow 2.4.1
- matplotlib 3.3.4
- opencv-python 4.5.1.48

## License
All my code is MIT licensed. Libraries follow their respective licenses.