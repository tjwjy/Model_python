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
        pass

    def get_next_position(self):
        pass

    def set_t(self):
        if (len(self.args_t) != 0):
            theoretial_distribution = powerlaw.Power_Law(xmin=self.args_t[1], parameters=[-self.args_t[0]])
            self.ts = theoretial_distribution.generate_random(100)
class Commute_Model(Model):
    def choose_candidate_point(self,max_dis,anchor_point1,anchor_point2,L_Place):
        dis,point=self.Envir.Network.chose_candidate_points_2(max_dis=max_dis,anchor_point1=anchor_point1,anchor_point2=anchor_point2,locations=L_Place)
        return dis,point
    def get_next_position(self,L_place):
        # ����p=size/pow(d.beta)
        beta = self.args_step[0]
        max_step = self.args_step[1]
        psum = []
        temp_sum = 0
        temp_positon = []
        # �ڰ뾶�ڵ���������������x��y֮��
        temp_positon, dis = self.choose_candidate_point(max_dis=max_step, anchor_point1=self.HomePosition,anchor_point2=self.WorkPosition,L_Place=L_place)
        for i, dis_temp in enumerate(dis):
            if (dis_temp > 0):
                p = temp_positon[i].weight * pow(dis_temp, beta)
                temp_sum = temp_sum + p
                psum.append(temp_sum)
        if (len(psum) > 0):
            ptemp = random.uniform(0, psum[len(psum) - 1])
            nextstep = None
            for index, temp in enumerate(psum):
                if (ptemp < temp):
                    nextstep = temp_positon[index]
                    break
            return nextstep
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
    def choose_candidate_point(self,max_dis,anchor_point,L_Place):
        point,dis=self.Envir.Network.chose_candidate_points(max_dis=max_dis,anchor_point=anchor_point,locations=L_Place)
        return point,dis
    def get_next_position(self,L_place,flag):
        # ����p=size/pow(d.beta)
        beta = self.args_step[0]
        max_step = self.args_step[1]
        psum = []
        temp_sum = 0
        temp_positon = []
        # �ڰ뾶�ڵ���������������x��y֮��
        if(flag==0):
            temp_positon,dis=self.choose_candidate_point(max_dis=max_step,anchor_point=self.HomePosition,L_Place=L_place)
        if(flag==1):
            temp_positon, dis = self.choose_candidate_point(max_dis=max_step, anchor_point=self.WorkPosition,L_Place=L_place)
        for i,dis_temp in enumerate(dis):
            if (dis_temp > 0):
                p = temp_positon[i].weight*pow(dis_temp, beta)
                temp_sum = temp_sum + p
                psum.append(temp_sum)
        if (len(psum) > 0):
            ptemp = random.uniform(0, psum[len(psum) - 1])
            nextstep = None
            for index, temp in enumerate(psum):
                if (ptemp < temp):
                    nextstep = temp_positon[index]
                    break
            return nextstep
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
                if(postion not in L_place):
                    print (0)
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
