#coding=gbk
#the class person remain some basic attributes of the people
#there are something that they chose randomly to simulate the real world
import random

import Model3
import coorditinates


class Person():
    #attributes
    home_loc=[]
    work_loc=[]
    #location of family and work.
    grid=[]
    locations=[]
    #model coorditions
    work_time=[]
    rest_time=[]
    # set the time to work[start,end] and sleep[start,end]
    args_model = [0, 0.6, -0.21]
    #set the gama and p for model,the Probability of explore is p*pow(S,gama)
    args_time = [-1.55, 0, 17, 10000]
    #set powerlaw disput time.beta=-1.55,time is between [0,17],simulate time is 10000
    args_steps = [-1.80, 5]
    #set steplegth ,beta and up limit
    args_grid = [[20, 20], [10, 2, 10, 2], 200]
    # grid dimension,grid_args(powerlaw contains [beta,min,max],normal contains [xmean,xsigma,ymean,ysigema]),number of point
    simulate_time = 10000
    #simulate times=10000
    home_locationList=[]
    work_locatonList=[]
    commute_LocationList=[]
    #the place the person has visit
    time=0
    time24=0
    stept=[]

    #function
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
    def set_args(self, args_model, args_step, args_t, args_grid, simulate_time):
        self.args_grid = args_grid
        self.args_model = args_model
        self.args_step = args_step
        self.args_t = args_t
        self.simulate_time = simulate_time
    def simulate(self):
        pass
    def set_time(self,time):
        self.time+=time
        self.time24=time%24
        print self.time24

class normal_person(Person):
    #create the model location disput nomal
    #peole select home and work randomly base on the position density
    def set_grid(self):
        if (len(self.args_grid) == 3):
            temp = coorditinates.normal_raster(self.args_grid[0], self.args_grid[1], self.args_grid[2])
            self.grid = temp.grid
            self.locations = temp.locationList
        else:
            print 'grid args is wrong'
    # ******should reset the model that do not need set the grid
    def set_home_loc(self):
        if(len(self.locations)):
            self.home_loc=random.choice(self.locations)
        else:
            print 'you should set grid first'
    def set_work_loc(self):
        if (len(self.locations)):
            self.work_loc= random.choice(self.locations)
        else:
            print 'you should set grid first'
    def set_work_time(self):
        start=random.normalvariate(7.5,1)
        end=random.normalvariate(17.5,1)
        self.work_time=[start,end]
    def set_rest_time(self):
        start = random.normalvariate(22, 1)
        end = random.normalvariate(6.5, 1)
        self.rest_time = [start, end]

    def __init__(self,args_model, args_step, args_t, args_grid, simulate_time):
        self.set_args(args_model, args_step, args_t, args_grid, simulate_time)
        self.set_grid()
        self.set_home_loc()
        self.set_work_loc()


    def simulate(self):
        t_now=6.5
        simulate_time=0
        while(simulate_time<self.simulate_time):
            self.set_work_time()
            self.set_rest_time()
            if(t_now<self.work_time[0]and t_now>self.rest_time[1]):
                #pass
                temp_Model=Model3.Commute_Model(self.args_model,self.args_t,self.args_steps,self.grid,self.locations,self.commute_LocationList,self.home_loc,self.work_loc)
                temp_Model.set_tbegin(t_now,self.work_time[0])
                self.work_locatonList=temp_Model.get_route(0)
                t_now=temp_Model.t_now
                #do things commute
                #parameter is t_now and work_time[0]
            elif(t_now>self.work_time[0] and t_now<self.work_time[1]):
                pass
                # temp_Model = Model3.HomeorWork_Model(self.args_model, self.args_t, self.grid, self.locations,
                #                                   self.commute_LocationList, self.home_loc, self.work_locatonList)
                # temp_Model.set_t(t_now, self.work_time[1])
                # self.work_locatonList = temp_Model.get_route(0)
                # t_now = temp_Model.t_now
                #do something around work
            elif(t_now>self.work_time[1] and t_now<self.rest_time[0]):
                pass
                # temp_Model = Model3.Commute_Model(self.args_model, self.args_t, self.grid, self.locations,
                #                                   self.commute_LocationList, self.home_loc, self.work_locatonList)
                # temp_Model.set_t(t_now, self.rest_time[0])
                # self.work_locatonList = temp_Model.get_route(1)
                # t_now = temp_Model.t_now
                #do things commute and then do things around home
            else:
                pass
                #sleep
