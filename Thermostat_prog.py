#Thermostat prog
import datetime
class Timing:
    def __init__(self):
        self.startTime = 0
        self.endTime = 0
        self.daysActive [0,0,0,0,0,0,0]
class Temp:
    #this should contain the current everyday status situation.
    #Can be set to work, home, vacation.
    #Typical week; work from 0800 to 1500 on weekdays
    #home from 1500 to 0700 and from 1500 on friday
    #to 0700 on the following monday.
    #Additionally there must be a difference between night and day,
    #and timing for night and day from weekdays compared to weekends.
 
    def __init__(self):
        self.temp = 15
    def setTemp(self, temp):
        self.temp = temp
        return
    def getTemp(self):
        return(self.temp)
    
    def printTemp(self):
        print(self.temp)
        return 
    
nightTemp = Temp()
nightTemp.printTemp()

print(datetime.datetime.today())
    #function: Need set and get functions for all thermostats 
    
