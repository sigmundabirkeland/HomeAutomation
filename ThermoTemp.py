import os
import time
import datetime
import sys
import RPi.GPIO as GPIO


def init():
    #Temperature sensor initialization
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')

def temp_raw():

    f = open(temp_sensor, 'r')
    lines = f.readlines()
    f.close()
    return lines

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

def transmit_code(code):
    '''Transmit a chosen code string using the GPIO transmitter'''
    GPIO.setmode(GPIO.BCM)
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
    GPIO.cleanup()
def getMode():
    weekday = int(time.strftime("%w"))
    hour = float(time.strftime("%H"))
    if weekday > 0 and weekday < 5:
        if hour >= 22 or hour < 6:
            return(1)
        if home == True:
            return(0)
        if hour >= 9 and hour < 14:
            return(2)
        else:
            return(0)
    if weekday == 5:
        if hour >= 23 or hour < 6:
            return(1)
        if home == True:
            return(0)
        if hour >= 9 and hour < 14:
            return(2)
        else:
            return(0)
    if weekday == 6:
        if hour >= 23 or hour < 8:
            return(1)
        else:
            return(0)
    if weekday == 0:
        if hour >= 22 or hour < 8:
            return(1)
        else:
            return(0)
init()
temp_sensor = '/sys/bus/w1/devices/28-0115827775ff/w1_slave'
#Send rf signal initialization
a_on =  '10011001101010100110101001011001100101100101010101101001101010101'
a_off = '10011001101010100110101001011001100101100101010101101010101010101'
b_on =  '10011001101010100110101001011001100101100101010101101001101010011'
b_off = '10011001101010100110101001011001100101100101010101101010101010011'
c_on =  '10011001101010100110101001011001100101100101010101101001101001101'
c_off = '10011001101010100110101001011001100101100101010101101010101001101'

low_delay = 0.00025
high_delay = 0.00025
zero_delay = 0.001
long_delay = 0.01
start_delay = 0.00275
NUM_ATTEMPTS = 5
TRANSMIT_PIN = 23
#end of init
weekday = time.strftime("%w")
time_H = time.strftime("%H")
time_M = time.strftime("%M")

normal = 22
night = 16
work = 16
home = True

with open("living_room_temp.csv", "a") as log:
while True:
	temp = read_temp()
    if getMode() == 0:
        thermo = normal
        print("normal mode. Thermo = ", thermo, "Temp = ", temp)
    elif getMode() == 1:
        thermo = night
        print("night mode. Thermo = ", thermo, "Temp = ", temp)
    else:
        thermo = work
        print("work mode. Thermo = ", thermo, "Temp = ", temp)
    if temp > thermo + 0.25:
        transmit_code(a_off)
        log.write("{0},{1},{2}\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(temp),"off"))
    if temp < thermo - 0.25:
        transmit_code(a_on)
        log.write("{0},{1},{2}\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(temp),"on"))
    else:
        log.write("{0},{1},{2}\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(temp),"unchanched"))
    GPIO.cleanup()
    time.sleep(300)
#end program cleanly
except KeyboardInterrupt:
    GPIO.cleanup()
    print "done"

