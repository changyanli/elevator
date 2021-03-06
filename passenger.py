import random
from threading import Thread
import time
class passenger:
    def __init__(self,appearTime,maxFloor=10,startFloor=None,endFloor=None,oddeven=False):
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
        if oddeven:
            if self.start != 1 and self.end != 1 and self.start % 2 != self.end %2:
                if self.start % 2 == 0:
                    self.start = 1
                else:
                    self.end = 1
        if(self.start>self.end):
            self.dir=-1#down
        else:
            self.dir=1#up
class passenger_generator:
    def __init__(self,filename=None,stoptime=10000,appear_freq=60,appear_max_num=12,maxFloor=10,oddeven = False,num = 0):
        self.stoptime=stoptime
        self.appear_freq=appear_freq
        self.appear_max_num=appear_max_num
        self.filename=filename
        self.maxFloor=maxFloor
        if(self.filename == None):
            self.filename = "newPassengerList"+str(num)+".txt"
            self.file=open(self.filename,'w')
            self.generator(oddeven=oddeven)
        self.file=open(self.filename)
        self.reader()
    def generator(self,oddeven=False):
        for time in range(self.stoptime):
            if(random.randint(0,self.appear_freq-1) == 0):
                for newpass in range(random.randint(0,self.appear_max_num)):
                    newpassenger = passenger(time,maxFloor=self.maxFloor,oddeven=oddeven)
                    self.file.write(str(time)+' '+str(newpassenger.start)+' '+str(newpassenger.end)+'\n')
        self.file.close()
    def reader(self):
        self.passenger_list = []
        for line in self.file:
            appearTime, start, end = line.split()
            newpass=passenger(int(appearTime),startFloor=int(start),endFloor=int(end))
            self.passenger_list.append(newpass)
        self.file.close()
    def reset(self):
        del(self.passenger_list)
        self.file=open(self.filename)
        self.reader()
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
