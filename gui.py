
import keyboard

while True:
    if keyboard.is_pressed('left arrow'):
        print("Left arrow key is pressed")
        break
    elif keyboard.is_pressed('right arrow'):
        print("Right arrow key is pressed")
        break
