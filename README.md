# Number Guesser

Number Guesser is an simple app that enables you draw whatever you want.

Program has access to the keras model which has been trained to guess numbers from 0-9. 
If you want you can modify the model and train it using a custom dataset.

Run the program with the following command `py guesser.py`

Train and save the model with the following command `py train-model.py`

Run the test suite with the following command `py test-model.py`

## User guide:

### Change background color:
- `LCTRL` + `1` → black
- `LCTRL` + `2` → white
- `LCTRL` + `n` → new canvas

### Set pen color:
- `q` → black
- `w` → white
- `r` → red
- `g` → green
- `b` → blue

### Set pen or rubber thickness:
- `LCTRL` + `SCROLL_UP`   → increase up to 20
- `LCTRL` + `SCROLL_DOWN` → decrease down to 10

### Tools:
- `LEFT_MOUSE_BUTTON`  → pen
- `RIGHT_MOUSE_BUTTON` → rubber

Press `ENTER` to guess the number.

## Dependencies:

- numpy 1.19
- pygame 1.9.6
- tensorflow 2.0.0
- opencv-python 4.2.0.34
