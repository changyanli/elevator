import random
from threading import Thread
import time
class passenger:
    def __init__(self,appearTime,maxFloor=10,startFloor=None,endFloor=None):
        self.time=appearTime
        if(startFloor==None):
            self.start=random.randint(0,maxFloor-1)
        else:
            self.start=startFloor
        if(endFloor==None):
            self.end=random.randint(0,maxFloor-1)
        else:
            self.end=endFloor
        #endfloor should be different with startfloor
        while(self.start==self.end):
            self.end=random.randint(0,maxFloor-1)
        if(self.start>self.end):
            self.dir=-1#down
        else:
            self.dir=1#up
class passenger_generator:
    def __init__(self,filename="newPassengerList.txt",stoptime=10000,appear_freq=60,appear_max_num=12,maxFloor=10):
        self.stoptime=stoptime
        self.appear_freq=appear_freq
        self.appear_max_num=appear_max_num
        self.maxFloor=maxFloor
        if(filename == "newPassengerList.txt"): 
            self.file=open(filename,'w')
            self.generator()
        self.file=open(filename)
        self.reader()
        self.findindex=0
    def generator(self):
        for time in range(self.stoptime):
            if(random.randint(0,self.appear_freq-1) == 0):
                for newpass in range(random.randint(0,self.appear_max_num)):
                    newpassenger = passenger(time,maxFloor=self.maxFloor)
                    self.file.write(str(time)+' '+str(newpassenger.start)+' '+str(newpassenger.end)+'\n')
        self.file.close()
    def reader(self):
        self.passenger_list = []
        for line in self.file:
            appearTime, start, end = line.split()
            newpass=passenger(int(appearTime),startFloor=int(start),endFloor=int(end))
            self.passenger_list.append(newpass)
        self.file.close()
    def get_passengers(self,time):
        passengers = []
        while(len(self.passenger_list)>0 and self.passenger_list[0].time==time):
            passengers.append(self.passenger_list.pop(0))
        return passengers
if __name__ == "__main__":
    generator=passenger_generator()
    for time in range(generator.stoptime):
        passengers=generator.get_passengers(time)
        for peo in passengers:
            print(''+str(peo.time)+' '+str(peo.start)+' '+str(peo.end))
