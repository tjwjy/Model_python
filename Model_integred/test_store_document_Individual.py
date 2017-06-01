import Environment
import Individual
import Cal_para
import matplotlib.pyplot as plt
import IO
args_model=[0.6,-0.21]
args_time=[2,1,10000]
args_steps=[-1.80,5]
args_grid=[[10,10],[10,2,10,2],200]

PointSize=400
simulate_time=400
temp_routeList=[]
Envir=Environment.normal_Environment(dimenssion=[20],xy_args=args_grid[1],size=PointSize)
document_name='Indevidual_normal_Envronment_PointSize_'+str(PointSize)+'_Time_'+str(simulate_time)+'.txt'
for i in range(0,100):
#model=Model5.HomeOrWork_Model(args_model=args_model,args_t=args_time,args_steps=args_steps,environment=Envir,visited_Place=[],homeposition=random.choice(Envir.locations),workposition=random.choice(Envir.locations))
    model=Individual.Nomal_Individual(args_model=args_model,args_t=args_time,args_step=args_steps,simulate_time=simulate_time,Environment=Envir)
    model.simulate()
    mid=model.data_mid
    write = IO.IO(mid)
    write.write_txt('D:\\'+document_name, i)
    print (i)
print (00)