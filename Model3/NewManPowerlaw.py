import random
import numpy as np
import matplotlib.pyplot as plt
import math
r=[]
for i in range(100000):
    r.append(random.random())
power=[]
for r1 in r:
    temp=3*pow((1-r1),-1/(.2-1))
    power.append(temp)
a=0
mins=min(power)
for i in range(len(power)):
    a+=math.log(power[i]/mins)
a1=1+len(power)*(1/a)
print (a1)
plt.hist(power)
plt.show()