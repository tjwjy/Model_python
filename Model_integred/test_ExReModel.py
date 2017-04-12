import Environment
import Model_inter
import Cal_para
import powerlaw
import write_txt
import matplotlib.pyplot as plt
args_model=[0.6,-0.21]
args_time=[2,1,10000]
args_steps=[-1.80,5]
args_grid=[[20,20],[10,2,10,2],200]
time=100
PointSize=1000
temp_routeList=[]
Envir=Environment.normal_Environment(dimenssion=[20],xy_args=args_grid[1],size=PointSize)
data1=[0]*PointSize
data2=[0]*PointSize
for i in range(1,10):
    exremodel=Model_inter.ExReModel(args_t=args_time,args_model=args_model,args_steps=args_steps,environment=Envir,visited_Place=[])
    exremodel.set_tbegin(0,1000)
    route,mid=exremodel.get_route()
    print (i)
    cal=Cal_para.Cal_para(mid.route,Envir)
    temp_data1 = cal.get_visit_frequency_disput()
    temp_data2 = cal.get_visit_frequency_raster_disput()
    for i,item in enumerate(temp_data1):
        data1[i]+=item
    for i,item in enumerate(temp_data2):
        data2[i]+=item
print (1)
data1=[i/100 for i in data1]
data2=[i/100 for i in data2]
data1_1=[]
data2_1=[]

for i in range(len(data1)):
    item=data1[i]
    for t in range(int(item)):
        data1_1.append(i+1)
for i in range(len(data2)):
    item=data2[i]
    for t in range (int(item)):
        data2_1.append(i+1)
fit=powerlaw.Fit(data1_1,discrete=True,xmin=1)
figure1=fit.plot_pdf(color='b',linewidth=2)
fit.power_law.plot_pdf(color='b',linestyle='--',ax=figure1)
fit2=powerlaw.Fit(data2_1,discrete=True,xmin=1)
fit2.plot_pdf(color='r',linewidth=2,ax=figure1)
fit2.power_law.plot_pdf(color='r',linestyle='--',ax=figure1)
print (fit.alpha,fit.sigma,fit2.alpha,fit2.sigma)
print (fit.distribution_compare('power_law','truncated_power_law'))
print (fit2.distribution_compare('power_law','truncated_power_law'))
plt.show()
write=write_txt.IO(mid)
write.write_txt('D:\document.txt',0)
