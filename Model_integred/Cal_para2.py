#coding=gbk
import Environment
import Cal_para
class Cal_para2():
    Envir=Environment.Environment()
    data_mid_list=[]
    def __init__(self,data_mid_list):
        if(data_mid_list):
            self.data_mid_list=data_mid_list
            self.Envir=data_mid_list[0].environment

    #return the frequency rank disput of the simulate
    def get_visit_frequency_disput(self):
        data1=[0]*1100
        data2=[0]*400
        for mid in self.data_mid_list:
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
