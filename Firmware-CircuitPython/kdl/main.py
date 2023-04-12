import keyboard
import kdl

# Driver code to test interpreter on numpad.
interpreter = kdl.kdl_interpreter([3,3,3], "test.kdl")
table = {'7':(0,0), '8':(0,1), '9':(0,2), '4':(1,0), '5':(1,1), '6':(1,2), '1':(2,0), '2':(2,1), '3':(2,2)}

def print_keys(interpreter):
    print()
    print("+-------+")
    print(f"|State:{interpreter.state}|")
    print("+"+("---+"*len(interpreter.is_pressed)))
    for i in range(len(interpreter.is_pressed)):
        print('|',end=' ')
        for j in range(len(interpreter.is_pressed[i])):
            print('1' if interpreter.is_pressed[i][j] else '0',end=' | ')
        print("\n+"+("---+"*len(interpreter.is_pressed)))

def key_pressed(e):
    if not e.name in list(table.keys()): return
    if e.event_type == 'up':
        print(interpreter.key_released(*table.get(e.name)))
    elif e.event_type == 'down':
        print(interpreter.key_pressed (*table.get(e.name)))
    #print_keys(interpreter)

if __name__ == "__main__":

    keyboard.hook(key_pressed)

    while True:
        pass
    interpreter = kdl.kdl_interpreter([2,2], "test.kdl")
    print_keys(interpreter)