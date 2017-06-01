#coding=gbk
#it is a class to set the args of model
#model includes the grid and the locations in invironment
#grid is artificial,location is subject
import random
import Point
import network
import numpy as np
class Environment():
    # Network=network.NetWork()
    # grid=[]
    # locations=[]
    # grid_dimenssion = []

    def __init__(self):
        self.grid = []
        self.locations = []
        self.grid_dimenssion = []
        self.Network = network.NetWork()

    def set_environment(self,environment):
        self.Network=environment.Network
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
            self.grid = get_simple_grid(self.grid_dimenssion[0], self.grid_dimenssion[1])

    def set_network(self,path):
        pass


class normal_network_Environment(Environment):
    def set_network(self,path):
        self.Network.read_shpfile(path)

    def set_locations(self,n,parameter=.3):
        self.locations=self.Network.add_positon_normal(n,parameter)

    def __init__(self,path,n,parameter):
        Environment.__init__(self)
        self.set_network(path)
        self.set_locations(n,parameter)
class normal_Environment(Environment):
    def __init__(self, dimenssion, xy_args=[0,0,0,0], size=100):
        Environment.__init__(self)
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
        self.grid = []
        self.locations = []
        self.grid_dimenssion = []
        self.Network = network.NetWork()
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
#
# def get_simple_grid(dimenssionX,dimenssionY):
#     L_Place = []
#     tag = 0
#     for i in range(1, dimenssionX + 1):
#         for j in range(1, dimenssionY + 1):
#             L_Place.append([i, j, tag])
#             tag = tag + 1
#     return L_Place
def get_simple_grid(x,y):
    return [i for i in range(x*y)]

# nomal_simple=normal_network_Environment( 0,100,.1)
# di=nomal_simple.Network.chose_candidate_points(.3,random.choice(nomal_simple.locations),nomal_simple.locations)
# print (0)

class Social_Envrionment(Environment):
    def set_grid_loc_number(self, grid_value_list,size):
        grid_number=[]
        if(grid_value_list):
            temp_choice = []
            for i,item in enumerate(grid_value_list):
                if(item>0):
                    for j in range(item):
                        temp_choice.append(i)
            for i in range(size):
                grid_number.append(random.choice(temp_choice))
        temp1=np.array(grid_number)
        temp2=np.bincount(temp1)
        temp3=temp2.tolist()
        return temp3
    def set_locations(self, xy_min,xy_max, grid_value_list,size):
        temp=self.set_grid_loc_number(grid_value_list,size=size)
        x_length=xy_max[0]-xy_min[0]
        y_length=xy_max[1]-xy_min[1]
        x_single=x_length/self.grid_dimenssion[0]
        y_single=y_length/self.grid_dimenssion[1]
        tempID=0
        for item in self.grid:
            if(item<len(temp)):
                temp_i=item%self.grid_dimenssion[0]
                temp_j=int(item/self.grid_dimenssion[0])
                x_min=x_single*temp_i
                x_max=x_min+x_single
                y_min=y_single*temp_j
                y_max=y_min+y_single
                temp_size=temp[item],
                for item2 in range(temp_size):
                    x=random.uniform(x_min,x_max)
                    y=random.uniform(y_min,y_max)
                    gridid=item
                    ID=tempID
                    point=Point.Point(location=[x,y],gridid=gridid,ID=ID)
                    self.locations.append(point)
                    tempID+=1
        return True
    def __init__(self, dimenssion, xy_min,xy_max, grid_value_list, size=100):
        self.grid = []
        self.locations = []
        self.grid_dimenssion = []
        self.Network = network.NetWork()
        self.set_dimenssion(dimenssion)
        self.set_grid()
        self.set_locations( xy_min,xy_max, grid_value_list, size)


