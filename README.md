# Number Guesser

Number Guesser is an simple app that enables you draw whatever you want.

You can paint with different colors on black or white background.

Program has access to the keras model that was trained to guess numbers from 0-9. 
If you want you can modify the model and train it using custom dataset.

Predicted number will be shown in console log.

## User guide:

Create new canvas:
- LCTRL + 1 > black background
- LCTRL + 2 > white background

Set pen color:
- q > black
- w > white
- r > red
- g > green
- b > blue

Set pen or rubber thickness:
- LCTRL + SCROLL_UP   ↑
- LCTRL + SCROLL_DOWN ↓ 

Modes:
- LEFT_MOUSE_BUTTON  > pen
- RIGHT_MOUSE_BUTTON > rubber

Press ENTER to guess number.

## Dependencies:

- numpy 1.19
- pygame 1.9.6
- tensorflow 2.0.0
- opencv-python 4.2.0.34
