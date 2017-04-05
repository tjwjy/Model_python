#coding=gbk
import math
import random
import powerlow
import Route


class Model():
    args_model = []
    args_t = []
    args_step=[]
    # 初始化数据
    # args_model包含参数包括S，p，和指数gama
    grid=[]
    locations=[]
    steps = []
    # 在初始化数据给予的情况下逐渐被赋值的参数
    ids = []
    HomePosition=[]
    WorkPosition=[]
    visited_Place=[]
    #set the polace you have visit
    # 需要算出路径后给出的参数
    t_end=0
    t_now=0
    ts=[]
    def __init__(self, args_model,args_t,args_steps,grid,locations,visited_Place=[],homeposition=[],workposition=[]):
        self.args_model = args_model
        self.args_t=args_t
        self.args_step=args_steps
        self.visited_Place=visited_Place
        self.HomePosition=homeposition
        self.WorkPosition=workposition
        self.grid=grid
        self.locations=locations
        self.set_t()
    def set_tbegin(self,t_begin,t_end):
        self.t_now=t_begin
        self.t_end=t_end
    def get_route(self):
        L_place=[]
        L_tempPlace = self.visited_Place # 访问的集合
        if(self.grid!=0):
            for item in self.locations:
                if(item  not in L_tempPlace):
                    L_place.append(item) # 没有访问的集合
        else:
            exit()
        gama = self.args_model[2]
        S = self.args_model[0]
        r = self.args_model[1]
        # 随机选择起始点，并初始化所要用到的循环数据
        postion = random.choice(L_place)
        L_tempPlace.append(postion)
        L_place.remove(postion)
        self.start_position=postion
        S = S + 1
        index=1
        while ((self.t_now < self.t_end) & (index < len(self.ts) - 1)):
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
            self.t_now = self.t_now + self.ts[index]
        for tempPlace in L_tempPlace:
            self.ids.append(tempPlace[2])
        return L_tempPlace

    def get_next_position(self):
        pass
    def set_t(self):
        if (len(self.args_t) != 0):
            self.ts = powerlow.get_float_powerlaw(self.args_t[0], self.args_t[1], self.args_t[2], self.args_t[3])

class Commute_Model(Model):
    def dis(self,temp1):
        if(len(self.HomePosition)*len(self.WorkPosition)>0):
            r1=math.pow((temp1[0]-self.HomePosition[0]),2)+math.pow((temp1[1]-self.HomePosition[1]),2)
            r2=math.pow((temp1[0]-self.WorkPosition[0]),2)+math.pow((temp1[1]-self.WorkPosition[1]),2)
            return r1+r2
        else:
            return 1
    def get_next_position(self,L_place):
        # 概率p=size/pow(d.beta)
        beta = self.args_step[0]
        max_step = self.args_step[1]
        psum = []
        temp_sum = 0
        temp_positon = []
        # 在半径内的所有满足条件的x，y之差
        for p in L_place:
            dis=self.dis(p)
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
    def get_route(self,flag):
        route=Route.route([],[])
        L_place = []
        L_tempPlace = self.visited_Place  # 访问的集合
        if (self.grid != 0):
            for item in self.locations:
                if (item not in L_tempPlace):
                    L_place.append(item)  # 没有访问的集合
        else:
            exit()
        gama = self.args_model[2]
        S = self.args_model[0]
        r = self.args_model[1]
        # 随机选择起始点，并初始化所要用到的循环数据
        if(flag==0):
            postion=self.HomePosition
        if(flag==1):
            postion=self.WorkPosition
        if(postion in L_place):
            L_place.remove(postion)
            L_tempPlace.append(postion)
        self.start_position = postion
        S = S + 1
        index = 1
        while ((self.t_now < self.t_end) & (index < len(self.ts) - 1)):
            tag = r * S ** (gama)
            tag2 = random.random()
            if (tag > tag2):
                # 这时候去探索新的场所代码
                next_postion = self.get_next_position(L_place)
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
            route.time.append(self.t_now)
            route.route.append(postion)
            self.t_now = self.t_now + self.ts[index]
        for tempPlace in L_tempPlace:
            self.ids.append(tempPlace[2])
        return L_tempPlace,route

class HomeorWork_Model(Model):
    def dis(self,temp1,flag):
        if(flag==0 and len(self.HomePosition)>0):
            r1 = math.pow((temp1[0] - self.HomePosition[0]), 2) + math.pow((temp1[1] - self.HomePosition[1]), 2)
            return r1
        elif(flag==1 and len(self.WorkPosition)>0):
            r1 = math.pow((temp1[0] - self.WorkPosition[0]), 2) + math.pow((temp1[1] - self.WorkPosition[1]), 2)
            return r1
        else:
            return 1
    def get_next_position(self,L_place,flag):
        # 概率p=size/pow(d.beta)
        beta = self.args_step[0]
        max_step = self.args_step[1]
        psum = []
        temp_sum = 0
        temp_positon = []
        # 在半径内的所有满足条件的x，y之差
        for p in L_place:
            dis=self.dis(p,flag)
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

    def get_route(self,flag):
        route=Route.route([],[])
        L_place = []
        L_tempPlace = self.visited_Place  # 访问的集合
        if (self.grid != 0):
            for item in self.locations:
                if (item not in L_tempPlace):
                    L_place.append(item)  # 没有访问的集合
        else:
            exit()
        gama = self.args_model[2]
        S = self.args_model[0]
        r = self.args_model[1]
        # 随机选择起始点，并初始化所要用到的循环数据
        if (flag == 0):
            postion = self.HomePosition
        if (flag == 1):
            postion = self.WorkPosition
        if (postion in L_place):
            L_place.remove(postion)
            L_tempPlace.append(postion)
        self.start_position = postion
        S = S + 1
        index = 1
        while ((self.t_now < self.t_end) & (index < len(self.ts) - 1)):
            tag = r * S ** (gama)
            tag2 = random.random()
            if (tag > tag2):
                # 这时候去探索新的场所代码
                next_postion = self.get_next_position(L_place,flag)
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
            route.time.append(self.t_now)
            route.route.append(postion)
            self.t_now = self.t_now + self.ts[index]
        for tempPlace in L_tempPlace:
            self.ids.append(tempPlace[2])
        return L_tempPlace,route







