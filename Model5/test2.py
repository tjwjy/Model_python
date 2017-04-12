import Environment
import random
import Model5
args_model=[0.6,-0.21]
args_time=[2,1,10000]
args_steps=[-1.80,5]
args_grid=[[20,20],[10,2,10,2],200]
time=100
temp_routeList=[]
nomal_simple=Environment.normal_network_Environment( 0,100,.1)
model=Model5.Commute_Model(args_steps=args_steps,args_model=args_model,args_t=args_time,environment=nomal_simple,visited_Place=[],homeposition=random.choice(nomal_simple.locations),workposition=random.choice(nomal_simple.locations))
model.set_tbegin(6,10)
route=model.get_route(0)
print (route)