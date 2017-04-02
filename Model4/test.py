# from scipy.stats import powerlaw
# import numpy as np
# import powerlaw as plw
# from matplotlib import pyplot as plt
# rvs=[]
# for i in range(10000):
#     temp=powerlaw.rvs(4)
#     rvs.append(temp)
# rvs2=[1/i for i in rvs]
# hist=np.arange(0,10,.5)
# fit=plw.Fit(rvs2,xmin=1)
# print (fit.alpha)
# print (fit.sigma)
# plt.hist(rvs2,bins=hist)
# plt.show()
import Model5
import Environment
import random
args_model=[0,0.6,-0.21]
args_time=[-2,0,5,10000]
args_steps=[-1.80,5]
args_grid=[[20,20],[10,2,10,2],200]
time=100
temp_routeList=[]
Envir=Environment.normal_Environment(dimenssion=[20],xy_args=args_grid[1],size=200)
model=Model5.Commute_Model(args_model=args_model,args_t=args_time,args_steps=args_steps,environment=Envir,visited_Place=[],homeposition=random.choice(Envir.locations),workposition=random.choice(Envir.locations))
model.set_tbegin(0,10)
route,mid=model.get_route(0)
print (9)