#coding=gbk
import Environment
import numpy as np
import math
from scipy.optimize import leastsq
class Cal_para():
    Envir=Environment.Environment()
    PointList=[]
    locationList=[]
    idList=[]
    gridIDList=[]
    tList=[]
    daylast=[]
    def __init__(self,PointList,Environment):
        self.PointList=PointList
        self.Envir=Environment
        if(len(PointList)):
            for position in PointList:
                self.locationList.append(position.location)
                self.idList.append(position.ID)
                self.gridIDList.append(position.gridID)
                self.tList.append(position.t)
            self.daylast=self.set_step(3)
        else:
            pass

    #拜访的locations随着时间的变化
    def get_visit_location_number(self, ids, num):
        id_array = np.array(ids[0:num])
        num = np.unique(id_array)
        return len(num)
    def get_visit_location_number_disput(self):
        #得到随着时间的增长，拜访的地点的数量的变化
        nums=self.daylast#选取抽样的步长，2，采用100为步长统计数据
        disput=[]
        for num in nums:
            sum_number=self.get_visit_location_number(self.idList,num)
            disput.append(sum_number)
        return disput,nums

    # 拜访的gridid的数量随着时间的变化
    def get_visit_location_number_raster_disput(self):
        #得到随着时间的增长，拜访的地点的数量的变化
        nums=self.daylast
        disput=[]
        for num in nums:
            sum_number=self.get_visit_location_number(self.gridIDList,num)
            disput.append(sum_number)
        return disput,nums

    #计算随着时间的退役，rog的变化
    def get_Rog(self,locations,num):
        locationlist=locations[0:num]
        list2=np.unique(locationlist)
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

        nums=self.daylast
        disput = []
        for num in nums:
            # uni_id=np.unique(self.idList[0:num]).tolist()
            # xy=[]
            # for i,id in enumerate(self.idList):
            #     if(id in uni_id):
            #         xy.append(self.grid[i])
            #         uni_id.remove(id)
            sum_number = self.get_Rog(self.locationList, num)
            disput.append(sum_number)
        return disput,nums

    #得到循环过后，中心度按照秩排序的分布
    #网格数据代表的是点的访问次数，栅格数据代表的是栅格访问的总数
    def get_weight(self, ids):
        temp1 = np.array(ids)
        temp2 = np.bincount(temp1)
        temp3 = temp2.tolist()
        temp4=sorted(temp3,reverse=True)
        return temp4
    def get_visit_frequency_disput(self):
        disput=self.get_weight(self.idList)
        return disput

    def get_visit_frequency_raster_disput(self):
        disput=self.get_weight(self.gridIDList)
        return disput

    # 得到不同的栅格的被拜访量的多少，这个大小在后面的可视化过程中作为该栅格的大小
    # 分为栅格和点位本身两个大小的计算方法
    def get_location_size(self,ids,nums):
        temp1 = np.array(ids[0:nums])
        temp2 = np.bincount(temp1)
        temp3 = temp2.tolist()
        return temp3

    def get_location_size_disput(self):
        nums=self.daylast
        locations_weight=[]
        for num in nums:
            locations_weight.append(self.get_location_size(self.idList,num))
        return locations_weight

    def get_location_size_raster_disput(self):
        nums = self.daylast
        locations_weight = []
        for num in nums:
            locations_weight.append(self.get_location_size(self.gridIDList, num))
        return locations_weight


    # 计算最小二乘的回归函数
    def func(self, p, x):
        k, b = p
        temp_y = []
        for item in x:
            temp_y.append(k * item + b)
        return temp_y

    def error(self, p, x, y, s):
        print (s)
        temp_answer = []
        tempfunc = self.func(p, x)
        for i in range(0, min(len(tempfunc), len(y))):
            temp_answer.append(tempfunc[i] - y[i])
        return temp_answer

    def cal_leastsq(self, x, y):
        length = min(len(x), len(y))
        s = "Test the number of iteration"
        p0 = [100, 2]
        Para = leastsq(self.error, p0, args=(x, y, s))
        k, b = Para[0]
        return k, b

    def set_step(self,flag):
        if(flag==1):
            num1 = [j for j in range(1, int(math.log(len(self.idList), 2)) + 1)]
            nums = [int(math.pow(2, j)) for j in num1]
            return nums
        if(flag==2):
            num1 = [j for j in range(1, int((len(self.idList) / 10)) + 1)]
            nums = [int(100 * j) for j in num1]
            return nums
        if(flag==3):
            num1=[]
            for i,t in enumerate(self.tList):
                if(i>0 and i<len(self.tList)-1):
                    if(t>=self.tList[i-1] and self.tList[i+1]<t):
                        print (i)
                        num1.append(i)
            num1.append(len(self.tList)-1)
            return num1


