from time import sleep
import kdl, pbm_codec

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
pixels = neopixel.NeoPixel(board.GP14, 12, brightness = 1.0)
display.text("Sus", 0,0,1)
display.show()

keyboard = Keyboard(usb_hid.devices)

pins = [board.GP2, board.GP3, board.GP4, board.GP5, board.GP6, board.GP7, board.GP8, board.GP9, board.GP10, board.GP11, board.GP12, board.GP13]
btns = [digitalio.DigitalInOut(pin) for pin in pins]

for btn in btns:
    btn.direction = digitalio.Direction.INPUT 
    btn.pull = digitalio.Pull.UP

display.fill(0)
display.text(f"{len(btns)} {len(pixels)}", 0,0,1)
display.show()

macro_pad_size = [4,4,4]

i_to_row_col = [(i%3, (i//3)) for i in range(sum(macro_pad_size))]

interpreter = kdl.kdl_interpreter([4,4,4], "test.kdl")

for i in range(len(pixels)):
    if interpreter.get_lit(*i_to_row_col[i]): pixels[i] = interpreter.get_color(*i_to_row_col[i])
    else: pixels[i] = (0,0,0)


#pbm_codec.draw_pbm(display, "img.pbm", 0, 0)
display.show()

prev_state = [False for i in range(len(btns))]
layer_change = False
led_updated = False
while True:
    #display.fill(0)
    #isplay.text(f"C:{interpreter.get_lit(*i_to_row_col[0])}", 20,0,1)
    #display.text(f"S:{interpreter.state}", 0,0,1)
    #display.show()
    i = 0
    while i < len(pixels):
        value = not btns[i].value
        if not prev_state[i] == value:
            #print("KEY UPDATE!")
            row_col = i_to_row_col[i]
            prev_state[i] = value

            if value:
                # Return list of commands to be run by keyboard
                layer_change, led_updated, display_command, press_sequence, type_str, errors = interpreter.key_pressed(*row_col)
            else:
                layer_change, led_updated, display_command, press_sequence, type_str, errors = interpreter.key_released(*row_col)

            if led_updated: pixels[i] = interpreter.get_color(*i_to_row_col[i])

            if layer_change:
                j = 0
                while j < len(pixels):
                    pixels[j] = interpreter.get_color(*i_to_row_col[j])
                    j += 1
                layer_change = False

            if not press_sequence == []:
                for seq in press_sequence:
                    if seq[0] == "press":
                        keyboard.send(*seq[1])
                    elif seq[0] == "type":
                        for key in seq[1]:
                            keyboard.send(key)
                    elif seq[0] == "wait":
                        sleep(seq[1])

            while not display_command == []:
                command = display_command.pop(0)
                #print (command)
                if command == "clear":
                    #print("Command -> clear")
                    display.fill(0) # TODO: handle background stuff
                    display.show()
                elif command[0] == "write":
                    #print("write")
                    _, x, y, msg = command
                    display.text(msg, x, y, 1)
                    display.show()

                

        i += 1

    #print(list(map(lambda x : x.value, btns)))

"""
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
    display.fill(0)
    display.text(f"{btn6.value}", 0,0,1)
    display.show()
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

"""
