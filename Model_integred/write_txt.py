import data_mid
import Environment
class IO():
    mid=None
    def __init__(self,mid):
        self.mid=mid
    def write_txt(self,path,flag):
        with (open(path,'w')) as f:
            #write into the document the Environment first
            if (flag == 0):
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
                            item.ID) + " " + " " + str(item.state) + " " + str(item.weight) + "\n"
                        f.writelines(temp_str)
                f.writelines('0\n')
            with (open(path, 'a')) as f:
                temp_str = 'People' + '\n'
                f.write(temp_str)
                temp_str = str(self.mid.person_tag) + '\n'
                f.write(temp_str)
                lg=len(self.mid.route)
                if(lg):
                    for i,item in enumerate(self.mid.route):
                        temp_str=str(item.location[0])+" "+str(item.location[1])+" "+str(item.ID)+" "+" "+str(item.state)+" "+str(item.weight)+"\n"
                        f.writelines(temp_str)
                f.writelines('0\n')
        return 0


