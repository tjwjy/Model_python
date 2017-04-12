import networkx as nx
import numpy as np
import random as rd
import Point
class NetWork():
    nx_graph=nx.Graph()
    nx_edges=[]
    nx_nodes=[]
    location=[]
    def __init__(self):
        self.nx_nodes=[]
        self.nx_graph=nx.Graph()
        self.nx_edges=[]
        self.location=[]

    def read_shpfile(self,Path):
        #read the shapefile
        nx_load_shp=nx.read_shp('E:/data/bj/road_unsplit.shp')
        self.nx_graph=nx_load_shp.to_undirected()
        #find the largest connected subgraph
        nx_list_subgraph=list(nx.connected_component_subgraphs(nx_load_shp.to_undirected()))[0]
        # self.nx_graph=nx_list_subgraph

        self.nx_nodes=np.array(nx_list_subgraph.nodes())
        self.nx_edges=np.array(nx_list_subgraph.edges())
        nx.write_shp(nx_list_subgraph,'C:/ww')
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
        answer=[]
        for i in range(n):
            temp_x=rd.normalvariate(mux,sigmax)
            temp_y=rd.normalvariate(muy,sigmay)
            self.location.append([temp_x,temp_y])
            n_near=self.get_nearest_n([temp_x,temp_y],self.nx_nodes,4)
            temp_point=Point.Point([temp_x,temp_y],0,i,n_near)
            answer.append(temp_point)
        return answer

    def chose_candidate_points(self,max_dis,anchor_point,locations):
        dis=[]
        point=[]
        for i in range(len(anchor_point.Neareast_point)):
            point1=anchor_point.Neareast_point[i]
            point2=anchor_point.location
            #print (self.nx_graph.number_of_nodes())
            self.nx_graph.add_edge(tuple(point1.tolist()),tuple(point2),distance=0)
            #print(self.nx_graph.number_of_nodes())

        for item in locations:
            if((pow(item.location[0]-anchor_point.location[0],2)+pow(item.location[1]-anchor_point.location[1],2)<max_dis*max_dis)):
                for i in range(len(item.Neareast_point)):
                    point1 = item.Neareast_point[i]
                    point2 = item.location
                    # print (self.nx_graph.number_of_nodes())
                    self.nx_graph.add_edge(tuple(point1.tolist()), tuple(point2), distance=0)
                    # print(self.nx_graph.number_of_nodes())
                dis.append(nx.shortest_path_length(self.nx_graph,source=tuple(anchor_point.location),target=tuple(item.location),weight='distance'))
                point.append(item)
        return point,dis

    def chose_candidate_points_2(self,max_dis,anchor_point1,anchor_point2,locations):
        dis=[]
        point=[]
        temp_grap=self.nx_graph.copy()
        for i in range(len(anchor_point2.Neareast_point)):
            point1=anchor_point2.Neareast_point[i]
            point2=anchor_point2.location
            #print (self.nx_graph.number_of_nodes())
            temp_grap.add_edge(tuple(point1.tolist()),tuple(point2),distance=0)
            #print(self.nx_graph.number_of_nodes())

        for i in range(len(anchor_point1.Neareast_point)):
            point1=anchor_point1.Neareast_point[i]
            point2=anchor_point1.location
            #print (self.nx_graph.number_of_nodes())
            temp_grap.add_edge(tuple(point1.tolist()),tuple(point2),distance=0)
            #print(self.nx_graph.number_of_nodes())

        for item in locations:
            if((pow(item.location[0]-anchor_point1.location[0],2)+pow(item.location[1]-anchor_point1.location[1],2)<max_dis*max_dis)):
                if ((pow(item.location[0] - anchor_point2.location[0], 2) + pow(
                            item.location[1] - anchor_point2.location[1], 2) < max_dis * max_dis)):
                    for i in range(len(item.Neareast_point)):
                        point1 = item.Neareast_point[i]
                        point2 = item.location
                        # print (self.nx_graph.number_of_nodes())
                        temp_grap.add_edge(tuple(point1.tolist()), tuple(point2), distance=0)
                        # print(self.nx_graph.number_of_nodes())
                    dis1=(nx.shortest_path_length(temp_grap,source=tuple(anchor_point1.location),target=tuple(item.location),weight='distance'))
                    dis2 = (nx.shortest_path_length(temp_grap, source=tuple(anchor_point1.location),
                                                    target=tuple(item.location), weight='distance'))
                    dis.append(dis1+dis2)
                    point.append(item)
        return point,dis

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