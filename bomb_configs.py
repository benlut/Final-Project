#################################
# CSC 102 Defuse the Bomb Project
# Configuration file
# Team: 
#################################

# constants
DEBUG = False
RPi = True
SHOW_BUTTONS = False
COUNTDOWN = 300
NUM_STRIKES = 5
NUM_PHASES = 4

# imports
from random import randint, shuffle, choice
from string import ascii_uppercase
if (RPi):
    import board
    from adafruit_ht16k33.segments import Seg7x4
    from digitalio import DigitalInOut, Direction, Pull
    from adafruit_matrixkeypad import Matrix_Keypad

# 7-segment display
if (RPi):
    i2c = board.I2C()
    component_7seg = Seg7x4(i2c)
    component_7seg.brightness = 0.5

# keypad
if (RPi):
    keypad_cols = [DigitalInOut(i) for i in (board.D10, board.D9, board.D11)]
    keypad_rows = [DigitalInOut(i) for i in (board.D5, board.D6, board.D13, board.D19)]
    keypad_keys = ((1, 2, 3), (4, 5, 6), (7, 8, 9), ("*", 0, "#"))
    component_keypad = Matrix_Keypad(keypad_rows, keypad_cols, keypad_keys)

# jumper wires
if (RPi):
    component_wires = [DigitalInOut(i) for i in (board.D14, board.D15, board.D18, board.D23, board.D24)]
    for pin in component_wires:
        pin.direction = Direction.INPUT
        pin.pull = Pull.DOWN

# pushbutton
if (RPi):
    component_button_state = DigitalInOut(board.D4)
    component_button_state.direction = Direction.INPUT
    component_button_state.pull = Pull.DOWN
    component_button_RGB = [DigitalInOut(i) for i in (board.D17, board.D27, board.D22)]
    for pin in component_button_RGB:
        pin.direction = Direction.OUTPUT
        pin.value = True

# toggle switches
if (RPi):
    component_toggles = [DigitalInOut(i) for i in (board.D12, board.D16, board.D20, board.D21)]
    for pin in component_toggles:
        pin.direction = Direction.INPUT
        pin.pull = Pull.DOWN

def genSerial(): return "B026DES"
def genTogglesTarget(): return [True, True, False, True] 
def genWiresTarget(): return [True, False, True, False, True] 
WIRE_CLUE = "Odd numbers need wires."
def genKeypadTarget(): return "2934"

serial = genSerial()
toggles_target = genTogglesTarget()
wires_target = genWiresTarget()
keypad_target = genKeypadTarget()
button_color = choice(["R", "G", "B"])

def genButtonTarget():
    global button_color
    b_target = None
    if (button_color == "G"):
        b_target = [ n for n in serial if n.isdigit() ][0]
    elif (button_color == "B"):
        b_target = [ n for n in serial if n.isdigit() ][-1]
    return b_target

button_target = genButtonTarget()
boot_text = f"--- SYSTEM ONLINE ---\nSerial number: {serial}\nPOWER RESTORED."
