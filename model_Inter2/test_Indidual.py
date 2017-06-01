import Environment
import Model_inter
import Cal_para2
import powerlaw
import IO
import matplotlib.pyplot as plt
import math
read=IO.IO()
data_mid=read.read_txt('D:\\Indevidual_normal_Envronment_PointSize_1000_Time_400.txt')
cal=Cal_para2.Cal_para2(data_mid)
def distance(position1,position2):
    #position1 and 2 are point class
    r1 = math.pow((position1.location[0] - position2.location[0]), 2) + math.pow(
        (position1.location[1] - position2.location[1]), 2)
    return math.sqrt(r1)

#######################################################################################################################################
#cal the raster_base and point_base visit frequency with rank
#compare the beta in the same figure

# data1_1,data2_1=cal.get_visit_frequency_disput()
# fit=powerlaw.Fit(data1_1,discrete=True,xmin=1)
# figure1=fit.plot_pdf(color='b',linewidth=2)
# fit.power_law.plot_pdf(color='b',linestyle='--',ax=figure1)
# fit2=powerlaw.Fit(data2_1,discrete=True,xmin=1)
# fit2.plot_pdf(color='r',linewidth=2,ax=figure1)
# fit2.power_law.plot_pdf(color='r',linestyle='--',ax=figure1)
# print (fit.alpha,fit.sigma,fit2.alpha,fit2.sigma)
# print (fit.distribution_compare('power_law','truncated_power_law', normalized_ratio=True))
# print (fit2.distribution_compare('power_law','truncated_power_law', normalized_ratio=True))
# plt.show()
# print (00)

##########################################################################################################################################
#caculate different group the rog disput with time
#to see that how home_work distance affects the rog
#compare the distance subtract the mean value

# attributes=cal.get_group_all_attribute(3,cal.attribute_func_rog_disput,distance)
# x=range(400)
# y1=attributes[0]
# y2=attributes[1]
# y3=attributes[2]
# figure=plt.figure(1)
# plot1=plt.plot(x,y1,color='b')
# plot2=plt.plot(x,y2,color='r')
# plot3=plt.plot(x,y3,color='g')
# plt.title('ROG of different home_work distance')
# plt.xlabel('time(day)')
# plt.ylabel('ROG')
# plt.legend([plot1,plot2,plot3],('max','mid','min'))
#
# x=range(400)
# mean1=float(sum(attributes[0])/len(attributes[0]))
# y1=[i/mean1 for i in attributes[0]]
# mean1=float(sum(attributes[1])/len(attributes[1]))
# y2=[i/mean1 for i in attributes[1]]
# mean1=float(sum(attributes[2])/len(attributes[2]))
# y3=[i/mean1 for i in attributes[2]]
# figure=plt.figure(2)
# plot1=plt.plot(x,y1,color='b')
# plot2=plt.plot(x,y2,color='r')
# plot3=plt.plot(x,y3,color='g')
# plt.title('ROG of different home_work distance(subtract mean)')
# plt.xlabel('time(day)')
# plt.ylabel('ROG')
# plt.legend([plot1,plot2,plot3],('max','mid','min'))
# plt.show()
# print (0)
#########################################################################################################################################
#calculate different group the visit frequency disput with rank
#if it is analysis base on point,do nothing like this
#else let Cal_para2.attribute_func_frequency_powerlaw return data_2
#then you can analysis base on raster

attributes=cal.get_group_all_attribute(3,cal.attribute_func_frequency_powerlaw,distance)
x=range(400)
y1=attributes[0]
y2=attributes[1]
y3=attributes[2]
fit1=powerlaw.Fit(y1,discrete=True,xmin=1)
fit2=powerlaw.Fit(y2,discrete=True,xmin=1)
fit3=powerlaw.Fit(y3,discrete=True,xmin=1)
figure1=fit1.plot_pdf(color='b',linewidth=2)
fit1.power_law.plot_pdf(color='b',linestyle='--',ax=figure1)
fit2.plot_pdf(color='r',linewidth=2,ax=figure1)
fit2.power_law.plot_pdf(color='r',linestyle='--',ax=figure1)
fit3.plot_pdf(color='g',linewidth=2,ax=figure1)
fit3.power_law.plot_pdf(color='g',linestyle='--',ax=figure1)
plt.xlabel('rank')
plt.ylabel('visit_frequency')
plt.title('visit frequency disput of different home_work distance')
plt.show()

##############################################################################################################################################

