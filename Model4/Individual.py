import Model5
import Environment
import data_mid
import numpy as np
import Point
import random
class Individual():
    # attributes
    home_loc = Point.Point([],0,0)
    work_loc = Point.Point([],0,0)
    # location of family and work.
    Envir=Environment.Environment()
    # model coorditions
    work_time = []
    rest_time = []
    # set the time to work[start,end] and sleep[start,end]
    args_time = [-1.55, 1, 17, 10000]
    # set powerlaw disput time.beta=-1.55,time is between [0,17],simulate time is 10000
    args_steps = [-1.80, 5]
    # set steplegth ,beta and up limit
    # grid dimension,grid_args(powerlaw contains [beta,min,max],normal contains [xmean,xsigma,ymean,ysigema]),number of point
    simulate_time = 10000
    # simulate times=10000
    home_locationList = []
    work_locatonList = []
    commute_LocationList = []
    # the place the person has visit
    data_mid=[]

    # function

    def set_grid(self):
        pass

    def set_home_loc(self):
        pass

    def set_work_loc(self):
        pass

    def set_work_time(self):
        pass

    def set_rest_time(self):
        pass

    def set_args(self, args_model, args_step, args_t, simulate_time):
        self.args_model = args_model
        self.args_step = args_step
        self.args_t = args_t
        self.simulate_time = simulate_time

    def simulate(self):
        pass

    def set_time(self, time):
        self.time += time
        self.time24 = time % 24
        print(self.time24)


class Nomal_Individual(Individual):
    #create the model location disput nomal
    #peole select home and work randomly base on the position density
    def set_home_loc(self):
        if(len(self.Envir.locations)):
            self.home_loc=random.choice(self.Envir.locations)
        else:
            print ('you should set grid first before you set homelocation')
    def set_work_loc(self):
        if (len(self.Envir.locations)):
            self.work_loc= random.choice(self.Envir.locations)
        else:
            print ('you should set grid first before you set worklocation')
    def set_work_time(self):
        start=random.normalvariate(7.5,.5)
        end=random.normalvariate(17.5,1)
        self.work_time=[start,end]
    def set_rest_time(self):
        start = random.normalvariate(22, 1)
        end = random.normalvariate(6.5, .5)
        self.rest_time = [start, end]

    def __init__(self,args_model, args_step, args_t, simulate_time,Environment):
        self.Envir.set_environment(Environment)
        self.set_args(args_model, args_step, args_t, simulate_time)
        self.data_mid=data_mid.data_mid(Environment,person_tag=0)
        self.set_home_loc()
        self.set_work_loc()
        self.home_locationList = []
        self.work_locatonList = []
        self.commute_LocationList = []


    def simulate(self):
        print (self.home_loc)
        print (self.work_loc)
        simulate_time=0
        while(simulate_time<self.simulate_time):
            self.set_work_time()
            self.set_rest_time()
            t_now = self.rest_time[1]
            if(t_now<self.work_time[0]and t_now>=self.rest_time[1]):
                #pass
                temp_Model=Model5.Commute_Model(self.args_model,self.args_t,self.args_steps,self.Envir,self.commute_LocationList,self.home_loc,self.work_loc)
                temp_Model.set_tbegin(t_now,self.work_time[0])
                self.commute_LocationList,tempRoute=temp_Model.get_route(0)
                self.data_mid.add_location(tempRoute.route)
                t_now=temp_Model.t_now
                #do things commute
                #parameter is t_now and work_time[0]
            if(t_now>self.work_time[0] and t_now<self.work_time[1]):
                #pass
                temp_Model =Model5.HomeOrWork_Model(self.args_model,self.args_t,self.args_steps,self.Envir,self.work_locatonList,self.home_loc,self.work_loc)
                temp_Model.set_tbegin(t_now, self.work_time[1])
                self.work_locatonList,tempRoute = temp_Model.get_route(1)
                self.data_mid.add_location(tempRoute.route)
                t_now = temp_Model.t_now
                #do something around work
            if(t_now>self.work_time[1] and t_now<self.rest_time[0]):
                #pass
                while(t_now<self.rest_time[0]):
                    temp=random.random()
                    if(temp<0.9):
                        break
                    temp_Model = Model5.Commute_Model(self.args_model,self.args_t,self.args_steps,self.Envir,self.commute_LocationList,self.home_loc,self.work_loc)
                    temp_Model.set_tbegin(t_now,t_now+0.1)
                    self.commute_LocationList,tempRoute = temp_Model.get_route(1)
                    t_now = temp_Model.t_now
                    self.data_mid.add_location(tempRoute.route)
                if(t_now<self.rest_time[0]):
                    temp_Model = Model5.HomeOrWork_Model(self.args_model,self.args_t,self.args_steps,self.Envir,self.home_locationList,self.home_loc,self.work_loc)
                    temp_Model.set_tbegin(t_now, self.rest_time[0])
                    self.home_locationList,tempRoute=temp_Model.get_route(0)
                    t_now = temp_Model.t_now
                    self.data_mid.add_location(tempRoute.route)
                #do things commute and then do things around home
            if(t_now>self.rest_time[0] or t_now<self.rest_time[1]):
                t_now=self.rest_time[1]
                simulate_time+=1
                print (simulate_time)
                #sleep
