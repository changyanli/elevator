class elevator:
    def __init__(self,maxfloor=10): #B1~9F
        self.status=0  #    0:stop 1:up -1:down
        self.maxfloor=maxfloor
        self.floor=1     #    default 1F 0=>B1
        self.passenger=[]
        self.maximum=12
        self.maxvelocity=2  #frame/floor
        self.minvelocity=4  #frame/floor
        self.velocity=4
        self.moving=0
        self.floorbtn=[False]*(self.maxfloor)
    def move(self,sys,time):
        if(self.moving==0):
            if(self.floorbtn[self.floor] or len(sys.floor_peo(self.floor,self.status))>0):
                self.reach_floor(sys,time)
            self.floor+=self.status
            if(self.floor<0):
                self.floor=0
            elif(self.floor>=self.maxfloor):
                self.floor=self.maxfloor-1
            nextfloor=self.floor+self.status
            if(nextfloor<0):
                nextfloor=0
            elif(nextfloor>=self.maxfloor):
                nextfloor=self.maxfloor-1
            if(self.floorbtn[self.floor] or len(sys.floor_peo(self.floor,self.status))>0):
                self.velocity=self.minvelocity
            elif(self.velocity>self.maxvelocity):
                self.velocity-=1
            if(self.floorbtn[nextfloor] or len(sys.floor_peo(nextfloor,self.status))>0):
                self.velocity+=1
            self.moving=self.velocity
        else:
            self.moving-=1
    def get_status(self):
        return self.status
    def peo_num(self):
        return len(self.passenger)
    def is_full(self):
        if(self.peo_num()==self.maximum):
             return True
        else:
             return False
    def reach_floor(self,sys,time):
        self.floorbtn[self.floor]=False;
        i=0
        while(i < len(self.passenger)):
            if(self.passenger[i].end == self.floor):
                sys.finishtime.append(time-self.passenger[i].time)
                #print(time-self.passenger[i].time,self.passenger[i].start,self.floor)
                self.passenger.pop(i)
            else:
                i+=1
        passengers=[]
        i=0
        while(i < len(sys.waitpeo[self.floor])):
            if(sys.waitpeo[self.floor][i].dir*self.status>=0):
                passengers.append(sys.waitpeo[self.floor].pop(i))
            else:
                i+=1
        self.passenger.extend(passengers)
        self.setbtn()
    def setbtn(self):
        for p in self.passenger:
            self.floorbtn[p.end]=True
    def still_work(self):
        for i in self.floorbtn:
            if(i):
                return True
        return False
