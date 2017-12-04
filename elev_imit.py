from threading import Thread
import time
import tkinter as tk
from tkinter import *
import  passenger
import elev_sys as system
class elev_imit:
    def __init__(self):
        self.Frame=Tk()
        self.sys=system.elev_sys()
        self.can=Canvas(self.Frame, width=500, height=500)
        self.can.pack()
        self.maxfloor=10 #B1~9F
        self.size=40
        self.floorpeo=[None]*self.maxfloor
        self.peotext=[None]*self.maxfloor
        self.elev1 =[None]*self.maxfloor
        self.elev2 =[None]*self.maxfloor
        self.floor1 =[None]*self.maxfloor
        self.floor2 =[None]*self.maxfloor
        self.predraw()
    def floorblock(self,num,floor):
        return [100+200*num , 50+self.size * (self.maxfloor-1-floor) , 100+self.size+200*num ,50+self.size * (self.maxfloor-floor)]
    def predraw(self):
        for i in range(self.maxfloor):
            floor1=self.floorblock(0,i)
            floor2=self.floorblock(1,i)
            if(i==self.sys.elev1.floor):
                color1="#F00"
            elif(self.sys.elev1.floorbtn[i]):
                color1="#FF0"
            else:
                color1="#FFF"
            if(i==self.sys.elev2.floor):
                color2="#F00"
            elif(self.sys.elev2.floorbtn[i]):
                color2="#FF0"
            else:
                color2="#FFF"
            self.elev1=self.can.create_rectangle(floor1[0],floor1[1],floor1[2],floor1[3], fill=color1)
            self.elev2=self.can.create_rectangle(floor2[0],floor2[1],floor2[2],floor2[3], fill=color2)
        peo1=self.sys.elev1.peo_num()
        peo2=self.sys.elev2.peo_num()
        self.p1=self.can.create_text((floor1[0]+floor1[2])/2,(floor1[1]+floor1[3])/2,text=peo1)
        self.p2=self.can.create_text((floor2[0]+floor2[2])/2,(floor2[1]+floor2[3])/2,text=peo2)
        roof1=self.floorblock(0,self.sys.maxfloor)
        roof2=self.floorblock(1,self.sys.maxfloor)
        self.elev1_sta=self.can.create_text((floor1[0]+floor1[2])/2,(roof1[1]+roof1[3])/2,text="STOP")
        self.elev2_sta=self.can.create_text((floor2[0]+floor2[2])/2,(roof2[1]+roof2[3])/2,text="STOP")
        self.time=self.can.create_text(50,150,text="Time : 0")
        self.avr_time=self.can.create_text(40,300,text="Avr Time : 0")
        self.max_time=self.can.create_text(40,450,text="Max Time : 0")
    def draw(self,time):
        for i in range(self.maxfloor):
            floor1=self.floorblock(0,i)
            floor2=self.floorblock(1,i)
            if(i==self.sys.elev1.floor):
                color1="#F00"
            elif(self.sys.elev1.floorbtn[i]):
                color1="#FF0"
            else:
                color1="#FFF"
            if(i==self.sys.elev2.floor):
                color2="#F00"
            elif(self.sys.elev2.floorbtn[i]):
                color2="#FF0"
            else:
                color2="#FFF"
            self.elev1=self.can.create_rectangle(floor1[0],floor1[1],floor1[2],floor1[3], fill=color1)
            self.elev2=self.can.create_rectangle(floor2[0],floor2[1],floor2[2],floor2[3], fill=color2)
        self.can.delete(self.p1)
        self.can.delete(self.p2)
        self.can.delete(self.elev1_sta)
        self.can.delete(self.elev2_sta)
        self.can.delete(self.time)
        self.can.delete(self.avr_time)
        self.can.delete(self.max_time)
        
        floor1=self.floorblock(0,self.sys.elev1.floor)
        floor2=self.floorblock(1,self.sys.elev2.floor)
        roof1=self.floorblock(0,self.sys.maxfloor)
        roof2=self.floorblock(1,self.sys.maxfloor)
        peo1=self.sys.elev1.peo_num()
        peo2=self.sys.elev2.peo_num()
        if(self.sys.elev1.status>0):
            e1s="UP"
        elif(self.sys.elev1.status==0):
            e1s="STOP"
        else:
            e1s="DOWN"
        if(self.sys.elev2.status>0):
            e2s="UP"
        elif(self.sys.elev2.status==0):
            e2s="STOP"
        else:
            e2s="DOWN"
        e1s+=str(self.sys.elev1.floor)
        e2s+=str(self.sys.elev2.floor)
        self.p1=self.can.create_text((floor1[0]+floor1[2])/2,(floor1[1]+floor1[3])/2,text=peo1)
        self.p2=self.can.create_text((floor2[0]+floor2[2])/2,(floor2[1]+floor2[3])/2,text=peo2)
        self.elev1_sta=self.can.create_text((floor1[0]+floor1[2])/2,(roof1[1]+roof1[3])/2,text=e1s)
        self.elev2_sta=self.can.create_text((floor2[0]+floor2[2])/2,(roof2[1]+roof2[3])/2,text=e2s)
        timestr="Time : "
        timestr+=str(time)
        avr_timestr="Avr time : "
        max_timestr="Max time : "
        Avr , Max = self.sys._time_reward(time)
        avr_timestr+=str(Avr)
        max_timestr+=str(Max)
        self.time=self.can.create_text(50,150,text=timestr)
        self.avr_time=self.can.create_text(40,300,text=avr_timestr)
        self.max_time=self.can.create_text(40,450,text=max_timestr)
        for i in range(self.maxfloor):
            self.can.delete(self.peotext[i])
            floor=self.floorblock(1,i)
            text=str(len(self.sys.waitpeo[i]))
            if(i<self.maxfloor-1 and self.sys.upbtn[i]):
                text+="U"
            if(i>0 and self.sys.downbtn[i-1]):
                text+="D"
            self.peotext[i]=self.can.create_text((floor1[0]+floor1[2]+floor2[0]+floor2[2])/4,(floor[1]+floor[3])/2,text=text)
        """
        if( self.sys.elev1.floorfloat==0):
            self.can.create_text(50+self.size/2,30,text="開")
            time.sleep(0.1)
            self.can.create_text(50+self.size/2,30,text="關")
            time.sleep(0.1)
        """
    def main(self):
        for i in range(0,1000):
            #self.draw(i)
            self.sys.act(i)
            if(i%100 == 99):
                print(i,self.sys._time_reward(i))
            #self.draw(i)
            #self.can.update()
            #time.sleep(0.2)
        self.Frame.mainloop()
if __name__ == "__main__":
    imitator=elev_imit()
    imitator.main()