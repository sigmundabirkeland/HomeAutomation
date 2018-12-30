import time
import sys
import RPi.GPIO as GPIO

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
NUM_ATTEMPTS = 10
TRANSMIT_PIN = 23

def transmit_code(code):
    '''Transmit a chosen code string using the GPIO transmitter'''
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRANSMIT_PIN, GPIO.OUT)
    #TODO must set up start signal
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

if __name__ == '__main__':
    for argument in sys.argv[1:]:
        exec('transmit_code(' + str(argument) + ')')
counter = 0

while (counter < 4):
	transmit_code(a_off)
	time.sleep(2)
	transmit_code(c_off)
	counter = counter + 1
	time.sleep(2)
