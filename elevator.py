class elevator:
    def __init__(self,maxfloor=10): #B1~9F
        self.status=0  #    0:stop 1:up -1:down
        self.maxfloor=maxfloor
        self._1f=1
        self.floor=self._1f #default 1F 0=>B1
        self.passenger=[]
        self.maximum=12
        self.maxvelocity=2  #sec/floor
        self.minvelocity=4  #sec/floor
        self.velocity=4
        self.moving=0
        self.doorOC=2       #door opening and closing spend 2 seconds
        self.floorbtn=[False]*(self.maxfloor)
    def move(self,sys,time):
        if self.moving == 0 :
            if self.floorbtn[self.floor] or len(sys.floor_peo(self.floor,self.status)) > 0 :
                if self.doorOC > 0 :
                    self.doorOC -= 1
                    return
                self.reach_floor(sys,time)
                self.doorOC = 2
                self.velocity = self.minvelocity
            self.floor += self.status
            if self.floor < 0 :
                self.floor = 0
            elif self.floor >= self.maxfloor :
                self.floor = self.maxfloor-1
            if self.floorbtn[self.floor] or len(sys.floor_peo(self.floor,self.status)) > 0 :
                if self.velocity < self.minvelocity:
                    self.velocity += 1
            elif self.velocity > self.maxvelocity:
                self.velocity -= 1
            self.moving = self.velocity
        else:
            self.moving -= 1
    def move_odd_even(self,sys,time,oe):#oe = 1 if odd =0 if even
        if self.moving == 0 :
            if self.floor %2 == oe or self.floor == self._1f :
                if self.floorbtn[self.floor] or len(sys.floor_peo(self.floor,self.status)) > 0 :
                    if self.doorOC > 0 :
                        self.doorOC -= 1
                        return
                    self.reach_floor(sys,time)
                    self.doorOC = 2
                    self.velocity = self.minvelocity
            self.floor += self.status
            if self.floor < 0 :
                self.floor = 0
            elif self.floor >= self.maxfloor :
                self.floor = self.maxfloor-1
            if self.floorbtn[self.floor] or len(sys.floor_peo(self.floor,self.status)) > 0 :
                if self.floor %2 == oe or self.floor == self._1f :
                    if self.velocity < self.minvelocity:
                        self.velocity += 1
            elif self.velocity > self.maxvelocity:
                self.velocity -= 1
            self.moving = self.velocity
        else:
            self.moving -= 1
    def getInf(self,time):
        etime=[]
        for peo in self.passenger:
            etime.append(time-peo.time)
        avr_time=0
        max_time=0
        if(len(etime)>0):
            avr_time=round(sum(etime)/len(etime),4)
            max_time=max(etime)
        Inf = [ self.status,
                self.floor,
                avr_time,
                max_time,
                self.moving ]
        Inf.extend(self.floorbtn)
        return Inf
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
        while(i < len(sys.waitpeo[self.floor]) and len(self.passenger)<self.maximum):
            if(sys.waitpeo[self.floor][i].dir*self.status>=0):
                passengers.append(sys.waitpeo[self.floor].pop(i))
            else:
                i+=1
        self.passenger.extend(passengers)
        self.setbtn()
    def setbtn(self):
        for p in self.passenger:
            self.floorbtn[p.end]=True
