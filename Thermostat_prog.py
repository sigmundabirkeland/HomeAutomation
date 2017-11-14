#Thermostat prog
class Thermostat:
    #this should contain the current everyday status situation.
    #Can be set to work, home, vacation.
    #Typical week; work from 0800 to 1500 on weekdays
    #home from 1500 to 0700 and from 1500 on friday
    #to 0700 on the following monday.
    #Additionally there must be a difference between night and day,
    #and timing for night and day from weekdays compared to weekends.
 
    def __init__(self):
        self.NightThermo = 15
        self.DayThermo = 21
        self.workThermo = 15
        self.vacationThermo = 15

        
    def printStatus(self):
        print("hei")
        return
    def returnStatus(self):
        return("hei")
    
thermostat = Thermostat()
print(thermostat.DayThermo)
thermostat.printStatus()
    #function: Need set and get functions for all thermostats 
    
