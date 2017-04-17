import Environment
import Model_inter
import Cal_para2
import powerlaw
import IO
import matplotlib.pyplot as plt
read=IO.IO()
data_mid=read.read_txt('D:\\normal_Envronment_PointSize_1000_Time_10000.txt')
cal=Cal_para2.Cal_para2(data_mid)
data1_1,data2_1=cal.get_visit_frequency_disput()
fit=powerlaw.Fit(data1_1,discrete=True,xmin=1)
figure1=fit.plot_pdf(color='b',linewidth=2)
fit.power_law.plot_pdf(color='b',linestyle='--',ax=figure1)
fit2=powerlaw.Fit(data2_1,discrete=True,xmin=1)
fit2.plot_pdf(color='r',linewidth=2,ax=figure1)
fit2.power_law.plot_pdf(color='r',linestyle='--',ax=figure1)
print (fit.alpha,fit.sigma,fit2.alpha,fit2.sigma)
print (fit.distribution_compare('power_law','truncated_power_law', normalized_ratio=True))
print (fit2.distribution_compare('power_law','truncated_power_law', normalized_ratio=True))
plt.show()
print (00)

