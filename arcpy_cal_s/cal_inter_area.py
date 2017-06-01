import matplotlib.pyplot as plt
def cal_similarity(value_list):
    value_x=[]
    value_y=[]
    for value in value_list:
        value_x.append(value[2])
        value_y.append(value[3])
    plt.scatter(value_x,value_y)
plt.show()


def write_txt(path,value_list):
    with (open(path, 'w')) as f:
        temp_str=""
        for value in value_list:
            temp_str=str(value[0])+" "+str(value[1])+" "+str(value[2])+" "+str(value[3])+"\n"
            f.writelines(temp_str)
def read_txt(path):
    value_list=[]
    with open(path,'r') as f:
        temp_str=f.readline()
        temp_str=temp_str.rstrip('\n')
        tag=True
        while(tag):
            temp_str = f.readline()
            temp_str = temp_str.rstrip('\n')
            if(temp_str):
                temp_str = temp_str.split(' ')
                temp_list=[]
                for item in temp_str:
                    temp_list.append(float(item))
            else:
                break
        return value_list

valuelist=[]
for t in range(4):
    temp=[i for i in range(4)]
    valuelist.append(temp)
path='D:/value.txt'
write_txt(path,valuelist)
value=read_txt(path)