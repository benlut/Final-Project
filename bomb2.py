#################################
# CSC 102 Defuse the Bomb Project
# Main program
# Team: 
#################################

from bomb_configs import *
from bomb_phases import *
from tkinter import *

booted = False 

# generates the bootup sequence on the LCD
def bootup():
    global booted
    gui._lscroll["text"] = boot_text.replace("\x00", "")
    gui.setup()
    if (RPi):
        timer.start()
        keypad.start()
        wires.start()
        button.start()
    booted = True
    gui.display_clue_image("clue1.png") 

# sets up the phase threads
def setup_phases():
    global timer, keypad, wires, button, toggles
    timer = Timer(component_7seg, COUNTDOWN)
    gui.setTimer(timer)
    keypad = Keypad(component_keypad, keypad_target)
    wires = Wires(component_wires, wires_target)
    button = Button(component_button_state, component_button_RGB, button_target, button_color, timer)
    gui.setButton(button)
    toggles = Toggles(component_toggles, toggles_target)
    toggles.start() # start toggles immediately to check power

# checks the phase threads
def check_phases():
    global active_phases, booted
    
    # Check for power first
    if not toggles._defused:
        gui._lscroll.config(text=" [ SYSTEM OFFLINE ]\n PLEASE FLIP BREAKER SWITCHES")
        gui.after(100, check_phases)
        return

    # If power is on but not booted yet
    if not booted: bootup()

    # check the timer
    if (timer._running):
        gui._ltimer["text"] = f"Time left: {timer}"
    else:
        turn_off()
        gui.after(100, gui.conclusion, False)
        return

    # check keypad
    if (keypad._running):
        gui._lkeypad["text"] = f"Keypad: {keypad}"
        if (keypad._defused):
            keypad._running = False
            active_phases -= 1
        elif (keypad._failed):
            strike()
            keypad._failed = False
            keypad._value = ""

    # check wires
    if (wires._running):
        gui._lwires["text"] = f"Wires: {wires}"
        if (wires._defused):
            wires._running = False
            active_phases -= 1
        elif (wires._failed):
            strike()
            wires._failed = False

    # check button
    if (button._running):
        gui._lbutton["text"] = f"Button: {button}"
        if (button._defused):
            button._running = False
            active_phases -= 1
        elif (button._failed):
            strike()
            button._failed = False

    gui._lstrikes["text"] = f"Strikes left: {strikes_left}"
    
    if (strikes_left == 0):
        turn_off()
        gui.after(100, gui.conclusion, False)
        return

    if (active_phases == 0):
        turn_off()
        gui.after(100, gui.conclusion, True)
        return

    gui.after(100, check_phases)

# handles a strike
def strike():
    global strikes_left
    strikes_left -= 1

# turns off the bomb
def turn_off():
    timer._running = False
    keypad._running = False
    wires._running = False
    button._running = False
    toggles._running = False
    if (RPi):
        component_7seg.fill(0)
        for pin in component_button_RGB:
            pin.value = True

######
# MAIN
######
window = Tk()
gui = Lcd(window)
strikes_left = NUM_STRIKES
active_phases = NUM_PHASES

if (RPi): setup_phases()
gui.after(100, check_phases)
window.mainloop()