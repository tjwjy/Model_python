import Environment
import Model_inter
import Cal_para
import powerlaw
import IO
import matplotlib.pyplot as plt
args_model=[0.6,-0.21]
args_time=[2,1,10000]
args_steps=[-1.80,5]
args_grid=[[20,20],[10,2,10,2],200]
time=100
PointSize=1000
simulate_time=10000
temp_routeList=[]
Envir=Environment.normal_Environment(dimenssion=[20],xy_args=args_grid[1],size=PointSize)
document_name='normal_Envronment_PointSize_'+str(PointSize)+'_Time_'+str(simulate_time)+'.txt'
for i in range(0,100):
    exremodel=Model_inter.ExReModel(args_t=args_time,args_model=args_model,args_steps=args_steps,environment=Envir,visited_Place=[])
    exremodel.set_tbegin(0,simulate_time)
    route,mid=exremodel.get_route()
    mid.person_tag=i
    write = IO.IO(mid)
    write.write_txt('D:\\'+document_name, i)
    print (i)
print (00)

