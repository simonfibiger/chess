import pyautogui
import time
import keyboard  # Import the keyboard module

time.sleep(5)
run = True

while run:
    # Press W and A together
    pyautogui.keyDown('w')
    pyautogui.keyDown('a')
    time.sleep(1)
    pyautogui.keyUp('w')
    pyautogui.keyUp('a')

    # Press S
    pyautogui.keyDown('s')
    time.sleep(1)
    pyautogui.keyUp('s')

    # Press D
    pyautogui.keyDown('d')
    time.sleep(1)
    pyautogui.keyUp('d')
    
    # Check if 'q' is pressed to stop the loop
    if keyboard.is_pressed('q'):
        run = False
