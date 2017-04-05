#coding=gbk
import math
import random
import data_mid
import Environment
import powerlaw
import Point
class Model():
    args_model = []
    args_t = []
    args_step = []
    # ��ʼ������
    # args_model������������S��p����ָ��gama
    #args_t������ʱ�������beta��xmin
    Envir=Environment.Environment()
    HomePosition=[]
    WorkPosition=[]
    visited_Place=[]
    #set the polace you have visit
    # ��Ҫ���·��������Ĳ���
    t_end=0
    t_now=0
    #ѭ����ʼ��ʱ��ͽ�����ʱ��
    ts=[]
    #ʱ��Ĳ������ڽ��н�ģǰ���Ƚ��ж��ģ�⣬����ʱ��Ĳ���
    def __init__(self, args_model,args_t,args_steps,environment,visited_Place=[],homeposition=[],workposition=[]):
        self.args_model = args_model
        self.args_t=args_t
        self.args_step=args_steps
        self.visited_Place=visited_Place
        self.HomePosition=homeposition
        self.WorkPosition=workposition
        self.Envir.set_environment(environment)
        self.set_t()
    def set_tbegin(self,t_now,t_end):
        self.t_now=t_now
        self.t_end=t_end
    def get_route(self):
        L_place=[]
        L_tempPlace = self.visited_Place # ���ʵļ���
        if(self.Envir.grid!=0):
            for item in self.Envir.locations:
                if(item  not in L_tempPlace):
                    L_place.append(item) # û�з��ʵļ���
        else:
            exit()
        gama = self.args_model[2]
        S = self.args_model[0]
        r = self.args_model[1]
        # ���ѡ����ʼ�㣬����ʼ����Ҫ�õ���ѭ������
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
                # ��ʱ��ȥ̽���µĳ�������
                next_postion = self.get_next_position(postion, L_place)
                if (next_postion == 0):
                    continue
                postion = next_postion
                ##���µ�ǰ����
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
            theoretial_distribution=powerlaw.Power_Law(xmin=self.args_t[1],parameters=[-self.args_t[0]])
            self.ts = theoretial_distribution.generate_random(100)

class Commute_Model(Model):
    def dis(self,temp1):
        if(len(self.HomePosition.location)*len(self.WorkPosition.location)>0):
            r1=math.pow((temp1.location[0]-self.HomePosition.location[0]),2)+math.pow((temp1.location[1]-self.HomePosition.location[1]),2)
            r2=math.pow((temp1.location[0]-self.WorkPosition.location[0]),2)+math.pow((temp1.location[1]-self.WorkPosition.location[1]),2)
            return r1+r2
        else:
            return 1
    def get_next_position(self,L_place):
        # ����p=size/pow(d.beta)
        beta = self.args_step[0]
        max_step = self.args_step[1]
        psum = []
        temp_sum = 0
        temp_positon = []
        # �ڰ뾶�ڵ���������������x��y֮��
        for p in L_place:
            dis=self.dis(p)
            if(dis<max_step*max_step):
                temp_positon.append([p,dis])
        for t_p in temp_positon:
            if (t_p[1] > 0):
                p = t_p[0].weight*pow(t_p[1], beta)
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
        mid=data_mid.data_mid(self.Envir,0)
        L_place = []
        L_tempPlace = self.visited_Place  # ���ʵļ���
        if (self.Envir.grid != 0):
            for item in self.Envir.locations:
                if (item not in L_tempPlace):
                    L_place.append(item)  # û�з��ʵļ���
        else:
            exit()
        gama = self.args_model[1]
        S = len(self.visited_Place)
        r = self.args_model[0]
        # ���ѡ����ʼ�㣬����ʼ����Ҫ�õ���ѭ������
        if(flag==0):
            postion=self.HomePosition
        if(flag==1):
            postion=self.WorkPosition
        if(postion in L_place):
            L_place.remove(postion)
        L_tempPlace.append(postion)
        temp_point = Point.Point(postion.location, postion.gridID, postion.ID, t=self.t_now, state=3,
                                     weight=postion.weight)
        mid.route.append(temp_point)
        S = S + 1
        index = 1
        while ((self.t_now < self.t_end) & (index < len(self.ts) - 1)):
            tag = r * S ** (gama)
            tag2 = random.random()
            if (tag > tag2):
                # ��ʱ��ȥ̽���µĳ�������
                next_postion = self.get_next_position(L_place)
                if (next_postion == 0):
                    continue
                postion = next_postion
                ##���µ�ǰ����
                L_tempPlace.append(postion)
                L_place.remove(postion)
                S = S + 1
                index = index + 1
            else:
                postion = random.choice(L_tempPlace)
                L_tempPlace.append(postion)
                index = index + 1
            temp_point=Point.Point(postion.location,postion.gridID,postion.ID,t=self.t_now,state=3,weight=postion.weight)
            mid.route.append(temp_point)
            self.t_now = self.t_now + self.ts[index]
        # for tempPlace in L_tempPlace:
            # self.ids.append(tempPlace.ID)
        return L_tempPlace,mid
