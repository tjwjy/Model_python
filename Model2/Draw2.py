#coding=gbk
import Cal_para
from matplotlib import pyplot as plt
import math
import numpy as np
from matplotlib import animation
import Route
class Draw():
    route=Route.route([],[])
    cal = Cal_para.Cal_para([])
    visit_location_number_disput = []
    visite_weight_disput = []
    rog_disput = []
    important_place=[]

    def __init__(self, route,important_place=[]):
        self.route.set_route_from_route(route)
        self.important_place=important_place
        self.cal = Cal_para.Cal_para(route.route)
        self.visit_location_number_disput = self.cal.get_visit_location_number_disput()
        self.visite_weight_disput = self.cal.get_weight_disput()
        self.rog_disput = self.cal.get_rog_disput()
        print self.visit_location_number_disput
        print self.visite_weight_disput
        print self.rog_disput

    def draw_visit_location_number_disput(self):
        ##绘图
        fig = plt.figure(1)
        axes = fig.add_subplot(2, 2, 1, xlim=(1, 100 * len(self.visit_location_number_disput)), ylim=(0, 600))
        line, = axes.plot([], [], lw=2)
        y = self.visit_location_number_disput
        x = [(i * 100) for i in range(len(self.visit_location_number_disput))]
        axes.set_xlabel("time")
        axes.set_ylabel("number of place")
        #axes.set_title("number of place distribution")
        axes.plot(x, y)
        axes2 = fig.add_subplot(2, 2, 2, xlim=(0, len(self.visite_weight_disput)), ylim=(0, 100))
        line, = axes.plot([], [], lw=2)
        y = self.visite_weight_disput
        x = [i for i in range(len(self.visite_weight_disput))]
        axes2.plot(x, y)
        axes2.set_xlabel("range")
        axes2.set_ylabel("visit frequency")
        #axes2.set_title("visit frequency distribution")
        axes3 = fig.add_subplot(2, 2, 3, xlim=(1, len(self.rog_disput)), ylim=(0, 2))
        line, = axes.plot([], [], lw=2)
        y = self.rog_disput
        x = [pow(2,i) for i in range(len(self.rog_disput))]
        axes3.plot(x, y)
        axes3.set_xlabel("time")
        axes3.set_ylabel("ROG")
        #axes3.set_title("ROG distribution")
        axes4 = fig.add_subplot(2, 2, 4, xlim=(0, 2), ylim=(0, 4))
        line, = axes.plot([], [], lw=2)
        visite_frequency_plus1 = [i + 1 for i in self.visite_weight_disput]
        y = [math.log10(i) for i in visite_frequency_plus1]
        x = [math.log10(i) for i in range(1, len(self.visite_weight_disput) + 1)]
        axes4.scatter(x, y, s=35)
        k, b = self.cal.cal_leastsq(x, y)
        xtemp = np.linspace(0, math.log(len(self.visite_weight_disput) + 1), 1000)
        ytemp = k * xtemp + b
        axes4.plot(xtemp, ytemp)
        axes4.set_ylabel("try")
        print k, b
        axes4.set_xlabel("time")
        axes4.set_ylabel("number of place")
        plt.show()
        # 比较不同栅格拜访数量的大小

    def draw_location_disput(self):
        tag = 0
        fig2 = plt.figure(2)
        locationWeight = self.cal.get_location_size_disput()
        axes = fig2.add_subplot(1, 1, 1, xlim=(1, 20), ylim=(0, 20))
        ims = []
        for i in range(len(locationWeight)):
            x = []
            y = []
            for j in range(len(locationWeight[0])):
                y.append(self.route.grid[j][0])
                x.append(self.route.grid[j][1])
            size = locationWeight[i]
            im = plt.scatter(x, y, s=size)
            ims.append([im])
        anim1 = animation.ArtistAnimation(fig2, ims, interval=500, blit=True)
        plt.show()

        # 比较不同的点被访问的数量的大小

    def draw_location_disput_raster(self):
        tag = 0
        fig2 = plt.figure(2)
        locationWeight = self.cal.get_location_size_raster_disput()
        axes = fig2.add_subplot(1, 1, 1, xlim=(1, 20), ylim=(0, 20))
        ims = []
        for i in range(len(locationWeight)):
            x = []
            y = []
            c = []
            size = []
            for item in self.important_place:
                x.append(item[0])
                y.append(item[1])
                c.append('r')
                size.append(100)
            for j in range(len(locationWeight[0])):
                x.append(self.route.locations[j][0])
                y.append(self.route.locations[j][1])
                c.append('b')
            size += locationWeight[i]
            im = plt.scatter(x, y, s=size, c=c)
            ims.append([im])
        anim1 = animation.ArtistAnimation(fig2, ims, interval=500, blit=True)
        plt.show()

        def draw_Commute_location_disput_raster(self):
            tag = 0
            fig2 = plt.figure(2)
            locationWeight = self.cal.get_location_size_raster_disput()
            axes = fig2.add_subplot(1, 1, 1, xlim=(1, 20), ylim=(0, 20))
            axes.set_title("visit place distirbution")
            ims = []
            for i in range(len(locationWeight)):
                x = []
                y = []
                c = []
                size = []
                for item in self.important_place:
                    x.append(item[0])
                    y.append(item[1])
                    c.append('r')
                    size.append(100)
                for j in range(len(locationWeight[0])):
                    x.append(self.route.locations[j][0])
                    y.append(self.route.locations[j][1])
                    c.append('b')
                size += locationWeight[i]
                im = plt.scatter(x, y, s=size, c=c)
                ims.append([im])
            anim1 = animation.ArtistAnimation(fig2, ims, interval=500, blit=True)
            plt.show()