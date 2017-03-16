#coding=gbk
import random
import math
from scipy.stats import powerlaw
from matplotlib import pyplot as plt
import numpy as np
from matplotlib import animation
import Grid
from scipy.optimize import leastsq
#获取时间间隔 呈现幂率分布
def getTstep(index,start,end,size):
    times_answer=[]
    if(index<0):
        index=abs(index)
        times=powerlaw.rvs(index,loc=start,scale=1,size=size)
        for time in times:
            times_answer.append(1/time)
    else:
        times_answer= powerlaw.rvs(index, loc=start, scale=end-start, size=size)
    return times_answer
def getTstep2(beta,start,end,size):
    x = get_powerlaw_rvs(beta, size=size)
    xtemp = []
    for item in x:
        if item < end and item>start:
            xtemp.append(item)
    return xtemp
#获取满足条件的点的距离以及其被选择的概率
def get_plist(beta,max_dis,gridDimension):
    disList=[]
    for  i in range(1,gridDimension+1):
        for j in range(1,gridDimension+1):
            dis=math.sqrt(i * i + j * j)
            if(disList.count(dis)==0) &(dis<max_dis)&(dis>0):
                disList.append(dis)
    pList=[]
    disList.sort()
    for dis in disList:
        pList.append(math.pow(dis,beta))
    return(disList,pList)
#采用概率的方法随机选取下一步的点的位置
def get_nextstep(plist,L_place,postion,disList):
    sum=0
    psumlist=[]
    for p in plist:
        sum=sum+p
        psumlist.append(sum)
    p_temp=random.uniform(0,psumlist[len(psumlist)-1])
    index=-1
    for i,p in enumerate(psumlist):
        if(p>p_temp):
            index=i
            break
    dis=disList[index]
    place_temp_list=[]
    for postion1 in L_place:
        distemp=math.sqrt((postion[0]-postion1[0])**2+(postion[1]-postion1[1])**2)
        if(distemp==dis):
            place_temp_list.append(postion1)
    if(len(place_temp_list)==0):
        return 0
    else:
        index1=random.randint(0,len(place_temp_list)-1)
        return place_temp_list[index1]
#生成坐标的网格
def get_grid(x,y):
    L_Place=[]
    tag=0
    for i in range(1,x+1):
        for j in range(1,y+1):
            L_Place.append([i,j,tag])
            tag=tag+1
    return L_Place
#获取生成的路线
def get_powerlaw_rvs(beta,size):
    beta2=-beta
    i=0
    y=[]
    while(i<size):
        y.append(random.random())
        i=i+1
    a=(-1+beta2)/(1-beta2)
    x=[]
    for y1 in y:
        temp=(-y1-a)*(-1+beta2)
        temp2=math.pow(temp,(1/(1-beta2)))
        x.append(temp2)
    return x
def get_rutin(args_model,args_times,args_steps,time_max,gridDimension):
    #初始化数据
    #args_model包含参数包括S，p，和指数gama
    #args_times包含参数包括时间的指数，上下限,要模拟的结果次数
    #args_step 包含步长的信息，指数，上限
    lstep=1
    tstep=getTstep2(args_times[0],args_times[1],args_times[2],args_times[3])
    L_Place=get_grid(gridDimension,gridDimension)
    L_tempPlace=[]
    gama=args_model[2]
    S=args_model[0]
    r=args_model[1]
    #随机选择起始点，并初始化所要用到的循环数据
    postion=random.choice(L_Place)
    L_tempPlace.append(postion)
    S=S+1
    index=0
    time_sum=0
    while((time_sum<time_max)&( index<len(tstep)-1)):
        tag=r*S**(gama)
        tag2=random.random()
        if(tag>tag2):
            #这时候去探索新的场所代码
            temp=get_plist(max_dis=args_steps[1], gridDimension=gridDimension, beta=args_steps[0])
            next_postion=get_nextstep(temp[1],L_Place,postion,temp[0])
            if(next_postion==0):
                continue
            postion=next_postion
            ##更新当前坐标
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

args_model=[0,0.6,0.21]
args_time=[-1.55,0,17,1000]
args_steps=[-1.80,100]
time=100000
temp_probability=[]
probability=[0]*(int(math.log(time)*3))
for i in range (0,10):
    test=get_rutin(args_model=args_model,args_times=args_time,args_steps=args_steps,time_max=time,gridDimension=0)
    counts,countL=get_probability(test)
    for j,count in enumerate(counts):
        if(j<len(probability)):
            probability[j]=probability[j]+count
    temp1=[]
    for t in probability:
        temp1.append((t/(i+1)))
    temp_probability.append(temp1)
    print probability
print temp_probability

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

#x=get_powerlaw_rvs(-1.55,1000)
#xtemp=[]
#for item in x:
    #if item<17:
        #xtemp.append(item)
#fig,ax=plt.subplots(1,1)
#ax.hist(xtemp, normed=0, histtype='bar', alpha=0.2)

axes2=fig.add_subplot(2,2,3,xlim=(1,20),ylim=(0,20))
max_prob=max(temp_probability)
grid1=Grid.get_simple_grid(20,20)
max_count=max(countL)
for i,count in enumerate(countL):
    x=grid1[i][0]
    y=grid1[i][1]
    s=count
    axes2.scatter(x,y,s=(count))

#绘制log的最小二乘回归函数
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