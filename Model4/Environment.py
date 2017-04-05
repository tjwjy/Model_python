#coding=gbk
#it is a class to set the args of model
#model includes the grid and the locations in invironment
#grid is artificial,location is subject
import numpy as np
import random
import Point
class Environment():
    grid=[]
    locations=[]
    grid_dimenssion = []

    def __init__(self):
        self.grid = []
        self.locations = []
        self.grid_dimenssion = []

    def set_environment(self,environment):
        self.grid=environment.grid
        self.locations=environment.locations
        self.grid_dimenssion=environment.grid_dimenssion
    #set the parameters of the class
    def set_dimenssion(self, dimenssion):
        if (len(dimenssion) == 2):
            self.grid_dimenssion = dimenssion
        elif (len(dimenssion) == 1):
            self.grid_dimenssion = [dimenssion[0], dimenssion[0]]
        else:
            pass
    def set_locations(self, x_arg, y_arg, size):
        pass
    def set_grid(self):
        if (len(self.grid_dimenssion) == 2):
            pass


class normal_Environment(Environment):
    def __init__(self, dimenssion, xy_args=[0,0,0,0], size=100):
        self.grid = []
        self.locations = []
        self.grid_dimenssion = []
        self.set_dimenssion(dimenssion)
        self.set_grid()
        self.set_locationList(xy_args, size)

    def set_grid(self):
        if(len(self.grid_dimenssion)==2):
            self.grid=get_simple_grid(int(self.grid_dimenssion[0]),int(self.grid_dimenssion[1]))
        if(len(self.grid_dimenssion)==1):
            self.grid=get_simple_grid(int(self.grid_dimenssion[0]),int(self.grid_dimenssion[0]))

    def set_locationList(self,xy_args,size):
        xmu=xy_args[0]
        xsigma=xy_args[1]
        ymu=xy_args[2]
        ysigma=xy_args[3]
        t=0
        for i in range(size):
            tempx=random.gauss(xmu,xsigma)
            tempy=random.gauss(ymu,ysigma)
            temp_tag=0
            temp_int_x=int(tempx)
            temp_int_y=int(tempy)
            gridID=(temp_int_x)*self.grid_dimenssion[0]+temp_int_y
            temp_point=Point.Point([tempx,tempy],gridID,t)
            self.locations.append(temp_point)
            t+=1
        print ('ok')
class random_Environment(Environment):
    def set_grid(self):
        if (len(self.grid_dimenssion) == 2):
            self.grid = get_simple_grid(self.grid_dimenssion[0], self.grid_dimenssion[1])
    def __init__(self, dimenssion, xy_args=0, size=100):
        self.set_dimenssion(dimenssion)
        self.set_grid()
        self.set_locationList(size)

    def set_locationList(self,size):
        t=0
        for i in range(size):
            tempx = random.uniform(0,self.grid_dimenssion[0])
            tempy = random.uniform(0,self.grid_dimenssion[1])
            temp_tag = 0
            temp_int_x = int(tempx)
            temp_int_y = int(tempy)
            gridID = (temp_int_x) * self.grid_dimenssion[0] + temp_int_y
            temp_point = Point.Point([tempx, tempy], gridID, t)
            self.locations.append(temp_point)
            t += 1

def get_simple_grid(dimenssionX,dimenssionY):
    L_Place = []
    tag = 0
    for i in range(1, dimenssionX + 1):
        for j in range(1, dimenssionY + 1):
            L_Place.append([i, j, tag])
            tag = tag + 1
    return L_Place

temp=normal_Environment([20,20 ],[10,2,10,2])
print (0)