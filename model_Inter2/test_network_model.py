import Environment
import Individual_network
import time as tm
import Cal_para
time1=tm.time()
args_model=[0.6,-0.21]
args_time=[2,1,10000]
args_steps=[-1.80,100000]
args_grid=[[20,20],[10,2,10,2],200]
time=100
temp_routeList=[]
Envir=Environment.normal_network_Environment( 0,1000,.1)
#model=Model5.HomeOrWork_Model(args_model=args_model,args_t=args_time,args_steps=args_steps,environment=Envir,visited_Place=[],homeposition=random.choice(Envir.locations),workposition=random.choice(Envir.locations))
model=Individual_network.Nomal_Network_Individual(args_model=args_model,args_t=args_time,args_step=args_steps,simulate_time=time,Environment=Envir)
model.simulate()
print (9)
cal=Cal_para.Cal_para(model.data_mid.route,Envir)
dis=cal.get_visit_location_number_disput()
print (dis)
time2=tm.time()
print (time2-time1)