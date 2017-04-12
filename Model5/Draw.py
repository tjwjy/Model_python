
import Cal_para
from matplotlib import pyplot as plt
import math
import numpy as np
from matplotlib import animation
import powerlaw
class Draw():
    cal = []
    visit_location_number_disput = []
    visite_weight_disput = []
    rog_disput = []
    important_place=[]
    fig1=plt.figure(1)
    fig2=plt.figure(2)
    filename=''
    def __init__(self, cal,important_place=[],fig=[],filename='fig'):
        self.filename=filename
        self.cal =cal
        self.visit_location_number_disput = self.cal.get_visit_location_number_disput()
        self.visite_weight_disput = self.cal.get_visit_frequency_disput()
        self.rog_disput =  self.cal.get_rog_disput()
        self.important_place=important_place
        if(len(fig)==0):
            self.fig1 = plt.figure(1)
            self.fig2 = plt.figure(2)
        else:
            self.fig1=fig[0]
            self.fig2=fig[1]
        print (self.visit_location_number_disput)
        print (self.visite_weight_disput)
        print (self.rog_disput)

    def draw_visit_location_number_disput(self):
        ##绘图
        fig = self.fig1
        axes = fig.add_subplot(2, 2, 1, xlim=(1, 100), ylim=(0, 600))
        y,z= self.visit_location_number_disput
        x = [i for i in range(len(self.cal.daylast))]
        axes.set_xlabel("time")
        axes.set_ylabel("number of place")
        #axes.set_title("number of place distribution")
        axes.plot(x, y)
        axes2 = fig.add_subplot(2, 2, 2, xlim=(0,100), ylim=(0, 100))
        line, = axes.plot([], [], lw=2)
        y = self.visite_weight_disput
        x = [i for i in range(len(self.visite_weight_disput))]
        axes2.plot(x, y)
        axes2.set_xlabel("range")
        axes2.set_ylabel("visit frequency")
        #axes2.set_title("visit frequency distribution")
        axes3 = fig.add_subplot(2, 2, 3, xlim=(1, 100), ylim=(0, 4))
        line, = axes.plot([], [], lw=2)
        y,z = self.rog_disput
        x = [i for i in range(len(self.cal.daylast))]
        axes3.plot(x, y)
        axes3.set_xlabel("time")
        axes3.set_ylabel("ROG")
        #axes3.set_title("ROG distribution")
        axes4 = fig.add_subplot(2, 2, 4, xlim=(0, 2.5), ylim=(0, 4))
        visite_frequency_plus1 = [i + 1 for i in self.visite_weight_disput]
        y = [math.log10(i) for i in visite_frequency_plus1]
        x = [math.log10(i) for i in range(1, len(self.visite_weight_disput) + 1)]
        axes4.scatter(x,y)
        temp=powerlaw.Fit([i for i in visite_frequency_plus1])
        # k=-temp.alpha+1
        # b=math.log10(temp.n_tail)
        #print (k)
        k, b = self.cal.cal_leastsq(x, y)
        print(k)
        xtemp = np.linspace(0, math.log(len(self.visite_weight_disput) + 1), 1000)
        ytemp = k * xtemp + b
        axes4.plot(xtemp, ytemp)
        axes4.set_xlabel("time")
        axes4.set_ylabel("number of place")
        # 比较不同栅格拜访数量的大小

    def draw_location_disput(self,data_mid):
        tag = 0
        fig2 = self.fig2
        locationWeight = self.cal.get_location_size_disput()
        axes = fig2.add_subplot(1, 1, 1, xlim=(1, 20), ylim=(0, 20))
        ims = []
        for i in range(len(locationWeight)):
            x = []
            y = []
            c = []
            size = []
            for item in self.important_place:
                x.append(item.location[0])
                y.append(item.location[1])
                c.append('r')
                size.append(100)
            for j in range(len(locationWeight[i])):
                x.append(data_mid.environment.locations[j].location[0])
                y.append(data_mid.environment.locations[j].location[1])
                c.append('b')
            size += locationWeight[i]
            im = plt.scatter(x, y, s=size, c=c)
            ims.append([im])
            # if(i%10==0):
            #     plt.savefig('D:/figname'+str(i)+".png", facecolor="white", transparent=True, dpi=600)
        anim1 = animation.ArtistAnimation(fig2, ims, interval=500, blit=True)
        plt.savefig('d:/'+self.filename+'location.png', facecolor="white",transparent=True,dpi=600)
        plt.show()

        # 比较不同的点被访问的数量的大小

    def draw_location_disput_raster(self,data_mid):
        tag = 0
        fig2 = self.fig2
        locationWeight = self.cal.get_location_size_raster_disput()
        axes = fig2.add_subplot(1, 1, 1, xlim=(1, 20), ylim=(0, 20))
        ims = []
        for i in range(len(locationWeight)):
            x = []
            y = []
            c = []
            size = []
            for item in self.important_place:
                x.append(item.location[0])
                y.append(item.location[1])
                c.append('r')
                size.append(100)
            for j in range(len(locationWeight[0])):
                x.append(data_mid.environment.locations[j].location[0])
                y.append(data_mid.environment.locations[j].location[1])
                c.append('b')
            size += locationWeight[i]
            im = plt.scatter(x, y, s=size, c=c)
            ims.append([im])
            # if(i%10==0):
            #     plt.savefig('D:/figname'+str(i)+".png", facecolor="white", transparent=True, dpi=600)
        anim1 = animation.ArtistAnimation(fig2, ims, interval=500, blit=True)
        plt.savefig('d:/'+self.filename+'location.png', facecolor="white",transparent=True,dpi=600)
        plt.show()

