import data_mid
import Environment
import Point
class IO():
    mid=None
    def __init__(self,mid=None):
        self.mid=mid
    def write_txt(self,path,flag):
            #write into the document the Environment first
            #when write the txt twice,begin with the route,ignore the envrionment
        if (flag == 0):
            with (open(path, 'w')) as f:
                temp_str='Environment'+'\n'
                f.write(temp_str)
                if(self.mid.environment.grid_dimenssion[0]*self.mid.environment.grid_dimenssion[1]==0):
                    temp_str=0
                else:
                    temp_str=str(self.mid.environment.grid_dimenssion[0])+' '+str(self.mid.environment.grid_dimenssion[1])+'\n'
                f.writelines(temp_str)
                lg = len(self.mid.environment.locations)
                if (lg):
                    for i, item in enumerate(self.mid.environment.locations):
                        temp_str = str(item.location[0]) + " " + str(item.location[1]) + " " + str(
                            item.ID) + " " + str(item.state) + " " + str(item.weight) + " "+str(item.gridID)+"\n"
                        f.writelines(temp_str)
                f.writelines('0\n')
        with (open(path, 'a+')) as f:
            temp_str = 'People' + '\n'
            f.write(temp_str)
            temp_str = str(self.mid.person_tag) + '\n'
            f.write(temp_str)
            if(self.mid.important_loc):
                temp_str = str(self.mid.important_loc) + '\n'
                f.write(temp_str)
            else:
                temp_str=' '+'\n'
                f.writelines(temp_str)
            lg=len(self.mid.route)
            if(lg):
                for i,item in enumerate(self.mid.route):
                    temp_str=str(item.location[0])+" "+str(item.location[1])+" "+str(item.ID)+ " "+str(item.state)+" "+str(item.weight)+ " "+str(item.gridID)+"\n"
                    f.writelines(temp_str)
            f.writelines('0\n')

        return 0
    def read_txt(self,path):
        if self.mid:
            self.mid=None
        temp_envir=Environment.Environment()
        temp_route=[]
        with open(path,'r') as f:
            temp_str=f.readline()
            temp_str=temp_str.rstrip('\n')
            if(temp_str=='Environment'):
                temp_str=f.readline()
                temp_str=temp_str.rstrip('\n')
                temp_str=temp_str.split(' ')
                temp_int=[int(temp_str[0]),int(temp_str[1])]
                temp_envir.set_dimenssion(temp_int)
            tag=True
            while(tag):
                temp_str = f.readline()
                temp_str = temp_str.rstrip('\n')
                if(temp_str!=str(0)):
                    temp_str = temp_str.split(' ')
                    tempx = float(temp_str[0])
                    tempy = float(temp_str[1])
                    ID=int(temp_str[2])
                    state=int(temp_str[3])
                    weight=int(temp_str[4])
                    gridID=int(temp_str[5])
                    point=Point.Point([tempx,tempy],ID=ID,state=state,weight=weight,gridid=gridID)
                    temp_route.append(point)
                else:
                    break
            temp_envir.locations=temp_route

            data_mid_list=[]
            temp_str = f.readline()
            while(temp_str):
                temp_route2 = []
                person_tag = 0
                temp_str = temp_str.rstrip('\n')
                if (temp_str == 'People'):
                    person_tag= int(f.readline().rstrip('\n'))
                temp_str = f.readline()
                important_loc=[]
                temp = temp_str.rstrip('\n')
                if(temp==''or temp_str==''):
                    temp = temp.split(" ")
                    for i in range(int(len(temp_str)/2)):
                        important_loc.append([float(temp[2*i]),float(temp[2*i+1])])
                while (True):
                    temp_str = f.readline()
                    temp_str = temp_str.rstrip('\n')
                    if (temp_str != str(0)):
                        temp_str = temp_str.split(' ')
                        tempx = float(temp_str[0])
                        tempy = float(temp_str[1])
                        ID = int(temp_str[2])
                        state = int(temp_str[3])
                        weight = int(temp_str[4])
                        gridID = int(temp_str[5])
                        point = Point.Point([tempx, tempy], gridid=gridID, ID=ID, state=state, weight=weight)
                        temp_route2.append(point)
                    else:
                        break
                temp_mid=data_mid.data_mid(temp_envir,person_tag=person_tag,important_loc=important_loc)
                temp_mid.add_location(temp_route2)
                data_mid_list.append(temp_mid)
                temp_str = f.readline()
            return data_mid_list


# io=IO(None)
# data_mi=io.read_txt('D:/document.txt')
# print (0)
