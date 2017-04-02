import numpy as  np
import powerlaw as plw
import scipy.stats
import matplotlib.pyplot as plt
import random as rdn
import math
def create_powerlaw(a,xmin,n):
    r_list=[]
    for i in range(n):
        r_list.append(rdn.random())
    power=[]
    for r_item in r_list:
        power.append(middle_fuction_in_powerlaw(r_item,a,xmin))
    for i in range(len(power)):
        a += math.log(power[i] / xmin)
    a1 = 1 + len(power) * (1 / a)
    print (a1)
    return power
def middle_fuction_in_powerlaw(r,a,min):
    x=pow(1-r,-1/(a-1))
    x=min*x
    return x

test_value=create_powerlaw(2,3,1000000)
hist=np.arange(3,20,0.5)
# fit=plw.Fit(test_value,xmin=3)
# print (fit.alpha)
# print (fit.sigma)
# plw.plot_pdf(test_value)
plt.hist(test_value,bins=hist)
# fit.power_law.plot_pdf()
plt.show()