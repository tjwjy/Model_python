#coding=gbk
import numpy as np
import math
from scipy.optimize import leastsq
class Cal_para():
    locationList=[]
    idList=[]
    #网格数据就是网格的点，栅格的话就是栅格所在的栅格的位置
    def __init__(self,gridList):
        #form of grid is (x,y.id)
        for grid in gridList:
             self.add_new_grid(grid)
    def add_new_grid(self,grid):
        locations=[]
        ids=[]
        for g in grid:
            locations.append([g[0],g[1]])
            ids.append(g[2])
        self.idList.append(ids)
        self.locationList.append(locations)
    def get_visit_location_number(self,ids,num):
        id_array=np.array(ids[0:num])
        num=np.unique(id_array)
        return len(num)
    def get_visit_location_number_disput(self):
        #得到随着时间的增长，拜访的地点的数量的变化
        nums=self.set_step(2)#选取抽样的步长，2，采用100为步长统计数据
        disput=[]
        for num in nums:
            sum_number=0
            for id in self.idList:
                sum_number+=self.get_visit_location_number(id,num)
            sum_number=sum_number/len(self.idList)
            disput.append(sum_number)
        return disput
    def get_Rog(self,locations,num):
        locationlist=locations[0:num]
        x=0
        y=0
        for location in locationlist:
            x+=location[0]
            y+=location[1]
        x=x/len(locationlist)
        y=y/len(locationlist)
        x2=0
        y2=0
        for location in locationlist:
            x2+=(location[0]-x)*(location[0]-x)
            y2+=(location[1]-y)*(location[1]-y)
        r=math.sqrt((x2+y2)/(len(locationlist)))
        return r
    def get_rog_disput(self):
        nums=self.set_step(1)
        disput = []
        for num in nums:
            sum_number = 0
            for locations in self.locationList:
                sum_number += self.get_Rog(locations, num)
            sum_number = sum_number / len(self.locationList)
            disput.append(sum_number)
        return disput
    def get_visit_frequency(self,ids):
        temp1=np.array(ids)
        temp2=np.bincount(temp1)
        temp3=temp2.tolist()
        max_value=max(temp3)
        disput=[0]*(max_value+1)
        for i in range(max_value+1):
            disput[i]=temp3.count(i)
        return disput
    def get_visit_frequency_disput(self):
        #得到拜访数量为1，2，3等的数量的点的个数的根部
        disputs = [0] * (int(math.log(len(self.idList[0])) * 3))
        for item in self.idList:
            ids=item
            disput=self.get_visit_frequency(ids)
            for i,value in enumerate(disput):
                if(i<len(disputs)):
                    disputs[i]+=value
        answer_disput=[]
        for temp_disput in disputs:
            answer_disput.append(temp_disput/len(self.idList))
        return answer_disput
    def get_weight(self,ids):
        temp1 = np.array(ids)
        temp2 = np.bincount(temp1)
        temp3 = temp2.tolist()
        temp4=sorted(temp3,reverse=True)
        disput=[]
        for temp in temp4:
            if(temp>0):
                disput.append(temp)
        return disput
    def get_weight_disput(self):
        #得到连接数量的分布
        #得到拜访数量为1，2，3等的数量的点的个数的根部
        disputs = [0] * (int(math.log(len(self.idList[0])) * 3))
        for item in self.idList:
            ids=item
            disput=self.get_weight(ids)
            for i,value in enumerate(disput):
                if(i<len(disputs)):
                    disputs[i]+=value
        answer_disput=[]
        for temp_disput in disputs:
            answer_disput.append(temp_disput/len(self.idList))
        return answer_disput

    def set_step(self,flag):
        if(flag==1):
            num1 = [j for j in range(1, int(math.log(len(self.idList[0]), 2)) + 1)]
            nums = [int(math.pow(2, j)) for j in num1]
            return nums
        if(flag==2):
            num1 = [j for j in range(1, int((len(self.idList[0]) / 100)) + 1)]
            nums = [int(100 * j) for j in num1]
            return nums


    #计算最小二乘的回归函数
    def func(self,p, x):
        k, b = p
        temp_y = []
        for item in x:
            temp_y.append(k * item + b)
        return temp_y
    def error(self,p, x, y, s):
        print s
        temp_answer = []
        tempfunc =self.func(p,x)
        for i in range(0, min(len(tempfunc), len(y))):
            temp_answer.append(tempfunc[i] - y[i])
        return temp_answer
    def cal_leastsq(self,x,y):
        length=min(len(x),len(y))
        s = "Test the number of iteration"
        p0 = [100, 2]
        Para = leastsq(self.error, p0, args=(x, y, s))
        k, b = Para[0]
        return k,b













