import networkx as nx
import numpy as np
import random as rd
class NetWork():
    nx_graph=nx.Graph()
    nx_edges=[]
    nx_nodes=[]
    location=[]
    def read_shpfile(self,Path):
        #read the shapefile
        nx_load_shp=nx.read_shp('E:/data/bj/streets_5huan_new.shp')
        #find the largest connected subgraph
        nx_list_subgraph=list(nx.connected_component_subgraphs(nx_load_shp.to_undirected()))[0]

        self.nx_nodes=np.array(nx_list_subgraph.nodes())
        self.nx_edges=np.array(nx_list_subgraph.edges())
        print (0)

    def add_positon_normal(self,n,parameter=.3):
        max_x=self.nx_nodes[:,0].max()
        max_y=self.nx_nodes[:,1].max()
        min_x=self.nx_nodes[:,0].min()
        min_y=self.nx_nodes[:,1].min()
        print ([max_x,min_x,max_y,min_y])
        mux=(max_x+min_x)/2
        sigmax=(max_x-min_x)*parameter
        muy=(max_y+min_y)/2
        sigmay=(max_y-min_y)*parameter
        for i in range(n):
            temp_x=rd.normalvariate(mux,sigmax)
            temp_y=rd.normalvariate(muy,sigmay)
            self.location.append([temp_x,temp_y])
            n_near=self.get_nearest_n([temp_x,temp_y],self.nx_nodes,4)
            print (0)

    def get_nearest_n(self,location,pointlist,n):
        dist=[]
        answer=[]
        for point in pointlist:
            dis=pow((point[0]-location[0]),2)+pow((point[1]-location[1]),2)
            dist.append(dis)
        dist2=sorted(dist)
        for i,item in enumerate(dist):
            if(item in dist2[0:n]):
                answer.append(pointlist[i])
        return answer



nt=NetWork()
nt.read_shpfile(0)
nt.add_positon_normal(12)