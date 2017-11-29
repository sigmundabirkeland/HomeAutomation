#Thermostat prog
import datetime
class Timing:
    def __init__(self,name):
        self.name=name
        self.startTime = [22, 22, 22, 22, 24, 24, 22]
        self.endTime = [5.5, 5.5, 5.5, 5.5, 5.5, 9, 9]
        self.onDays = [1,1,1,1,1,1,1]
        self.offDays = [1,1,1,1,1,1,1]
        self.temperature = 15
    def setStartTime(self,onDays,startTime):
        self.onDays = onDays
        for i in range(0,6):
            if self.onDays[i] == 1:
                self.startTime = startTime
        return
    def setEndTime(self,offDays,endTime):
        self.offDays = offDays
        for i in range(0,7):
            if self.onDays[i] == 1:
                self.endTime = endTime
        return
    def checkMode(current):
    #Method to check current Mode. First I will test for NightMode
    #Current consist of day and time
        test = 1
        return
        
    def printTiming(self):
        print(self.name,"thermostat is set to: ", self.temperature)
        print("Weekday:\t","Mon","\t", "Tue","\t","Wed","\t","Thu","\t","Fri","\t","Sat","\t","Sun")
        print("Active :",end="\t")
        for i in range(0,7):
            if self.onDays[i] == 1:
                print("On",end="\t")
            else:
                print("off",end="\t")
        print("")
        print("Start  :",end="\t")
        for i in range(0,7):
            if self.onDays[i] == 1:
                print(self.startTime[i],end="\t")
            else:
                print("-",end="\t")
        print("")
        print("End    :",end="\t")
        for i in range(0,7):
            if self.onDays[i] == 1:
                print(self.endTime[i],end="\t")
            else:
                print("-",end="\t")
        return
            
            
        
        
        
        
class Temp:
    #this should contain the current everyday status situation.
    #Can be set to work, home, vacation.
    #Typical week; work from 0800 to 1500 on weekdays
    #home from 1500 to 0700 and from 1500 on friday
    #to 0700 on the following monday.
    #Additionally there must be a difference between night and day,
    #and timing for night and day from weekdays compared to weekends.
    #def __init__(self):
    #   self.thermoTemp = 21
    #    self.nightTiming = Timing("Night")
    timing = Timing("Night")
    def __init__(self,temp):
        self.thermoTemp = temp
        self.nightTiming = Timing("Night")
        return
    def setThermoTemp(self, temp):
        self.temp = temp
        return
    def getThermoTemp(self):
        return(self.thermoTemp)
    
    def printTemp(self):
        print("The thermostat temperature is set to ", self.thermoTemp, "C")
        return
    def getStatus(self):
        #function to fetch status
        return
#Global Function
def getSensorTemperature():
    #Call to get temperature from sensor
    return(10*rand())

    
temp = Temp(15)
temp.nightTiming.printTiming()#nightTemp.printTemp()
#nightTiming = Timing("Night")
#nightTiming.printTiming()



#print(datetime.datetime.today())
    #function: Need set and get functions for all thermostats 
    
