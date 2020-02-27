import os
import time
import datetime
import sys
import random
import mlcd #import of mock LCD


def read_temp():
    return random.randint(15,18)




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
    #GPIO.setmode(GPIO.BOARD)
    #GPIO.setup(TRANSMIT_PIN, GPIO.OUT)
    for t in range(NUM_ATTEMPTS):
        #GPIO.output(TRANSMIT_PIN,1)
        time.sleep(high_delay)
        #GPIO.output(TRANSMIT_PIN,0)
        time.sleep(start_delay)
        for i in code:
            if i == '1':
                #GPIO.output(TRANSMIT_PIN, 1)
                time.sleep(high_delay)
                #GPIO.output(TRANSMIT_PIN, 0)
                time.sleep(low_delay)
            elif i == '0':
                #GPIO.output(TRANSMIT_PIN, 1)
                time.sleep(high_delay)
                #GPIO.output(TRANSMIT_PIN, 0)
                time.sleep(zero_delay)
            else:
                continue
        #GPIO.output(TRANSMIT_PIN, 0)
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


    mlcd.init(20,4)
    mlcd.draw(["Hello world",
               "    ------",
               "Domination!"])
    
    termo = TermostatTemp()
    termostat()
 

