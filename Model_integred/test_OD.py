import Environment
import Model_inter
import Cal_para2
import powerlaw
import IO
import matplotlib.pyplot as plt
import math
read=IO.IO()
data_mid=read.read_txt('D:\\Nomal_Individual_HomeAndWork_Seperate_PointSize_400_Time_400.txt')
cal=Cal_para2.Cal_para2(data_mid)
def distance(position1,position2):
    #position1 and 2 are point class
    r1 = math.pow((position1.location[0] - position2.location[0]), 2) + math.pow(
        (position1.location[1] - position2.location[1]), 2)
    return math.sqrt(r1)
OD=cal.get_OD_2_grid(213,210)
t=cal.cal_OD_24hours_disput(OD)
print (t)
figure=plt.figure(1)
x=[i for i in range(25)]
plt.plot(x,t)
plt.show()