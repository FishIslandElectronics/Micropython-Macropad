from time import sleep

import digitalio, busio, board, usb_hid, neopixel
import adafruit_ssd1306
from random import randint

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

from analogio import AnalogIn

analog1_in = AnalogIn(board.A1)
analog2_in = AnalogIn(board.A2)
analog3_in = AnalogIn(board.A0)

def get_voltage(pin):
    return (pin.value * 3.3) / 65536

i2c = busio.I2C(scl=board.GP1, sda=board.GP0) # This RPi Pico way to call I2C
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
display.fill(0)
pixels = neopixel.NeoPixel(board.GP14, 12)
display.text("amogus", 0,0,1)
display.show()

keyboard = Keyboard(usb_hid.devices)

btn1 = digitalio.DigitalInOut(board.GP2)
btn1.direction = digitalio.Direction.INPUT
btn1.pull = digitalio.Pull.UP

btn2 = digitalio.DigitalInOut(board.GP3)
btn2.direction = digitalio.Direction.INPUT
btn2.pull = digitalio.Pull.UP

btn3 = digitalio.DigitalInOut(board.GP4)
btn3.direction = digitalio.Direction.INPUT
btn3.pull = digitalio.Pull.UP

btn4 = digitalio.DigitalInOut(board.GP5)
btn4.direction = digitalio.Direction.INPUT
btn4.pull = digitalio.Pull.UP

btn5 = digitalio.DigitalInOut(board.GP6)
btn5.direction = digitalio.Direction.INPUT
btn5.pull = digitalio.Pull.UP

btn6 = digitalio.DigitalInOut(board.GP7)
btn6.direction = digitalio.Direction.INPUT
btn6.pull = digitalio.Pull.UP

# GP8 to GP13 are all wired to buttons

for i in range(len(pixels)):
    pixels[i] = (randint(0,255),randint(0,255),randint(0,255))
       
while True:
    #[analog.value for analog in [analog1_in,analog2_in,analog3_in]]
    if not btn1.value:
        keyboard.press(Keycode.SHIFT, Keycode.GUI, Keycode.THREE)
        keyboard.release(Keycode.SHIFT, Keycode.GUI, Keycode.THREE)
        print("screen shotted")
        sleep(.02)
        	
    if not btn2.value:
        keyboard.press(Keycode.H)
        keyboard.release(Keycode.H)
        keyboard.press(Keycode.I)
        keyboard.release(Keycode.I)
        print("hi")
        sleep(.02)
    
    if not btn3.value:
        keyboard.press(Keycode.SHIFT, Keycode.GUI, Keycode.FOUR)
        keyboard.release(Keycode.SHIFT, Keycode.GUI, Keycode.FOUR)
        print("screen shotted selective")
        sleep(.02)
    
    if not btn4.value:
        keyboard.press(Keycode.CONTROL, Keycode.TAB)
        keyboard.release(Keycode.CONTROL, Keycode.TAB)
        print("tab switch right")
        sleep(.02)
    
    if not btn5.value:
        keyboard.press(Keycode.SHIFT, Keycode.CONTROL, Keycode.TAB)
        keyboard.release(Keycode.SHIFT, Keycode.CONTROL, Keycode.TAB)
        print("tab switch left")
        sleep(.02)
    
    if not btn6.value:
        keyboard.press(Keycode.GUI, Keycode.N)
        keyboard.release(Keycode.GUI, Keycode.N)
        print("new tab")
        sleep(.02)
    
    sleep(.1)
