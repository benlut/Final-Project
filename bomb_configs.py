#################################
# CSC 102 Defuse the Bomb Project
# Configuration file
# Team: 
#################################

# constants
DEBUG = False         # debug mode?
RPi = True            # is this running on the RPi?
SHOW_BUTTONS = False  # show the Pause and Quit buttons on the main LCD GUI?
COUNTDOWN = 300       # the initial bomb countdown value (seconds)
NUM_STRIKES = 5       # the total strikes allowed before the bomb "explodes"
NUM_PHASES = 4        # the total number of initial active bomb phases

# imports
from random import randint, shuffle, choice
from string import ascii_uppercase
if (RPi):
    import board
    from adafruit_ht16k33.segments import Seg7x4
    from digitalio import DigitalInOut, Direction, Pull
    from adafruit_matrixkeypad import Matrix_Keypad

#################################
# setup the electronic components
#################################
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

###########
# functions to generate targets
###########
def genSerial():
    return "B026DES"

def genTogglesTarget():
    # Switch On On off On <- Given from hint solving binary problem. 1 = On, 0 = Off - B
    return [True, True, False, True] 

def genWiresTarget():
    # 1st slot needs wire, 2nd empty, 3rd wire, 4th empty, 5th wire. - B
    return [True, False, True, False, True] 

WIRE_CLUE = "Odd numbers need wires." # Odd SLOTS only need wires. Even doesnt. (1,3,5) - B

def genKeypadTarget():
    return "2934" # Given number from clue -> Keypad

button_color = choice(["R", "G", "B"])

def genButtonTarget():
    global button_color
    b_target = None
    # G is the first numeric digit in the serial number
    if (button_color == "G"):
        b_target = [ n for n in serial if n.isdigit() ][0]
    # B is the last numeric digit in the serial number
    elif (button_color == "B"):
        b_target = [ n for n in serial if n.isdigit() ][-1]
    return b_target

###############################
serial = genSerial()
toggles_target = genTogglesTarget()
wires_target = genWiresTarget()
keypad_target = genKeypadTarget()
button_target = genButtonTarget()

# set the bomb's LCD bootup text
boot_text = f"--- SYSTEM ONLINE ---\n"\
            f"Serial number: {serial}\n"\
            f"POWER RESTORED."
