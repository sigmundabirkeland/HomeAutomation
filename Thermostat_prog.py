#Thermostat prog
import datetime
class Thermostat:
    #this should contain the current everyday status situation.
    #Can be set to work, home, vacation.
    #Typical week; work from 0800 to 1500 on weekdays
    #home from 1500 to 0700 and from 1500 on friday
    #to 0700 on the following monday.
    #Additionally there must be a difference between night and day,
    #and timing for night and day from weekdays compared to weekends.
 
    def __init__(self):
        self.nightTemp = 15
        self.dayTemp = 21
        self.workTemp = 15
        self.awayTemp = 15

        
    def printStatus(self):
        print("hei")
        return
    def returnStatus(self):
        return("hei")
    def setNightTemp(self, temp):
        self.nightTemp = temp
        return
    def getNightTemp(self):
        return(self.nightTemp)
    
    def setDayTemp(self, temp):
        self.dayTemp = temp
        return
    def getDayTemp(self):
        return(self.dayTemp)
    
    def setWorkTemp(self, temp):
        self.workTemp = temp
        return
    def getWorkTemp(self):
        return(self.workTemp)

    def setWorkTemp(self, temp):
        self.awayTemp = temp
        return
    def getWorkTemp(self):
        return(self.awayTemp)
    
thermostat = Thermostat()
print(thermostat.dayTemp)
thermostat.printStatus()
thermostat.setNightTemp(16)
print(thermostat.getNightTemp())
print(datetime.datetime.today())
    #function: Need set and get functions for all thermostats 
    
