#coding=gbk
import Grid
import powerlow
import math
import random
class Model():
    args_model=[]
    args_step=[]
    args_t=[]
    args_grid=[]
    simulate_time=0
    grid=0
    # 初始化数据
    # args_model包含参数包括S，p，和指数gama
    # args_t包含参数包括时间的指数，上下限,要模拟的结果次数
    # args_step 包含步长的信息，指数，上限
    #args_grid 网格的参数，包括网格长，宽，类型,如果类型为2，即powerlaw类型的则需要传入最后一个powerlaw参数,包括beta，min和max
    steps=[]
    ts=[]
    #在初始化数据给予的情况下逐渐被赋值的参数
    locations=[]
    ids=[]
    frequency=[]
    #需要算出路径后给出的参数
    def __init__(self,args_model,args_step,args_t,args_grid,simulate_time):
        self.args_grid=args_grid
        self.args_model=args_model
        self.args_step=args_step
        self.args_t=args_t
        self.simulate_time=simulate_time
        self.set_t()
        self.set_grid()
    def get_route(self):
        L_place = [item for item in self.grid]  # 没有访问的集合
        L_tempPlace = []  # 访问的集合
        gama = self.args_model[2]
        S = self.args_model[0]
        r = self.args_model[1]
        # 随机选择起始点，并初始化所要用到的循环数据
        postion = random.choice(self.grid)
        L_tempPlace.append(postion)
        L_place.remove(postion)
        S = S + 1
        index = 0
        time_sum = 0
        while ((time_sum < self.simulate_time) & (index < len(self.ts) - 1)):
            tag = r * S ** (gama)
            tag2 = random.random()
            if (tag > tag2):
                # 这时候去探索新的场所代码
                next_postion = self.get_next_position(postion, L_place)
                if (next_postion == 0):
                    continue
                postion = next_postion
                ##更新当前坐标
                L_tempPlace.append(postion)
                L_place.remove(postion)
                S = S + 1
                index = index + 1
            else:
                postion = random.choice(L_tempPlace)
                L_tempPlace.append(postion)
                index = index + 1
            time_sum = time_sum + self.ts[index]
        for tempPlace in L_tempPlace:
            self.locations.append([tempPlace[0],tempPlace[1]])
            self.ids.append(tempPlace[2])
        return L_tempPlace
    def get_next_position(self):
        pass
    def set_grid(self):
        if(len(self.args_grid)!=0):
            if(self.args_grid[2]==1):
                temp=Grid.get_simple_grid(self.args_grid[0],self.args_grid[1])
                self.grid=temp
            if (self.args_grid[2] == 2):
                temp = Grid.get_powerlaw_grid(self.args_grid[0], self.args_grid[1],self.args_grid[3],)
                self.grid = temp
    def set_t(self):
        if(len(self.args_t)!=0):
            self.ts=powerlow.get_float_powerlaw(self.args_t[0],self.args_t[1],self.args_t[2],self.args_t[3])
class ExReModel(Model):
    def get_plist(self,beta1, max_dis, gridDimension):
        disList = []
        for i in range(1, min(max_dis, gridDimension + 1)):
            for j in range(1, min(max_dis, gridDimension + 1)):
                dis = math.sqrt(i * i + j * j)
                if (disList.count(dis) == 0) & (dis < max_dis) & (dis > 0):
                    disList.append(dis)
        pList = []
        disList.sort()
        for dis in disList:
            pList.append(math.pow(dis, beta1))
        return (disList, pList)
    def get_next_position(self,postion,L_place):
        #position 当前位置
        #L_place 备选位置
        max_step=self.args_step[1]
        beta=self.args_step[0]
        gridDimension=self.args_grid[0]
        disList,plist=self.get_plist(beta,max_step,gridDimension)
        #计算在max距离之内的所有的点的概率
        sum = 0
        psumlist = []
        for p in plist:
            sum = sum + p
            psumlist.append(sum)
        p_temp = random.uniform(0, psumlist[len(psumlist) - 1])
        index = -1
        for i, p in enumerate(psumlist):
            if (p > p_temp):
                index = i
                break
        dis = disList[index]
        beta_dis = []
        # 存储距离目标点为dis的所有的点的x，y的差
        for i in range(0, int(dis) + 1):
            for j in range(0, int(dis) + 1):
                if ((i * i + j * j == int(dis * dis)) & (beta_dis.count([i, j]) == 0)):
                    beta_dis.append([i, j])
        if (len(beta_dis) == 0):
            return 0
        else:
            beta = random.choice(beta_dis)
            signals = [[1, 1], [1, -1], [-1, -1], [-1, 1]]
            temp=[]
            for signal in signals:
                x, y = [postion[0] + signal[0] * beta[0], postion[1] + signal[1] * beta[1]]
                index = int((x - 1) * gridDimension + y - 1)
                if(index<self.args_grid[0]*self.args_grid[1]):
                    temp.append(index)
            temp2=[]
            for temp1 in temp:
                if(self.grid[temp1] in L_place):
                    temp2.append(temp1)
            if(len(temp2)>1):
                next_place=random.choice(temp2)
                return self.grid[next_place]
            else:
                return 0
class MyModel(Model):
    def get_next_position(self, postion,L_place):
        # 概率p=size/pow(d.beta)
        beta = self.args_step[0]
        max_step = self.args_step[1]
        gridDimension=self.args_grid[0]
        psum = []
        temp_sum = 0
        temp_grid=[]
        beta_dis=[]
        #在半径内的所有满足条件的x，y之差
        for i in range(0, int(max_step)+1):
            for j in range(0, int(max_step)+1):
                if ((i * i + j * j < int(max_step * max_step)) & (beta_dis.count([i, j]) == 0)):
                    beta_dis.append([i, j])
        signals = [[1, 1], [1, -1], [-1, -1], [-1, 1]]
        temp = []
        #满足半径之内的grid的所有店的index集合
        for signal in signals:
            for beta_dis1 in beta_dis:
                x, y = [postion[0] + signal[0]*beta_dis1[0] , postion[1] + signal[1]*beta_dis1[1] ]
                index = int((x - 1) * gridDimension + y - 1)
                if (index < self.args_grid[0] * self.args_grid[1]):
                    temp.append(index)
        temp2 = []
        #选取其中在未遍历过的所有的点的index
        for temp1 in temp:
            if (self.grid[temp1] in L_place):
                temp2.append(temp1)
        for tempn in temp2:
            dis = math.sqrt(pow((self.grid[tempn][0] - postion[0]), 2) + pow((self.grid[tempn][1] - postion[1]), 2))
            if (dis > 0):
                p = self.grid[tempn][3] * pow(dis,beta)
                temp_grid.append(self.grid[tempn])
                temp_sum = temp_sum + p
                psum.append(temp_sum)
        if(len(psum)>0):
            ptemp = random.uniform(0, psum[len(psum) - 1])
            nextstep = None
            for index, temp in enumerate(psum):
                if (ptemp < temp):
                    nextstep = temp_grid[index]
                    break
            return nextstep
        else:
            return 0



