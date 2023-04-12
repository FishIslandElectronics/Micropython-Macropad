from time import sleep

import digitalio, busio, board, usb_hid
import adafruit_ssd1306

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode


i2c = busio.I2C(scl=board.GP1, sda=board.GP0) # This RPi Pico way to call I2C
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
display.fill(1)
display.show()

keyboard = Keyboard(usb_hid.devices)

btn1 = digitalio.DigitalInOut(board.GP10)
btn1.direction = digitalio.Direction.INPUT
btn1.pull = digitalio.Pull.DOWN

btn2 = digitalio.DigitalInOut(board.GP11)
btn2.direction = digitalio.Direction.INPUT
btn2.pull = digitalio.Pull.DOWN

btn3 = digitalio.DigitalInOut(board.GP12)
btn3.direction = digitalio.Direction.INPUT
btn3.pull = digitalio.Pull.DOWN

btn4 = digitalio.DigitalInOut(board.GP13)
btn4.direction = digitalio.Direction.INPUT
btn4.pull = digitalio.Pull.DOWN

btn5 = digitalio.DigitalInOut(board.GP14)
btn5.direction = digitalio.Direction.INPUT
btn5.pull = digitalio.Pull.DOWN

btn6 = digitalio.DigitalInOut(board.GP15)
btn6.direction = digitalio.Direction.INPUT
btn6.pull = digitalio.Pull.DOWN

while True:
    if btn1.value:
        keyboard.press(Keycode.SHIFT, Keycode.GUI, Keycode.THREE)
        keyboard.release(Keycode.SHIFT, Keycode.GUI, Keycode.THREE)
        print("screen shotted")
        sleep(.02)
        
    if btn2.value:
        keyboard.press(Keycode.H)
        keyboard.release(Keycode.H)
        keyboard.press(Keycode.I)
        keyboard.release(Keycode.I)
        print("hi")
        sleep(.02) 
    
    if btn3.value:
        keyboard.press(Keycode.SHIFT, Keycode.GUI, Keycode.FOUR)
        keyboard.release(Keycode.SHIFT, Keycode.GUI, Keycode.FOUR)
        print("screen shotted selective")
        sleep(.02)
    
    if btn4.value:
        keyboard.press(Keycode.CONTROL, Keycode.TAB)
        keyboard.release(Keycode.CONTROL, Keycode.TAB)
        print("tab switch right")
        sleep(.02)
    
    if btn5.value:
        keyboard.press(Keycode.SHIFT, Keycode.CONTROL, Keycode.TAB)
        keyboard.release(Keycode.SHIFT, Keycode.CONTROL, Keycode.TAB)
        print("tab switch left")
        sleep(.02)
    
    if btn6.value:
        keyboard.press(Keycode.GUI, Keycode.N)
        keyboard.release(Keycode.GUI, Keycode.N)
        print("new tab")
        sleep(.02)
    
    sleep(.1)
