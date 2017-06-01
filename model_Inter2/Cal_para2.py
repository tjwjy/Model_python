#coding=gbk
import Environment
import Cal_para
import data_mid
import  numpy as np
class Cal_para2():
    Envir=Environment.Environment()
    data_mid_list=[]
    def __init__(self,data_mid_list):
        if(data_mid_list):
            self.data_mid_list=data_mid_list
            self.Envir=data_mid_list[0].environment

    #return the frequency rank disput of the simulate
    def get_visit_frequency_disput(self,route=[]):
        data1=[0]*1100
        data2=[0]*400
        if not route:
            route=self.data_mid_list
        for mid in route:
            cal = Cal_para.Cal_para(mid.route, self.Envir)
            temp_data1 = cal.get_visit_frequency_disput()
            temp_data2 = cal.get_visit_frequency_raster_disput()
            for i, item in enumerate(temp_data1):
                data1[i] += item
            for i, item in enumerate(temp_data2):
                data2[i] += item
        data1=[item/len(self.data_mid_list) for item in data1]
        data2=[item/len(self.data_mid_list) for item in data2]
        data1_1 = []
        data2_1 = []
        for i in range(len(data1)):
            item = data1[i]
            for t in range(int(item)):
                data1_1.append(i + 1)
        for i in range(len(data2)):
            item = data2[i]
            for t in range(int(item)):
                data2_1.append(i + 1)
        return data1_1,data2_1

    #####################################################################################################################################
    #cal the attribute of different group
    #group is based on home_work_distance
    #attribute is  discuss later
    def get_group_all_attribute(self, n, attribute_func, dis_func):
        group_tag = self.get_homework_dis_group(n, distant=dis_func)
        group_attribute = []
        for i in range(n):
            temp_attribute = self.get_group_attribute(groupid=i, group_tag=group_tag, attribute_func=attribute_func)
            group_attribute.append(temp_attribute)
        return group_attribute

    def get_homework_dis_group(self,n,distant):
        dis_list=[]
        for item in self.data_mid_list:
            dis=distant(item.important_loc[0],item.important_loc[1])
            dis_list.append(dis)
        temp_dis_list=sorted(dis_list)
        length=int(len(temp_dis_list)/n)*n
        temp_dis_array=np.array(temp_dis_list[0:length]).reshape((n,-1))

        group_tag=[]
        #store the tag of mid_data_list
        for item in dis_list:
            for j,jtem in enumerate(temp_dis_array):
                if(item in jtem):
                    group_tag.append(j)
                    continue
        return group_tag

    def get_group_attribute(self,groupid,group_tag,attribute_func):
        group=[]
        for i,item in enumerate(self.data_mid_list):
            if(i<len(group_tag)):
                if(group_tag[i] == groupid):
                    group.append(item)
        return attribute_func(group)

   ###########################################################################################################################
    #atrribute func ,using in func get_group_all_attribute,
    # aim to cal the different group attribute
    #group base on distance
    def attribute_func_rog_disput(self,group):
        locations=[]
        dis_temp=[]
        for item in group:
            cal = Cal_para.Cal_para(item.route, self.Envir)
            dis,_=cal.get_rog_disput()
            if not dis_temp:
                dis_temp=[i for i in dis]
            else:
                dis_temp=list(map(lambda x,y: x+y,dis_temp,dis))
        dis=[i/len(group) for i in dis_temp]
        return dis


    #get the beta and xmin of diffrent group powerlaw
    #return the point_base and raster_base answer
    def attribute_func_frequency_powerlaw(self,group):
        temp_data_mid=data_mid.data_mid(self.Envir)
        data_1,data_2=self.get_visit_frequency_disput(route=group)
        ## need a func to cal the beta and xmin of the data_1 and data_2
        return data_1

    ##############################################################################################################################







