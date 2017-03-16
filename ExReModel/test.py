#coding=gbk
import math
import Model
from matplotlib import pyplot as plt
import Cal_para
import numpy as np
args_model=[0,0.6,-0.21]
args_time=[-1.55,0,17,10000]
args_steps=[-1.80,10]
args_grid=[100,100,1,[-2,1,17]]
time=10000
route=[]
for i in range(10):
    newModel=Model.ExReModel(args_model=args_model,args_grid=args_grid,args_step=args_steps,args_t=args_time,simulate_time=time)
    route.append(newModel.get_route())
cal=Cal_para.Point_Visit(route)

visit_location_number_disput=cal.get_visit_location_number_disput()
visite_frequency_disput=cal.get_visit_frequency_disput()
rog_disput=cal.get_rog_disput()
print visit_location_number_disput
print visite_frequency_disput
print rog_disput

##绘图
fig=plt.figure(1)
axes=fig.add_subplot(2,2,1,xlim=(1,100*len(visit_location_number_disput)),ylim=(0,600))
line,=axes.plot([],[],lw=2)
y=visit_location_number_disput
x=[(i*100) for i in range(len(visit_location_number_disput))]
axes.plot(x,y)

axes2=fig.add_subplot(2,2,2,xlim=(1,len(visite_frequency_disput)),ylim=(0,100))
line,=axes.plot([],[],lw=2)
y=visite_frequency_disput
x=[i for i in range(len(visite_frequency_disput))]
axes2.plot(x,y)

axes3=fig.add_subplot(2,2,3,xlim=(1,len(rog_disput)),ylim=(0,20))
line,=axes.plot([],[],lw=2)
y=rog_disput
x=[i for i in range(len(rog_disput))]
axes3.plot(x,y)

axes4=fig.add_subplot(2,2,4,xlim=(0,2),ylim=(0,10))
line,=axes.plot([],[],lw=2)
visite_frequency_disput.remove(visite_frequency_disput[0])
visite_frequency_plus1=[i+1 for i in visite_frequency_disput]
y=[math.log10(i) for i in visite_frequency_plus1]
x=[math.log10(i) for i in range(1,len(visite_frequency_disput)+1)]
axes4.scatter(x,y,s=35)
k,b=cal.cal_leastsq(x,y)
xtemp=np.linspace(0,math.log(len(visite_frequency_disput)+1),1000)
ytemp=k*xtemp+b
axes4.plot(xtemp,ytemp)
print k,b
plt.show()

