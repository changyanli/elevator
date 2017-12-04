import elevator as elev
import random
from threading import Thread
import numpy as np
import time
class passenger:
    def __init__(self,time):
        self.time=time
        self.start=random.randint(0,9)#B1~9F
        self.end=random.randint(0,9)
        while(self.start==self.end):
            self.end=random.randint(0,9)
        if(self.start>self.end):
            self.dir=-1#down
        else:
            self.dir=1#up
    def get_time(self):
        return self.time
    def get_end(self):
        return self.end
class elev_sys:
    def __init__(self):
        self.maxfloor=10 #B1~9F
        self.elev1=elev.elevator(self.maxfloor)
        self.elev2=elev.elevator(self.maxfloor)
        self.upbtn=[False]*(self.maxfloor-1)
        self.downbtn=[False]*(self.maxfloor-1)
        self.waitpeo=[[] for i in range(self.maxfloor)]
        self.finishtime=[]
    def reset(self):
        self.elev1=elev.elevator(self)
        self.elev2=elev.elevator(self)
        for i in range(self.maxfloor-1):
            self.upbtn[i]=False
            self.downbtn[i]=False
        for i in range(self.maxfloor):
            self.waitpeo[i]=[]
        self.finishtime=[]
    def _time_reward(self,time):
        wait_time=self.finishtime
        for i in range(self.maxfloor):
            for peo in self.waitpeo[i]:
                wait_time.append(time-peo.time)
        for peo in self.elev1.passenger:
            wait_time.append(time-peo.time)
        for peo in self.elev2.passenger:
            wait_time.append(time-peo.time)
        if(len(wait_time)==0):
            return 0,0
        else:
            return round(sum(wait_time)/len(wait_time),4),max(wait_time)
    def act(self,time):
        self.peo_come(time)
        self.set_btn()
        self.elev1.move(self,time)
        self.elev2.move(self,time)
        self.control(time)
    def _step(self,action):
        self.peo_come(time)
        self.set_btn()
        self.elev1.move(self,time)
        self.elev2.move(self,time)
        self.elev1.status=action[0]
        self.elev2.status=action[1]
        state = [self.elev1,self.elev2,waitpeo,averagetime,maxtime]
        reward=0
        for time in self.averagetime:
            reward+=time
        reward/=self.maxfloor
        reward-=maxtime
        if(maxtime>180):
            done=True
        else:
            done=False
        return np.array(state), reward, done, {}
    def control(self,time):
        status1=self.elev1.status
        status2=self.elev2.status
        up1=self.search_up(self.elev1)
        up2=self.search_up(self.elev2)
        down1=self.search_down(self.elev1)
        down2=self.search_down(self.elev2)
        if(self.elev1.floor==0 or self.elev1.floor==self.maxfloor-1):
            self.elev1.status=0
        if(self.elev2.floor==0 or self.elev2.floor==self.maxfloor-1):
            self.elev2.status=0
        if(up1!=None):
            if(up2!=None):
                if(up1<up2):
                    if(status1<1):
                        if(status1==0 or down1==None):
                            self.elev1.status=1
                        elif(status2==0 or down2==None):
                            self.elev2.status=1
                elif(up1>up2):
                    if(status2==0 or down2==None):
                        self.elev2.status=1
                    elif(status1==0 or down1==None):
                        self.elev1.status=1
                else:
                    if(status1==0 or down1==None):
                        self.elev1.status=1
                    elif(status2==0 or down2==None):
                        self.elev2.status=1
            else:
                if(status1==0 or down1==None):
                    self.elev1.status=1
        elif(up2!=None):
            if(status2==0 or down2==None):
                self.elev2.status=1
        if(down1!=None):
            if(down2!=None):
                if(down1<=down2):
                    if(status1>-1):
                        if(status1==0 or up1==None):
                            self.elev1.status=-1
                        elif(status2==0 or up2==None):
                            self.elev2.status=-1
                elif(down1>=down2):
                    if(status2>-1):
                        if(status2==0 or up2==None):
                            self.elev2.status=-1
                        elif(status1==0 or up1==None):
                            self.elev1.status=-1
                else:
                    if(status1==0 or up1==None):
                        self.elev1.status=-1
                    elif(status2==0 or up2==None):
                        self.elev2.status=-1
            else:
                if(status1==0 or up1==None):
                    self.elev1.status=-1
        elif(down2!=None):
            if(status2==0 or up2==None):
                self.elev2.status=-1
        if(up1 == None and down1 == None):
            self.elev1.status=0
        if(up2 == None and down2 == None):
            self.elev2.status=0
        '''
        if(self.elev1.status>0 and not self.search_up(self.elev1)):
            if(self.search_down(self.elev1)):
                self.elev1.status=-1
            else:
                self.elev1.status=0
        elif(self.elev1.status<0 and not self.search_down(self.elev1)):
            if(self.search_up(self.elev1)):
                self.elev1.status=1
            else:
                self.elev1.status=0
        elif(self.elev1.status==0):
            if(self.search_up(self.elev1)):
                self.elev1.status=1
            elif(self.search_down(self.elev1)):
                self.elev1.status=-1
        if(self.elev2.status>0 and not self.search_up(self.elev2)):
            if(self.search_down(self.elev2)):
                self.elev2.status=-1
            else:
                self.elev2.status=0
        elif(self.elev2.status<0 and not self.search_down(self.elev2)):
            if(self.search_up(self.elev2)):
                self.elev2.status=1
            else:
                self.elev2.status=0
        elif(self.elev2.status==0):
            if(self.search_up(self.elev2)):
                self.elev2.status=1
            elif(self.search_down(self.elev2)):
                self.elev2.status=-1
        
        '''
    def set_btn(self):
        for i in range(self.maxfloor):
            up=False;
            down=False;
            for p in self.waitpeo[i]:
                if(p.dir>0):
                    up=True
                elif(p.dir<0):
                    down=True
            if(i<self.maxfloor-1):
                self.upbtn[i]=up
            if(i>0):
                self.downbtn[i-1]=down
    def search_up(self,elev):
        i=elev.floor
        while(i<self.maxfloor-1):
            if(self.downbtn[i]):
                return i-elev.floor+1
            elif(i>elev.floor and self.upbtn[i]):
                return i-elev.floor
            i+=1
        if(elev.status>-1):
            i=elev.floor
            while(i<self.maxfloor):
                if(elev.floorbtn[i]):
                    return i-elev.floor
                i+=1
        return None
    def search_down(self,elev):
        i=elev.floor-1
        while(i>=0):
            if(self.upbtn[i]):
                return elev.floor-i
            elif(i<elev.floor-1 and self.downbtn[i]):
                return elev.floor-i+1
            i-=1
        if(elev.status<1):
            i=elev.floor
            while(i>=0):
                if(elev.floorbtn[i]):
                    return elev.floor-i
                i-=1
        return None              
    def floor_peo(self,floor,ud):#ud =1 up -1 down
        peos=[]
        i=0
        for peo in self.waitpeo[floor]:
            peos.append(peo.time)
        return peos
    def peo_come(self,time):
        if(random.randint(0,9)==1):
            newpass =passenger(time)
            self.waitpeo[newpass.start].append(newpass)