class HomeOrWork_Model(Model):
    def dis(self,temp1,flag):
        if (flag == 0 and len(self.HomePosition.location) > 0):
            r1 = math.pow((temp1.location[0]-self.HomePosition.location[0]),2)+math.pow((temp1.location[1]-self.HomePosition.location[1]),2)
            return r1
        elif (flag == 1 and len(self.WorkPosition.location) > 0):
            r1 = math.pow((temp1.location[0]-self.WorkPosition.location[0]),2)+math.pow((temp1.location[1]-self.WorkPosition.location[1]),2)
            return r1
        else:
            return 1
    def get_next_position(self,L_place,flag):
        # ����p=size/pow(d.beta)
        beta = self.args_step[0]
        max_step = self.args_step[1]
        psum = []
        temp_sum = 0
        temp_positon = []
        # �ڰ뾶�ڵ���������������x��y֮��
        for p in L_place:
            dis=self.dis(p,flag )
            if(dis<max_step*max_step):
                temp_positon.append([p,dis])
        for t_p in temp_positon:
            if (t_p[1] > 0):
                p = t_p[0].weight*pow(t_p[1], beta)
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
        mid=data_mid.data_mid(self.Envir,0)
        L_place = []
        L_tempPlace = self.visited_Place  # ���ʵļ���
        if (self.Envir.grid != 0):
            for item in self.Envir.locations:
                if (item not in L_tempPlace):
                    L_place.append(item)  # û�з��ʵļ���
        else:
            exit()
        gama = self.args_model[1]
        S =len(self.visited_Place)
        r = self.args_model[0]
        # ���ѡ����ʼ�㣬����ʼ����Ҫ�õ���ѭ������
        if(flag==0):
            postion=self.HomePosition
        if(flag==1):
            postion=self.WorkPosition
        if(postion in L_place):
            L_place.remove(postion)
        L_tempPlace.append(postion)
        L_tempPlace.append(postion)
        temp_point = Point.Point(postion.location, postion.gridID, postion.ID, t=self.t_now, state=3,
                                 weight=postion.weight)
        mid.route.append(temp_point)
        self.start_position = postion
        S = S + 1
        index = 1
        while ((self.t_now < self.t_end) & (index < len(self.ts) - 1)):
            tag = r * S ** (gama)
            tag2 = random.random()
            if (tag > tag2):
                # ��ʱ��ȥ̽���µĳ�������
                next_postion = self.get_next_position(L_place,flag)
                if (next_postion == 0):
                    continue
                postion = next_postion
                ##���µ�ǰ����
                L_tempPlace.append(postion)
                L_place.remove(postion)
                S = S + 1
                index = index + 1
            else:
                postion = random.choice(L_tempPlace)
                L_tempPlace.append(postion)
                index = index + 1
            temp_point=Point.Point(postion.location,postion.gridID,postion.ID,t=self.t_now,state=flag,weight=postion.weight)
            mid.route.append(temp_point)
            self.t_now = self.t_now + self.ts[index]
        # for tempPlace in L_tempPlace:
            # self.ids.append(tempPlace.ID)
        return L_tempPlace,mid
