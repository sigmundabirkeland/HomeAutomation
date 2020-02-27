import os
import time
import datetime
import sys
import RPi.GPIO as GPIO
import random
import I2C_LCD_driver





def read_temp():

    lines = temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = temp_raw()
    temp_output = lines[1].find('t=')

    if temp_output != -1:
        temp_string = lines[1].strip()[temp_output+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

def getState(mode):
    weekday = int(time.strftime("%w"))
    hour = float(time.strftime("%H"))
    #Away-mode activated
    if mode == 2:
        if hour >= 23 or hour < 7:
            return(0,0)
        else:
            return(1,0)
    #Monday to Thursday
    if weekday > 0 and weekday < 5:
        #night 
        if hour >= 23 or hour < 7:
             return(0,0)
        #home 
        if mode:
            return(1,1)
        #work 
        if hour >= 8 and hour < 14:
            return(1,0)
        else:
            #home
            return(1,1)
    #Friday
    if weekday == 5:
        #night
        if hour >= 24 or hour < 6:
            return(0,0)
        #home
        if home == True:
            return(1,1)
        #work
        if hour >= 8 and hour < 14:
            return(1,0)
        else:
            #home
            return(1,1)
    #Saturday
    if weekday == 6:
        #night
        if hour >= 23 or hour < 8:
            return(0,0)
        else:
            #home
            return(1,1)
    #Sunday
    if weekday == 0:
        #night
        if hour >= 23 or hour < 8:
            return(1,0)
        #home
        else:
            return(1,1)
def power(onOff):
    a_on =  '10011001101010100110101001011001100101100101010101101001101010101'
    a_off = '10011001101010100110101001011001100101100101010101101010101010101'
    b_on =  '10011001101010100110101001011001100101100101010101101001101010011'
    b_off = '10011001101010100110101001011001100101100101010101101010101010011'
    c_on =  '10011001101010100110101001011001100101100101010101101001101001101'
    c_off = '10011001101010100110101001011001100101100101010101101010101001101'

    #termo._owenPower = onOff
    #print("Owen Status: ",termo._owenPower,"onOff Status: ", onOff)
    if onOff:
        transmit_code(a_on)
        transmit_code(b_on)
        transmit_code(c_on)
    else:
        transmit_code(a_off)
        transmit_code(b_off)
        transmit_code(c_off)
    return()

#def updateDisplay():


    
def transmit_code(code):
    '''Transmit a chosen code string using the GPIO transmitter'''
    low_delay = 0.00025
    high_delay = 0.00025
    zero_delay = 0.001
    long_delay = 0.01
    start_delay = 0.00275
    NUM_ATTEMPTS = 5
    TRANSMIT_PIN = 16
    print("Transmitting")
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(TRANSMIT_PIN, GPIO.OUT)
    for t in range(NUM_ATTEMPTS):
        GPIO.output(TRANSMIT_PIN,1)
        time.sleep(high_delay)
        GPIO.output(TRANSMIT_PIN,0)
        time.sleep(start_delay)
        for i in code:
            if i == '1':
                GPIO.output(TRANSMIT_PIN, 1)
                time.sleep(high_delay)
                GPIO.output(TRANSMIT_PIN, 0)
                time.sleep(low_delay)
            elif i == '0':
                GPIO.output(TRANSMIT_PIN, 1)
                time.sleep(high_delay)
                GPIO.output(TRANSMIT_PIN, 0)
                time.sleep(zero_delay)
            else:
                continue
        GPIO.output(TRANSMIT_PIN, 0)
        time.sleep(long_delay)
        
class TermostatTemp:
    def __init__(self):
        self._low = 16
        self._high = 20
        self._mode = 0
        self._termoStates = getState(self._mode)
        self._owenPower = 0
        self._modes = ["Home","Work","Away"]
        self._states = ["Nighttime", "Daytime"]
        self._termoStatesString = ["%i" % self._low,"%i" % self._high]
        self._owenStates = ["Off","On"]
        GPIO.add_event_detect(11, GPIO.RISING, callback = self.button_mode_callback_mode, bouncetime=50) # Setup event on pi$
        GPIO.add_event_detect(13, GPIO.RISING, callback = self.button_mode_callback_temp_up, bouncetime=50) # Setup event on pi$
        GPIO.add_event_detect(15, GPIO.RISING, callback = self.button_mode_callback_temp_down, bouncetime=50) # Setup event on pi$

    @property
    def mode(self):
        return self._mode
    @mode.setter
    def mode(self,args):
        self._mode=args
    @property
    def owenPower(self):
        return self._owenPower
    @owenPower.setter
    def owenPower(self,args):
        self._owenPower = args
        power(args)

    @property
    def status(self):
        
        self.termoStates = getState(self._mode)
        
        return(self._modes[self._mode],self._states[self._termoStates[0]],
               self._termoStatesString[self._termoStates[1]],
               self._owenStates[self._owenPower])
    @property
    def currentTemp(self):
        self._termoStates = getState(self._mode)
        termoState = self._termoStates[1]
        if termoState:
            return self._high
        else:
            return self._low

    def button_mode_callback_mode(channel):
        
        self.mode = self.mode(self.mode)+1 % 3
        if home:
            #print("home")
            mylcd.lcd_display_string("Home Mode     ",4)
        else:
            #print("away")
            mylcd.lcd_display_string("Work Mode     ",4)

    def button_mode_callback_temp_up(channel):
        global high, low, normal, thermo, night
        #print("button 2 pushed")
        mode = getMode()
        if mode == 0:
            high += 1
            normal = high
            thermo = high
            mylcd.lcd_display_string("Target: %d%sC" % (high, chr(223)),2)
        elif mode == 1:
            low += 1
            night = low
            work = low
            thermo = low
            mylcd.lcd_display_string("Target: %d%sC" % (low, chr(223)),2)
        else:
            low += 1
            night = low
            work = low
            thermo = low
            mylcd.lcd_display_string("Target: %d%sC" % (low, chr(223)),2)

    def button_mode_callback_temp_down(channel):
        global high, low, normal, thermo, night
        #print("button 3 pushed")
        mode = getMode()
        if mode == 0:
            high -= 1
            normal = high
            thermo = high
            mylcd.lcd_display_string("Target: %d%sC" % (high, chr(223)),2)
        elif mode == 1:
            low -= 1
            night = low
            work = low
            thermo = low
            mylcd.lcd_display_string("Target: %d%sC" % (low, chr(223)),2)
        else:
            low -= 1
            night = low
            work = low
            thermo = low
            mylcd.lcd_display_string("Target: %d%sC" % (low, chr(223)),2)
    
    
  
        
def termostat():
    temperature = read_temp()
    #mode == 0 Home
    #mode == 1 Work
    #mode == 2 Away
    modeses = termo.mode
    #state == 0 night
    #state == 1 day
    #thermoState == 0 low
    #thermoState == 1 high


    if termo.currentTemp > temperature:
        termo.owenPower = 1        
    else:
        termo.ownePower = 0
    
    print(termo.status)
    #update display
    mlcd.draw(["Temperature %i" % (temperature),"Target Temp %i" % (termo.currentTemp),
               "Power: %s" % termo.status[3], "%s  %s" % (termo.status[0], termo.status[1])])


if __name__ == "__main__":

    GPIO.setwarnings(False) # Ignore waring for now
    GPIO.setmode(GPIO.BOARD) # Use physical numbering
    GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_UP) # Set pin 11 to an input and that init$
    GPIO.setup(13, GPIO.IN, pull_up_down = GPIO.PUD_UP) # Set pin 13 to an input and that init$
    GPIO.setup(15, GPIO.IN, pull_up_down = GPIO.PUD_UP) # Set pin 15 to an input and that init$
    mlcd.init(20,4)
    #Temperature sensor initialization
    
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    temp_sensor = '/sys/bus/w1/devices/28-0115827775ff/w1_slave'

    myDisplay = Display()
    
    
    termo = TermostatTemp()
    try:
        while True:
            
            termostat()
            mylcd.lcd_clear()
            mylcd.lcd_display_string("Temp: %d%sC" % (temp, chr(223)),1)
            mylcd.lcd_display_string("Target: %d%sC" % (thermo, chr(223)),2)
            mylcd.lcd_display_string(myDisplay.status,3)
            mylcd.lcd_display_string(myDisplay.mode,4)
            time.sleep(20)
 

