#!/usr/bin/python
import os
import time
import datetime
import sys
import RPi.GPIO as GPIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import I2C_LCD_driver


GPIO.setwarnings(False) # Ignore waring for now
GPIO.setmode(GPIO.BOARD) # Use physical numbering
GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # Set pin 11 to an input and that init$




def button_mode_callback(channel):
	home = not home
	print("button pushed")
	if home:
		print("home")
		mylcd.lcd_display_string("Home mode activated",4)
	else:
		mylcd.lcd_display_string("Home mode deactivated",4)


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
    GPIO.cleanup()
def getMode():
    weekday = int(time.strftime("%w"))
    hour = float(time.strftime("%H"))
    if weekday > 0 and weekday < 5:
        if hour >= 23 or hour < 6:
            return(1)
        if home == True:
            return(0)
        if hour >= 9 and hour < 14:
            return(2)
        else:
            return(0)
    if weekday == 5:
        if hour >= 24 or hour < 6:
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
        if hour >= 23 or hour < 8:
            return(1)
        else:
            return(0)

def plotGraph(temp,dateChanged,status,reset_time):
    dateChanged = 0
    if dateChanged == 1:
	plt.clf()
	plt.scatter(x,y)
	plt.plot(x,y)
	plt.title('Daily Temperature Change')
	fig.savefig('DayTemp.png')
	x[:] = []
	y[:] = []
	reset_time = time.time()
   	dateChanged = 0
    	#y.append(temp)
    	#x.append(time.time() - reset_time)

class Display:
    def __init__(self):
        self.mode = "init"
        self.status = "init"
init()
temp_sensor = '/sys/bus/w1/devices/28-0115827775ff/w1_slave'
#Send rf signal initialization
a_on =  '10011001101010100110101001011001100101100101010101101001101010101'
a_off = '10011001101010100110101001011001100101100101010101101010101010101'
b_on =  '10011001101010100110101001011001100101100101010101101001101010011'
b_off = '10011001101010100110101001011001100101100101010101101010101010011'
c_on =  '10011001101010100110101001011001100101100101010101101001101001101'
c_off = '10011001101010100110101001011001100101100101010101101010101001101'

mylcd = I2C_LCD_driver.lcd()

low_delay = 0.00025
high_delay = 0.00025
zero_delay = 0.001
long_delay = 0.01
start_delay = 0.00275
NUM_ATTEMPTS = 5
TRANSMIT_PIN = 16
push_button_pin = 11
#end of init

x = []
y = []



normal = 16
night = 16
work = 16
status = 0
home = False
#away = False
date = datetime.datetime.now().day
dateChanged = 0
reset_time = time.time()
thermo = normal
myDisplay = Display()
GPIO.add_event_detect(11, GPIO.RISING, callback = button_mode_callback) # Setup event on pi$
try:
    while True:
    	#with open("/home/pi/HomeAutomation/living_room_temp.csv", "a") as log:
        temp = read_temp()
        mode = getMode()
        print("Temperature ", temp)
	if mode == 0:
            thermo = normal
            myDisplay.mode = "Normal mode"
	    #mylcd.lcd_display_string("Normal mode",4)
        elif mode == 1:
            thermo = night
            myDisplay.mode = "Night mode"
            #mylcd.lcd_display_string("Night mode",4)
	    #print("night mode. Thermo = ", thermo, "Temp = ", temp)
        else:
            thermo = work
            myDisplay.mode = "Work mode"
	    #mylcd.lcd_display_string("Work mode",4)
            #print("work mode. Thermo = ", thermo, "Temp = ", temp)
        if temp > thermo + 0.25:
            transmit_code(a_off)
	    transmit_code(c_off)
            myDisplay.status = "Status: Off"
            if status == 1:
		#log.write("{0},{1},{2}\n".format(time.strftime("%Y-%m-%d 
		#%H:%M:%S"),str(temp),"0"))
            	status = 0
	    #else:
		#log.write("{0},{1},{2}\n".format(time.strftime("%Y-%m-%d 
		#%H:%M:%S"),str(temp),"0"))
	elif temp < thermo - 0.25:
            transmit_code(a_on)
	    transmit_code(c_on)
	    myDisplay.status = "Status: On"
            if status == 0:
		#log.write("{0},{1},{2}\n".format(time.strftime("%Y-%m-%d 
		#%H:%M:%S"),str(temp),"1"))
		status = 1
	    #else:
		#log.write("{0},{1},{2}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"),str(temp),"1"))
		#print("Thermostat on, temp = ",temp)
	#else:
	    #print("Thermostat unchanged, temp= ", temp)
	    #if status == 1:
		#log.write("{0},{1},{2}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"),str(temp),"1"))
	    #else:
		#log.write("{0},{1},{2}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"),str(temp),"0"))
        if datetime.datetime.now().day != date:
            dateChanged = True
            date = datetime.datetime.now().day
	    #plotGraph(temp,dateChanged,status,reset_time)
        print("Status: ", status)
        mylcd.lcd_clear()
	mylcd.lcd_display_string("Temp: %d%sC" % (temp, chr(223)),1)
	mylcd.lcd_display_string("Target: %d%sC" % (thermo, chr(223)),2)
        mylcd.lcd_display_string(myDisplay.status,3)
        mylcd.lcd_display_string(myDisplay.mode,4)
    	time.sleep(5)

#end program cleanly
except KeyboardInterrupt:
    GPIO.cleanup()
    mylcd.lcd_clear()
    print "done"

