#coding=gbk
import powerlow as pl
import random
def get_simple_grid(dimenssionX,dimenssionY,powerlow_args=0):
    L_Place = []
    tag = 0
    for i in range(1, dimenssionX + 1):
        for j in range(1, dimenssionY + 1):
            L_Place.append([i, j, tag,1])
            tag = tag + 1
    return L_Place
def get_powerlaw_grid(dimenssionX,dimenssionY,powerlow_args=[-2,1,17]):
    beta=powerlow_args[0]
    min=powerlow_args[1]
    max=powerlow_args[2]
    size=dimenssionX*dimenssionY
    pl_rvs=pl.get_int_powerlaw(beta,min,max,size)
    L_Place = []
    tag = 0
    for i in range(1, dimenssionX + 1):
        for j in range(1, dimenssionY + 1):
            L_Place.append([i, j, tag,1])
            tag = tag + 1
    for i,rvs in enumerate(pl_rvs):
        L_Place[i][3]=rvs
    return L_Place
class coordition():
    locationList = []
    #五位，1，2位为x，y坐标，3位为所属的单元格坐标，四位是权重，五位为该点的id，第五位为栅格的数据所特有的
    grid_dimenssion = []
    # list x,y
    grid = []
    # list,the tag of the raster
    # ag从0开始，如果tag是1，1，则应当是第二行第二列，当点位的横坐标在1-2之间，纵坐标在1-2之间。方便进行归算
    # 不对外使用

    def set_dimenssion(self, dimenssion):
        if (len(dimenssion) == 2):
            self.grid_dimenssion = dimenssion
        elif (len(dimenssion == 1)):
            self.grid_dimenssion = [dimenssion, dimenssion]
        else:
            print ('grid dimenssion is not right')

    def __init__(self, dimenssion):
        pass
    def set_grid(self):
        if (len(self.grid_dimenssion) == 2):
           pass

    def set_locationList(self, x_arg, y_arg, size):
        pass

    def get_grid(self):
        return self.grid

    def get_location(self):
        if(len(self.locationList)>0):
            return self.locationList
        else:
            return []
class normal_raster(coordition):
    def set_grid(self):
        if(len(self.grid_dimenssion)==2):
            self.grid=get_simple_grid(self.grid_dimenssion[0],self.grid_dimenssion[1],0)

    def __init__(self, dimenssion, xy_args=[0,0,0,0], size=100):
        self.set_dimenssion(dimenssion)
        self.set_grid()
        self.set_locationList(xy_args, size)

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
            tag=(temp_int_x)*self.grid_dimenssion[0]+temp_int_y
            self.locationList.append([tempx,tempy,tag,1,t])
            t+=1
        print ('ok')

class random_raster(coordition):
    def set_grid(self):
        if (len(self.grid_dimenssion) == 2):
            self.grid = get_simple_grid(self.grid_dimenssion[0], self.grid_dimenssion[1], 0)
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
            tag = (temp_int_x) * self.grid_dimenssion[0] + temp_int_y
            self.locationList.append([tempx, tempy, tag, 1, t])
            t += 1

class simple_grid(coordition):
    def set_grid(self):
        if (len(self.grid_dimenssion) == 2):
            self.grid = get_simple_grid(self.grid_dimenssion[0], self.grid_dimenssion[1], 0)
    def set_locationList(self,size):
        t=0
        for i in range(size):
            temp = random.choice(self.grid)
            temp_tag = 0
            tempx = int(temp[0])
            tempy = int(temp[1])
            tag = (tempx) * self.grid_dimenssion[0] + tempy
            self.locationList.append([tempx, tempy, tag, 1, t])
            t += 1
    def __init__(self,dimenssion,size):
        self.set_dimenssion(dimenssion)
        self.set_grid()
        self.set_locationList(size)
class powerLaw_grid(coordition):
    def set_grid(self,args_powerlaw):
        if (len(self.grid_dimenssion) == 2):
            if(len(args_powerlaw)==3):
                self.grid = get_powerlaw_grid(self.grid_dimenssion[0],self.grid_dimenssion[1],args_powerlaw)
            else:
                self.grid=get_powerlaw_grid(self.grid_dimenssion[0],self.grid_dimenssion[1])

    def set_locationList(self,size):
        t=0
        for i in range(size):
            temp = random.choice(self.grid)
            temp_tag = 0
            tempx = int(temp[0])
            tempy = int(temp[1])
            weight=temp[3]
            tag = (tempx) * self.grid_dimenssion[0] + tempy
            self.locationList.append([tempx, tempy, tag, weight, t])
            t += 1

    def __init__(self,dimenssion,arg_powerlaw=[],size=100):
        self.set_dimenssion(dimenssion)
        self.set_grid(arg_powerlaw)
        self.set_locationList(size)


