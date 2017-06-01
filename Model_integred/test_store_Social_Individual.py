import Environment
import Individual
import Cal_para
import matplotlib.pyplot as plt
import IO
from scipy import stats


def set_value_list_x(Envir,average=10,sigma=5):
    #presume that the disput is 1-Normal_disput
    answer=[]
    for i in Envir.grid:
        tempi=int(i%Envir.grid_dimenssion[0])
        tempj=int(i/Envir.grid_dimenssion[0])
        x=stats.norm.pdf(tempi,average,sigma)*100
        y=stats.norm.pdf(tempj,average,sigma)*100
        value=int(x*y)
        answer.append(value)
    maxvalue=max(answer)
    answer2=[maxvalue-i for i in answer]
    return answer2

args_model=[0.6,-0.21]
args_time=[2,1,10000]
args_steps=[-1.80,5]
args_grid=[[10,10],[10,2,10,2],200]

PointSize=400
simulate_time=400
temp_routeList=[]
Envir=Environment.normal_Environment(dimenssion=[20],xy_args=args_grid[1],size=PointSize)
document_name='Nomal_Individual_HomeAndWork_Seperate_PointSize_'+str(PointSize)+'_Time_'+str(simulate_time)+'.txt'
value_list=set_value_list_x(Envir,5,2.5)
# i=[j for j in range(0,20)]
# value=[]
# for item in i:
#     value.append(value_list[item])
# x=[temp for temp in range(20)]
# plt.plot(x,value)
# plt.show()

for i in range(0,100):
#model=Model5.HomeOrWork_Model(args_model=args_model,args_t=args_time,args_steps=args_steps,environment=Envir,visited_Place=[],homeposition=random.choice(Envir.locations),workposition=random.choice(Envir.locations))
    model=Individual.Nomal_Individual_HomeAndWork_Seperate(args_model=args_model,args_t=args_time,args_step=args_steps,simulate_time=simulate_time,Environment=Envir)
    model.set_home_loc2(value_list)
    model.simulate()
    mid=model.data_mid
    write = IO.IO(mid)
    write.write_txt('D:\\'+document_name, i)
    print (i)
print (00)
