import Cal_para
import Cal_para2
import powerlaw
from matplotlib import animation
import IO
import random
import matplotlib.pyplot as plt


def get_location_size_disput(cal):
    nums = [i for i in range(40, 1000, 20)]
    locations_weight = []
    for num in nums:
        locations_weight.append(cal.get_location_size(cal.idList, num))
    return locations_weight


def draw_location_disput(data_mid,cal):
    tag = 0
    fig2 = plt.figure(0)
    locationWeight = get_location_size_disput(cal)
    axes = fig2.add_subplot(1, 1, 1, xlim=(1, 20), ylim=(0, 20))
    ims = []
    for i in range(len(locationWeight)):
        x = []
        y = []
        c = []
        size = []
        for item in data_mid.important_loc:
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
    #anim1.save('basic_animation.mp4',writer="ffmpeg", fps=30, extra_args=['-vcodec', 'libx264'])
    plt.savefig('d://location.png', facecolor="white", transparent=True, dpi=600)
    plt.show()


read=IO.IO()
data_mid=read.read_txt('D:\\Indevidual_normal_Envronment_PointSize_1000_Time_400.txt')
data_mid_draw=random.choice(data_mid)
cal=Cal_para.Cal_para(PointList=data_mid_draw.route,Environment=data_mid_draw.environment)
draw_location_disput(data_mid_draw,cal)

