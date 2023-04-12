from random import random

LETTERS = "abcdefghijklmnopqrstuvwxyz"
LETTERS_UPPER = LETTERS.upper()
NUMBERS = "0123456789"
NUMBERS_UPPER = "!@#$%^&*()"
OTHER_KEYS = {"ENTER": 0x28, "ESC": 0x29, "BACK": 0x2A, "TAB": 0x2B, "SPACE": 0x2C, " ": 0x2C, "CTRL": 0xE0, "ALT": 0xE2, "WIN": 0xE3, "CMD": 0xE3}

def decode_key(key):
    if key in LETTERS: # Lowercase letters keycodes start at 4 ('a') and go to 30 ('z')
        return [(ord(key)-ord('a'))+4]
    
    if key in LETTERS_UPPER: # Uppercase includes shift]
        return [(ord(key)-ord('A'))+4, 0xE1]
    
    if key in NUMBERS: # Numbers start at 0x1E, starting with 1
        return [(ord(key)-ord('1'))+0x1E]
    
    if key in NUMBERS_UPPER: # Similarly, these keys are numbers with the shift key held
        return [NUMBERS_UPPER.index(key)+0x1E, 0xE1]
    
    
    return [OTHER_KEYS.get(key, None)]

def is_numeric(string):
    for char in string:
        if char not in NUMBERS:
            return False
    return True

class key():
    def __init__(self, state, attributes = []):
        self.color = (0,0,0)
        self.lit = False
        self.state = state
        self.lit_on_reset = False

        actions = []

        # Get static properties from the list
        # TODO: make press ["press", [...list of buttons and key names...]]
        # TODO: diplay commands. Clear, print, draw (image)
        # TODO: make type ["type", "one single string"]   make string using ' '.join()

        for i in range(len(attributes)):
            action = attributes[i]

            if action[0] == "color":
                if action[1] == "random":
                    self.color = (int(random()*255), int(random()*255), int(random()*255))
                    continue
                self.color = tuple(map(int,action[1:]))

            elif action[0] == "press":
                converted_keys = []
                for key in action:
                    print(key)
                    if key != "press": converted_keys += decode_key(key)
                print(converted_keys)
                actions.append(("press", converted_keys))

            elif action[0] == "type":
                converted_keys = []
                for key in ' '.join(action[1:]):
                    converted_keys += decode_key(key)
                actions.append(("type", converted_keys))

            elif action[0] == "on":
                if action[1] == "always":
                    self.lit = True
                    self.lit_on_reset = True
                elif action[1] == "never":
                    self.lit = False
                    self.lit_on_reset = False
                else:
                    actions.append((action[0], action[1:]))

            else:
                # And add actions to the dictionary of actions
                actions.append((action[0], action[1:]))

        self.actions = actions

    def get_color(self): 
        return self.color if self.lit else (0,0,0)

    def get_lit(self): 
        return self.lit

    def pressed(self):
        led_update = False
        #print(f"Pressed! {self.actions}")
        state = self.state
        display_command = []
        press_sequence = []
        type_str = ""
        errors = []

        for action, args in self.actions:
            #print(action)
            # Handle the 'on' lighting action
            if action == "on":
                if args[0] == "pressed":
                    self.lit = True
                    led_update = True

            # Press keys sequentially, used for shortcuts
            if action == "press":
                press_list = []
                for key in args:
                    press_list.append(key)
                press_sequence.append(("press", press_list))

            # Type is one long string of chars to type
            if action == "type":
                press_sequence.append(("type", args))

            if action == "wait":
                press_sequence.append(("wait", float(args[0])))

            # Handle the setstate actions. --ALWAYS DO LAST--
            if action == "setstate":
                #print(int(args[0]))
                state = int(args[0])


            

            # Return the current state for no state change
        return (state, led_update, display_command, press_sequence, type_str, errors)

    def reset(self):
        self.lit = self.lit_on_reset

    def released(self):
        led_update = False
        display_command = []
        press_sequence = []
        type_str = ""
        errors = []
        for action, args in self.actions:
            # Handle the 'on' lighting action
            if action == "on":
                if args[0] == "pressed":
                    self.lit = False
                    led_update = True

            if action == "display":
                if args[0] == "clear":
                    display_command.append(("clear"))
                elif args[0] == "text":
                    display_command.append(("write", int(args[1]), int(args[2]), ' '.join(args[3:])))

        return (self.state, led_update, display_command, press_sequence, type_str, errors)     

    def __str__(self):
        return f"Key Color:{self.color} Lit:{self.lit} Actions:{self.actions}"


