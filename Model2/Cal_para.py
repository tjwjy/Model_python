#coding=gbk
import numpy as np
import math
from scipy.optimize import leastsq
class Cal_para():
    locationList=[]
    idList=[]
    pointidList=[]
    def __init__(self,route):
        if(len(route)):
            for position in route:
                self.locationList.append([position[0],position[1]])
                self.idList.append(position[2])
            if(len(route[0])):
                for position in route:
                    self.pointidList.append(position[4])
        else:
            pass

    #计算随着时间推移，拜访的位置的数量的变化
    #如果是网格点，则反映的是拜访的点位的数量，如果是栅格数据，则返回的是访问的栅格的数量
    def get_visit_location_number(self, ids, num):
        id_array = np.array(ids[0:num])
        num = np.unique(id_array)
        return len(num)
    def get_visit_location_number_disput(self):
        #得到随着时间的增长，拜访的地点的数量的变化
        nums=self.set_step(2)#选取抽样的步长，2，采用100为步长统计数据
        disput=[]
        for num in nums:
            sum_number=self.get_visit_location_number(self.idList,num)
            disput.append(sum_number)
        return disput

    #计算随着时间推移，栅格数据中拜访的点的个数的变化情况
    #当且仅当数据为栅格数据的情况下，数据才会存在第四位数据
    def get_visit_location_number_raster_disput(self):
        #得到随着时间的增长，拜访的地点的数量的变化
        nums=self.set_step(2)#选取抽样的步长，2，采用100为步长统计数据
        disput=[]
        for num in nums:
            sum_number=self.get_visit_location_number(self.pointidList,num)
            disput.append(sum_number)
        return disput

    #计算随着时间的退役，rog的变化
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
            sum_number = self.get_Rog(self.locationList, num)
            disput.append(sum_number)
        return disput

    #得到循环过后，中心度按照秩排序的分布
    #网格数据代表的是点的访问次数，栅格数据代表的是栅格访问的总数
    def get_weight(self, ids):
        temp1 = np.array(ids)
        temp2 = np.bincount(temp1)
        temp3 = temp2.tolist()
        temp4 = sorted(temp3, reverse=True)
        disput = []
        for temp in temp4:
            if (temp > 0):
                disput.append(temp)
        return disput
    def get_weight_disput(self):
        disputs = [0] * (int(math.log(len(self.idList)) * 3))
        disput=self.get_weight(self.idList)
        for i in range(min(len(disput),len(disputs))):
            disputs[i]=disput[i]
        return disputs

    def get_weight_raster_disput(self):
        disputs = [0] * (int(math.log(len(self.idList)) * 3))
        disput = self.get_weight(self.pointidList)
        for i in range(min(len(disput),len(disputs))):
            disputs[i]=disput[i]
        return disput

    #得到不同的栅格的被拜访量的多少，这个大小在后面的可视化过程中作为该栅格的大小
    #分为栅格和点位本身两个大小的计算方法
    def get_location_size(self,ids,nums):
        temp1 = np.array(ids[0:nums])
        temp2 = np.bincount(temp1)
        temp3 = temp2.tolist()
        return temp3

    def get_location_size_disput(self):
        nums=self.set_step(2)
        locations_weight=[]
        for num in nums:
            locations_weight.append(self.get_location_size(self.idList,num))
        return locations_weight

    def get_location_size_raster_disput(self):
        nums = self.set_step(2)
        locations_weight = []
        for num in nums:
            locations_weight.append(self.get_location_size(self.pointidList, num))
        return locations_weight


    # 计算最小二乘的回归函数
    def func(self, p, x):
        k, b = p
        temp_y = []
        for item in x:
            temp_y.append(k * item + b)
        return temp_y

    def error(self, p, x, y, s):
        print s
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
