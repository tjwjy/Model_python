import Environment
import Individual
import Cal_para
import Draw
import matplotlib.pyplot as plt
import powerlaw
args_model=[0.6,-0.21]
args_time=[2,1,10000]
args_steps=[-1.80,5]
args_grid=[[20,20],[10,2,10,2],200]
time=1000
temp_routeList=[]
Envir=Environment.normal_Environment(dimenssion=[20],xy_args=args_grid[1],size=200)
#model=Model5.HomeOrWork_Model(args_model=args_model,args_t=args_time,args_steps=args_steps,environment=Envir,visited_Place=[],homeposition=random.choice(Envir.locations),workposition=random.choice(Envir.locations))
model=Individual.Nomal_Individual(args_model=args_model,args_t=args_time,args_step=args_steps,simulate_time=time,Environment=Envir)
model.simulate()
print (9)
cal=Cal_para.Cal_para(model.data_mid.route,Envir)
dis=cal.get_visit_location_number_disput()
data=model.data_mid.route
data1_1=[]
data2_1=[]
data1=cal.get_visit_frequency_disput()
data2=cal.get_visit_frequency_raster_disput()
for i in range(len(data1)):
    item=data1[i]
    for t in range(item):
        data1_1.append(i)
for i in range(len(data2)):
    item=data2[i]
    for t in range(item):
        data2_1.append(i)
fit=powerlaw.Fit(data1,discrete=True,xmax=1000)
figure1=fit.plot_ccdf(color='b',linewidth=2)
fit.power_law.plot_ccdf(color='b',linestyle='--',ax=figure1)
fit2=powerlaw.Fit(data2,discrete=True,xmax=1000)
fit2.plot_ccdf(color='r',linewidth=2,ax=figure1)
fit2.power_law.plot_ccdf(color='r',linestyle='--',ax=figure1)
print (fit.alpha,fit.sigma,fit2.alpha,fit2.sigma)
print (fit.distribution_compare('power_law','exponential'))
print (fit2.distribution_compare('power_law','exponential'))
plt.show()