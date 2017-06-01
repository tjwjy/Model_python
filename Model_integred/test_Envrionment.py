import Environment
import random
grid_value_list=[]
for i in range(400):
    grid_value_list.append(random.randint(0,10))
Envir=Environment.Social_Envrionment(dimenssion=[20,20],xy_min=[0,0],xy_max=[40,40],grid_value_list=grid_value_list,size=1000)
print (0)