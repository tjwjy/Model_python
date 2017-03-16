#coding=gbk
import Cal_para
import random
import math
from scipy.stats import powerlaw
from matplotlib import pyplot as plt
import numpy as np
from matplotlib import animation
import Grid
import powerlow

#获取最大长度为imax_dis时候，各个长度的分布
#返回满足条件的距离的List和其出现的概率
def get_plist(beta,max_dis,gridDimension):
    disList=[]
    for i in range(1,min(max_dis,gridDimension+1)):
        for j in range(1,min(max_dis,gridDimension+1)):
            dis=math.sqrt(i * i + j * j)
            if(disList.count(dis)==0) &(dis<max_dis)&(dis>0):
                disList.append(dis)
    pList=[]
    disList.sort()
    for dis in disList:
        pList.append(math.pow(dis,beta))
    return(disList,pList)
#采用概率的方法随机选取下一步的点的位置
def get_nextstep(plist,L_place,postion,disList,gridDimension):
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
    # for postion1 in L_place:
    #     distemp=math.sqrt((postion[0]-postion1[0])**2+(postion[1]-postion1[1])**2)
    #     if(distemp==dis):
    #         place_temp_list.append(postion1)
    beta_dis=[]
    #存储距离目标点为dis的所有的点的x，y的差
    for i in range(0,int(dis)+1):
        for j in range(0,int(dis)+1):
            if((i*i+j*j==int(dis*dis)) & (beta_dis.count([i,j])==0)):
                beta_dis.append([i,j])
    if(len(beta_dis)==0):
        return 0
    else:
        beta=random.choice(beta_dis)
        signals=[[1,1],[1,-1],[-1,-1],[-1,1]]
        signal=random.choice(signals)
        #选取正负号
        next_postion= [postion[0]+signal[0]*beta[0],postion[1]+signal[1]*beta[1]]
        flag=1
        while (flag>0):
            if (next_postion[0] < 0 or next_postion[1] < 0 or next_postion[0] > gridDimension - 1 or next_postion[1] > gridDimension - 1):
                if (len(signals)>1):
                    signals.remove(signal)
                    signal=random.choice(signals)
                    next_postion = [postion[0] + signal[0] * beta[0], postion[1] + signal[1] * beta[1]]
                else:
                    flag=0
            else:
                index = (next_postion[0]-1) * gridDimension + next_postion[1]-1
                return L_place[index]
                break
        return 0



#获取时间间隔 呈现幂率分布
def get_route(args_model,args_times,args_steps,time_max,gridDimension):
    #初始化数据
    #args_model包含参数包括S，p，和指数gama
    #args_times包含参数包括时间的指数，上下限,要模拟的结果次数
    #args_step 包含步长的信息，指数，上限
    lstep=1
    tstep=powerlow.get_float_powerlaw(args_times[0],args_times[1],args_times[2],args_times[3])
    L_Place=Grid.get_simple_grid(dimenssionX=gridDimension,dimenssionY=gridDimension)#建立均质分布的网格
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
            temp = get_plist(max_dis=args_steps[1], gridDimension=gridDimension, beta=args_steps[0])
            next_postion = get_nextstep(temp[1], L_Place, postion, temp[0],gridDimension)
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

args_model=[0,0.6,-0.21]
args_time=[-1.55,0,17,1000]
args_steps=[-1.80,10]
time=100000
routeList=[]
for i in range (0,10):
    test=get_route(args_model=args_model,args_times=args_time,args_steps=args_steps,time_max=time,gridDimension=20)
    routeList.append(test)
route=Cal_para.Point_Visit(routeList)
visit_location_number_disput=route.get_visit_location_number_disput()
visite_frequency_disput=route.get_visit_frequency_disput()
rog_disput=route.get_rog_disput()
print visit_location_number_disput
print visite_frequency_disput
print rog_disput

##绘图
fig=plt.figure(1)
axes=fig.add_subplot(2,2,1,xlim=(1,100*len(visit_location_number_disput)),ylim=(0,1000))
line,=axes.plot([],[],lw=2)
y=visit_location_number_disput
x=[(i*100) for i in range(len(visit_location_number_disput))]
axes.plot(x,y)

axes2=fig.add_subplot(2,2,2,xlim=(1,len(visite_frequency_disput)),ylim=(0,1000))
line,=axes.plot([],[],lw=2)
y=visite_frequency_disput
x=[i for i in range(len(visite_frequency_disput))]
axes2.plot(x,y)

axes3=fig.add_subplot(2,2,3,xlim=(1,len(rog_disput)),ylim=(0,50))
line,=axes.plot([],[],lw=2)
y=rog_disput
x=[i for i in range(len(rog_disput))]
axes3.plot(x,y)
plt.show()