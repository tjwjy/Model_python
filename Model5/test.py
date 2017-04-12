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
import Individual
import Cal_para
import Draw
args_model=[0.6,-0.21]
args_time=[2,1,10000]
args_steps=[-1.80,5]
args_grid=[[20,20],[10,2,10,2],200]
time=100
temp_routeList=[]
Envir=Environment.normal_network_Environment( 0,100,.1)
#model=Model5.HomeOrWork_Model(args_model=args_model,args_t=args_time,args_steps=args_steps,environment=Envir,visited_Place=[],homeposition=random.choice(Envir.locations),workposition=random.choice(Envir.locations))
model=Individual.Nomal_Individual(args_model=args_model,args_t=args_time,args_step=args_steps,simulate_time=time,Environment=Envir)
model.simulate()
print (9)
cal=Cal_para.Cal_para(model.data_mid.route,Envir)
dis=cal.get_visit_location_number_disput()
draw=Draw.Draw(cal,[model.home_loc,model.work_loc])
draw.draw_visit_location_number_disput()
draw.draw_location_disput(model.data_mid)
print (1)