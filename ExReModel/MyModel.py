#coding=gbk
import random
import math
from matplotlib import pyplot as plt
import numpy as np
from matplotlib import animation
import Grid
import powerlow
from scipy.optimize import leastsq
def get_next_step(grid,beta,postion,max_dis):
    #����p=size/pow(d.beta)
    psum=[]
    temp_sum=0
    temp_grid=[]
    for temp in grid:
        if(int(temp[0]-postion[0])*(temp[0]-postion[0])+(temp[1]-postion[1])*(temp[1]-postion[1])<int(max_dis*max_dis)):
            dis=math.sqrt(pow((temp[0]-postion[0]),2)+pow((temp[1]-postion[1]),2))
            if(dis>0):
                p=temp[3]*pow(dis,0-beta)
                temp_grid.append(temp)
                temp_sum=temp_sum+p
                psum.append(temp_sum)
    ptemp=random.uniform(0,psum[len(psum)-1])
    nextstep=None
    for index,temp in enumerate(psum):
        if(ptemp<temp):
            nextstep=temp_grid[index]
            break
    return nextstep
def get_route(args_model,args_times,args_steps,time_max,gridDimension,grid_args):
    #��ʼ������
    #args_model������������S��p����ָ��gama
    #args_times������������ʱ���ָ����������,Ҫģ��Ľ������
    #args_step ������������Ϣ��ָ��������
    lstep=1
    tstep=powerlow.get_float_powerlaw(args_times[0],args_times[1],args_times[2],args_times[3])
    L_Place=Grid.get_powerlaw_grid(grid_args,dimenssionX=gridDimension,dimenssionY=gridDimension)
    L_tempPlace=[]
    gama=args_model[2]
    S=args_model[0]
    r=args_model[1]
    #���ѡ����ʼ�㣬����ʼ����Ҫ�õ���ѭ������
    postion=random.choice(L_Place)
    L_tempPlace.append(postion)
    S=S+1
    index=0
    time_sum=0
    while((time_sum<time_max)&( index<len(tstep)-1)):
        tag=r*S**(gama)
        tag2=random.random()
        if(tag>tag2):
            #��ʱ��ȥ̽���µĳ�������
            next_postion=get_next_step(grid=L_Place,beta=args_steps[0],postion=postion,max_dis=args_steps[1])
            if(next_postion==0):
                continue
            postion=next_postion
            ##���µ�ǰ����
            L_tempPlace.append(postion)
            S=S+1
            index=index+1
        else:
            postion=random.choice(L_tempPlace)
            L_tempPlace.append(postion)
            index=index+1
        time_sum=time_sum+tstep[index]
    return L_tempPlace
def get_probability(rutin):
    temp=[]
    for item in rutin:
        temp.append(item[2])
    temp1=np.array(temp)
    count=np.bincount(temp1)
    countL=count.tolist()
    tag_max=max(countL)
    temp_answer=[0]*(tag_max+1)
    for i in range(1,tag_max+1):
        tag1=countL.count(i)
        temp_answer[i]=tag1
    #fig,ax=plt.subplots(1,1)
    #ax.hist(countL,normed=1,histtype='stepfilled', alpha=0.2)
    #plt.show()
    return temp_answer,countL

args_model=[0,0.6,-0.21]
args_time=[-1.55,0,17,1000]
args_steps=[-1.80,10]
args_grid=[-2,1,17]
time=100000
temp_probability=[]
probability=[0]*(int(math.log(time)*3))
for i in range (0,10):
    test=get_route(args_model=args_model,args_times=args_time,args_steps=args_steps,time_max=time,gridDimension=40,grid_args=args_grid)
    prob,countL=get_probability(test)
    for j,prob in enumerate(prob):
        if(j<len(probability)):
            probability[j]=probability[j]+prob
    temp1=[]
    for t in probability:
        temp1.append((t/(i+1)))
    temp_probability.append(temp1)
    print probability
print temp_probability

#�����������ķֲ���ͼ
fig=plt.figure(1)
axes=fig.add_subplot(2,1,1,xlim=(1,20),ylim=(0,200))
line,=axes.plot([],[],lw=2)
def init():
    line.set_data([0],[0])
    return line
def animate(i):
    global temp_probability
    y=temp_probability[i]
    x=[i for i in range(0,len(temp_probability[i]))]
    line.set_data(x,y)
    return line
anim1=animation.FuncAnimation(fig,animate,init_func=init,frames=len(temp_probability),interval=30)

#����������Ķ�ͼ
axes2=fig.add_subplot(2,2,3,xlim=(1,20),ylim=(0,20))
max_prob=max(temp_probability)
grid1=Grid.get_simple_grid(40,40)
max_count=max(countL)
for i,count in enumerate(countL):
    x=grid1[i][0]
    y=grid1[i][1]
    s=count
    axes2.scatter(x,y,s=(count))

#����log����С���˻ع麯��
def func(p,x):
     k,b=p
     temp_y=[]
     for item in x:
         temp_y.append(k*item+b)
     return temp_y

def error(p,x,y,s):
    print s
    temp_answer=[]
    tempfunc=func(p,x)
    for i in range(0,min(len(tempfunc),len(y))):
        temp_answer.append(tempfunc[i]-y[i])
    return temp_answer
axes3=fig.add_subplot(2,2,4)
tempx=[]
tempy=[]
for i in range(1,len(probability)-1):
    if(probability[i]>0):
        tempy.append(math.log(probability[i]))
        tempx.append(math.log(i))
s="Test the number of iteration"
p0=[100,2]
Para=leastsq(error,p0,args=(tempx,tempy,s))
k,b=Para[0]
print k,b
axes3.scatter(tempx,tempy,s=35)
x=np.linspace(0,5,1000)
y=k*x+b
axes3.plot(x,y)
plt.show()