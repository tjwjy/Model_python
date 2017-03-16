#coding=gbk
import math
import random

import Model.powerlow
import Model2.coorditinates


class Model():
    args_model = []
    args_step = []
    args_t = []
    args_coordition = []
    simulate_time = 0
    # 初始化数据
    # args_model包含参数包括S，p，和指数gama
    # args_t包含参数包括时间的指数，上下限,要模拟的结果次数
    # args_step 包含步长的信息，指数，上限
    # args_grid 网格的参数，包括网格【长，宽】，【参数，如正太分布或者幂律参数】，得到的点的个数
    grid=[]
    locations=[]
    steps = []
    ts = []
    # 在初始化数据给予的情况下逐渐被赋值的参数
    ids = []
    frequency = []
    start_position=[]

    # 需要算出路径后给出的参数
    def __init__(self, args_model, args_step, args_t, args_grid, simulate_time):
        self.args_grid = args_grid
        self.args_model = args_model
        self.args_step = args_step
        self.args_t = args_t
        self.simulate_time = simulate_time
        self.set_t()
        self.set_grid()
    def get_route(self):
        if(self.grid!=0):
            L_place = [item for item in self.locations]  # 没有访问的集合
        else:
            exit()
        L_tempPlace = []  # 访问的集合
        gama = self.args_model[2]
        S = self.args_model[0]
        r = self.args_model[1]
        # 随机选择起始点，并初始化所要用到的循环数据
        postion = random.choice(L_place)
        L_tempPlace.append(postion)
        L_place.remove(postion)
        self.start_position=postion
        S = S + 1
        index = 0
        time_sum = 0
        while ((time_sum < self.simulate_time) & (index < len(self.ts) - 1)):
            tag = r * S ** (gama)
            tag2 = random.random()
            if (tag > tag2):
                # 这时候去探索新的场所代码
                next_postion = self.get_next_position(postion, L_place)
                if (next_postion == 0):
                    continue
                postion = next_postion
                ##更新当前坐标
                L_tempPlace.append(postion)
                L_place.remove(postion)
                S = S + 1
                index = index + 1
            else:
                postion = random.choice(L_tempPlace)
                L_tempPlace.append(postion)
                index = index + 1
            time_sum = time_sum + self.ts[index]
        for tempPlace in L_tempPlace:
            self.ids.append(tempPlace[2])
        return L_tempPlace

    def get_next_position(self):
        pass

    def set_grid(self):
        pass
    def set_t(self):
        if (len(self.args_t) != 0):
            self.ts = Model.powerlow.get_float_powerlaw(self.args_t[0], self.args_t[1], self.args_t[2], self.args_t[3])


class Normal_Model(Model):
    def dis(self,temp1,temp2):
        return math.pow((temp1[0]-temp2[0]),2)+math.pow((temp1[1]-temp2[1]),2)
    def set_grid(self):
        if (len(self.args_grid) == 3):
            temp = Model2.coorditinates.normal_raster(self.args_grid[0], self.args_grid[1], self.args_grid[2])
            self.grid=temp.grid
            self.locations=temp.locationList
        else:
            print 'grid args is wrong'
    def get_next_position(self,postion,L_place):
        # 概率p=size/pow(d.beta)
        beta = self.args_step[0]
        max_step = self.args_step[1]
        gridDimension = self.args_grid[0]
        psum = []
        temp_sum = 0
        temp_positon = []
        # 在半径内的所有满足条件的x，y之差
        for p in L_place:
            dis=self.dis(postion, p)
            if(dis<max_step*max_step):
                temp_positon.append([p,dis])
        temp2 = []
        for t_p in temp_positon:
            if (t_p[1] > 0):
                p = t_p[0][3]*pow(t_p[1], beta)
                temp_sum = temp_sum + p
                psum.append(temp_sum)
        if (len(psum) > 0):
            ptemp = random.uniform(0, psum[len(psum) - 1])
            nextstep = None
            for index, temp in enumerate(psum):
                if (ptemp < temp):
                    nextstep = temp_positon[index]
                    break
            return nextstep[0]
        else:
            return 0

class Random_Model(Normal_Model):
    def set_grid(self):
        if (len(self.args_grid) == 3):
            temp = Model2.coorditinates.random_raster(self.args_grid[0], self.args_grid[1], self.args_grid[2])
            self.grid=temp.grid
            self.locations=temp.locationList
        else:
            print 'grid args is wrong'
class PowerLaw_grid_Model(Normal_Model):
    def set_grid(self):
        if (len(self.args_grid) == 3):
            temp = Model2.coorditinates.powerLaw_grid(self.args_grid[0], self.args_grid[1], self.args_grid[2])
            self.grid = temp.grid
            self.locations = temp.locationList
        else:
            print 'grid args is wrong'

class Simple_grid_Model(Normal_Model):
    def set_grid(self):
        if (len(self.args_grid) == 3):
            temp = Model2.coorditinates.simple_grid(self.args_grid[0], self.args_grid[2])
            self.grid = temp.grid
            self.locations = temp.locationList
        else:
            print 'grid args is wrong'


class ExReModel(Model):
    def set_grid(self):
        if(len(self.args_grid==3)):
            temp= Model2.coorditinates.powerlaw_grid(self.args_grid[0], self.args_grid[1], self.args_grid[2])
            self.grid=temp.grid
            self.locations=temp.locationList
        else:
            print '创建坐标系过程中参数错误，是否和其他模型参数弄混'


