import pyautogui
import time
import keyboard  # Import the keyboard module

"""time.sleep(5)
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
    pyautogui.keyUp('s')123456

   

    # Press D
    pyautogui.keyDown('d')
    time.sleep(1)
    pyautogui.keyUp('d')
    
    # Check if 'q' is pressed to stop the loop
    if keyboard.is_pressed('q'):
        run = False"""
with open("10-million-password-list-top-1000000.txt", "r" ) as passwords:
    passwords = passwords.readlines()

tim = time.gmtime()
print(tim.tm_min , ":" , tim.tm_sec)
for password in passwords[:100]:
   pyautogui.typewrite(password)
   pyautogui.keyDown("\n")

tim = time.gmtime()
print(tim.tm_min , ":" , tim.tm_sec)

