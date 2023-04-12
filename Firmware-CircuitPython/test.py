import keyboard

btns = [True for i in range(10)]

prev_state = [True for btn in btns]

table = {'7':0, '8':1, '9':2, '4':3, '5':4, '6':5, '1':6, '2':7, '3':8}

def a():
    for i in range(len(btns)):
        value = btns[i]
        if not prev_state[i] == value:
            print("TRIGGER")
            prev_state[i] = value

def key_pressed(e):
    if not e.name in list(table.keys()): return
    id = table.get(e.name)
    print(e.event_type)
    if e.event_type == 'up':
        btns[id] = True
        print(btns[id], prev_state[id])
    elif e.event_type == 'down':
        btns[id] = False
        print(btns[id], prev_state[id])
    print("bfr", btns[id], prev_state[id])
    a()
    print("aftr",btns[id], prev_state[id])
    #print(btns)
    #print_keys(interpreter)

if __name__ == "__main__":

    keyboard.hook(key_pressed)

    while True:
        pass