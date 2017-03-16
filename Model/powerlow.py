import math
import random
from matplotlib import pyplot as plt
def get_int_powerlaw(beta,min,max,size):
    rvs=[i for i in range(min,max+1,1)]
    pList=[math.pow(i, beta) for i in rvs]
    pSumList=[]
    sum=0
    answer=[]
    for p in pList:
        sum=sum+p
        pSumList.append(sum)
    tag=0
    for i in range(0,size):
        temp=random.uniform(0,pSumList[len(pSumList)-1])
        for i,psum in enumerate(pSumList):
            if(psum>temp):
                tag=i
                break;
        answer.append(rvs[i])
    return answer
# xtemp=get_int_powerlaw(-2,1,6,100)
# fig,ax=plt.subplots(1,1)
# ax.hist(xtemp, normed=0, histtype='bar', alpha=0.2)
# plt.show()

def get_float_powerlaw(beta,min,max,size):
    x = get_powerlaw_rvs(beta, size=size)
    xtemp = []
    for item in x:
        if item < max and item > min:
            xtemp.append(item)
    return xtemp
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
