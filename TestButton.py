#!/usr/bin/python
import os
import time
import datetime
import sys
import RPi.GPIO as GPIO
import I2C_LCD_driver



class Termostat:
    def __init__(self):
        self._mode = 0
        self._temp = 20
        GPIO.setwarnings(False) # Ignore waring for now
        GPIO.setmode(GPIO.BOARD) # Use physical numbering
        GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_UP) # Set pin 11 to an input and that init$
        GPIO.setup(13, GPIO.IN, pull_up_down = GPIO.PUD_UP) # Set pin 13 to an input and that init$
        GPIO.setup(15, GPIO.IN, pull_up_down = GPIO.PUD_UP) # Set pin 15 to an input and that init$
        GPIO.add_event_detect(11, GPIO.RISING, callback = self.button_mode_callback_mode, bouncetime=50) # Setup event on pi$
        GPIO.add_event_detect(13, GPIO.RISING, callback = self.button_mode_callback_temp_up, bouncetime=50) # Setup event on pi$
        GPIO.add_event_detect(15, GPIO.RISING, callback = self.button_mode_callback_temp_down, bouncetime=50) # Setup event on pi$

    @property
    def mode(self):
        return self._mode
    @mode.setter
    def cycleMode(self):
        self._mode=(self.mode + 1)%3
        
    @property
    def temp(self):
        return self._temp
    @mode.setter
    def tempUp(self):
        self._temp += 1
    @mode.setter
    def tempUp(self):
        self._temp -= 1

    def button_mode_callback_mode(channel):
        
        self.mode = (self.mode(self.mode)+1 )% 3
        if self.mode:
            mylcd.lcd_display_string("Home Mode     ",4)
        elif:
            mylcd.lcd_display_string("Work Mode     ",4)
        else:
            mylcd.lcd_display_string("Away Mode     ",4)



if __name__ == "__main__":


    button = Termostat()
    myDisplay = Display()
    try:
        while True:
            print("hei")
            time.sleep(20)
