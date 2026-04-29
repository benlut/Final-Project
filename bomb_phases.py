#################################
# CSC 102 Defuse the Bomb Project
# GUI and Phase class definitions
# Team: 
#################################

from bomb_configs import *
from tkinter import *
import tkinter
from threading import Thread
from time import sleep
import os
import sys

#########
# classes
#########
class Lcd(Frame):
    def __init__(self, window):
        super().__init__(window, bg="black")
        window.attributes("-fullscreen", True)
        self._timer = None
        self._button = None
        self.setupBoot()

    def setupBoot(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)
        self._lscroll = Label(self, bg="black", fg="white", font=("Courier New", 14), text="", justify=LEFT)
        self._lscroll.grid(row=0, column=0, columnspan=3, sticky=W)
        self.pack(fill=BOTH, expand=True)

    def setup(self):
        self._ltimer = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Time left: ")
        self._ltimer.grid(row=1, column=0, columnspan=3, sticky=W)
        self._lkeypad = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Keypad phase: ")
        self._lkeypad.grid(row=2, column=0, columnspan=3, sticky=W)
        self._lwires = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Wires phase: ")
        self._lwires.grid(row=3, column=0, columnspan=3, sticky=W)
        self._lbutton = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Button phase: ")
        self._lbutton.grid(row=4, column=0, columnspan=3, sticky=W)
        self._ltoggles = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Toggles phase: ")
        self._ltoggles.grid(row=5, column=0, columnspan=2, sticky=W)
        self._lstrikes = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Strikes left: ")
        self._lstrikes.grid(row=5, column=2, sticky=W)

    def setTimer(self, timer): self._timer = timer
    def setButton(self, button): self._button = button

    def conclusion(self, success=False):
        self._lscroll.config(text="DEFUSED" if success else "EXPLODED")
        self._ltimer.destroy()
        self._lkeypad.destroy()
        self._lwires.destroy()
        self._lbutton.destroy()
        self._ltoggles.destroy()
        self._lstrikes.destroy()
        
        self._bretry = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Retry", command=self.retry)
        self._bretry.grid(row=1, column=0, pady=40)
        self._bquit = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Quit", command=self.quit)
        self._bquit.grid(row=1, column=2, pady=40)

    def retry(self):
        os.execv(sys.executable, ["python3"] + [sys.argv[0]])
        exit(0)

    def quit(self): exit(0)

class PhaseThread(Thread):
    def __init__(self, name, component=None, target=None):
        super().__init__(name=name, daemon=True)
        self._component = component
        self._target = target
        self._defused = False
        self._failed = False
        self._running = False

class Timer(PhaseThread):
    def __init__(self, component, initial_value):
        super().__init__("Timer", component)
        self._value = initial_value
        self._paused = False

    def run(self):
        self._running = True
        while (self._running):
            if not self._paused:
                self._update()
                self._component.print(str(self))
                sleep(1)
                if (self._value == 0): self._running = False
                self._value -= 1
            else: sleep(0.1)

    def _update(self):
        self._min = f"{self._value // 60}".zfill(2)
        self._sec = f"{self._value % 60}".zfill(2)

    def __str__(self): return f"{self._min}:{self._sec}"

class Keypad(PhaseThread):
    def run(self):
        self._running = True
        self._value = ""
        while (self._running):
            if (self._component.pressed_keys):
                key = self._component.pressed_keys[0]
                while (self._component.pressed_keys): sleep(0.1)
                self._value += str(key)
                if (self._value == self._target):
                    self._defused = True
                elif (self._value != self._target[0:len(self._value)]):
                    self._failed = True
            sleep(0.1)

    def __str__(self):
        if (self._defused): return f"DEFUSED | Wire clue: {WIRE_CLUE}" 
        return self._value

class Wires(PhaseThread):
    def run(self):
        self._running = True
        while (self._running):
            current = [pin.value for pin in self._component]
            if (current == self._target): self._defused = True
            elif (any(current) and current != self._target and sum(current) >= sum(self._target)):
                self._failed = True
            sleep(0.1)

    def __str__(self):
        if (self._defused): return "DEFUSED"
        current = [pin.value for pin in self._component]
        display = ""
        for i in range(5):
            display += f"[S{i+1}:{'IN' if current[i] else 'OUT'}] "
        return display

class Button(PhaseThread):
    def __init__(self, component, rgb, target, color, timer):
        super().__init__("Button", component, target)
        self._rgb = rgb
        self._color = color
        self._timer = timer

class Button(PhaseThread):
    # This must have exactly these 6 items (self + 5 from bomb.py)
    def __init__(self, component, rgb, target, color, timer):
        super().__init__("Button", component, target)
        self._rgb = rgb
        self._color = color
        self._timer = timer

    def run(self):
        self._running = True
        # Set colors (False is ON for common cathode/RPi pins usually)
        self._rgb[0].value = False if self._color == "R" else True
        self._rgb[1].value = False if self._color == "G" else True
        self._rgb[2].value = False if self._color == "B" else True
        
        pressed = False
        while (self._running):
            if (self._component.value): 
                pressed = True
            else:
                if (pressed):
                    # Check if target digit is in the timer seconds
                    if (not self._target or str(self._target) in self._timer._sec):
                        self._defused = True
                    else: 
                        self._failed = True
                    pressed = False
            sleep(0.1)

    def __str__(self): 
        return "DEFUSED" if self._defused else "Released"

class Toggles(PhaseThread):
    def run(self):
        self._running = True
        while (self._running):
            self._value = [pin.value for pin in self._component]
            if (self._value == self._target):
                self._defused = True
            sleep(0.1)

    def __str__(self): return "ONLINE" if self._defused else str(self._value)