class kdl_interpreter():
    # TODO: Provide pointers to be called for each action. Example, lit would call 
    # keyboard_manager_pointer.lighting_on(row, col)
    def __init__(self, sizes, source_file):
        """Takes in a 1D array of sizes containing the columns for a given row. The number of rows is the length
        of the list. Also takes in a path to a kdl source file to parse"""

        self.is_pressed = [[False for _ in range(i)] for i in sizes]
        self.states = []
        self.backgrounds = []
        self.sizes = sizes
        self.state = 0
        self.state_semaphore = False
        self.changed_state = False

        keywords = ["key", "setstate", "on", "color", "press", "type", "display", "wait"]

        with open(source_file, 'r') as file:
            # Track currently being assembled state and its number
            current_state_num = None
            current_state = [[None for _ in range(i)] for i in sizes]

            # Parse file line by line
            for line in file:
                # Split lines by spaces, makes them lowercase and removes whitespace
                tokens = list(map( lambda x : x.strip(), list(line.split(' '))))

                if tokens[0].lower() == "state":
                    if not is_numeric(tokens[1]): 
                        print(f"NOT NUMERIC: |{tokens[1]}|")
                        return

                    #print(f"state: {tokens[1]}")
                    if not current_state_num == None: 
                        self.states.append(current_state)
                        current_state = [[None for _ in range(i)] for i in sizes]

                    current_state_num = int(tokens[1])
                    
                elif tokens[0].lower() == "key":
                    if tokens[1].endswith(':') and ',' in tokens[1]:
                        # Transform x,y: to row, column tuple
                        row, column = map(int, map(lambda x : x.split(':')[0], tokens[1].split(',')))
                        print(f"{row},{column}")

                    actions = []
                    for i in range(2, len(tokens)):
                        # Handle comments
                        if tokens[i] == '//': break

                        if tokens[i] in keywords:
                            print(tokens[i])
                            actions.append([tokens[i]])
                        else:
                            actions[-1].append(tokens[i].split(',')[0])
                    current_state[row][column] = key(current_state_num, attributes=actions)

            # Append final state at the end
            self.states.append(current_state)

    def key_pressed(self, row, column):
        """Marks a given key as released and returns a tuple of actions, formatted (changed_state, led_update, display_command, press_sequence, type_str, errors)"""
        # press_sequence is sequence of key codes held until the last one is pressed
        # type_str is a sting to be pressed one key at a time
        new_state, led_update, display_command, press_sequence, type_str, errors = self.states[self.state][row][column].pressed()
        changed_state = not new_state == self.state
        self.state = new_state

        columns = len(self.states[self.state][0])
        rows = len(self.states[self.state])

        if changed_state:
            [self.states[self.state][ro][col].reset() for col in range(columns) for ro in range(rows)]

        return (changed_state, led_update, display_command, press_sequence, type_str, errors)

    def key_released(self, row, column):
        """Marks a given key as released and returns a tuple of actions, formatted (changed_state, led_update, display_command, press_sequence, type_str, error)"""
        # press_sequence is sequence of key codes held until the last one is pressed
        # type_str is a sting to be pressed one key at a time
        return self.states[self.state][row][column].released()

    def get_color(self, row, column):
        return self.states[self.state][row][column].get_color()

    def get_lit(self, row, column):
        return self.states[self.state][row][column].get_lit()

    def is_held(self, row, column):
        pass
        return self.is_pressed[row][column]
