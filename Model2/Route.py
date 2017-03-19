import numpy as np
class route:
    route=[]
    time=[]
    state=[]
    grid=[]
    locations=[]
    #store the locations
    #store the time
    #store the state 1:home,2:work,3,commute
    def __init__(self,grid,locations):
        self.route = []
        self.time = []
        self.state = []
        self.locations=locations
        self.grid=grid
    def add_location(self,location):
        for item in location:
            self.route.append(item)
    def add_time(self,times):
        for i in range(len(times)):
            self.time.append(times[i])

    def add_item(self,routes,times,states):
        n=len(routes)
        for i in range(n):
            self.state.append(states)
        self.add_location(routes)
        self.add_time(times)
        print " "
    def set_route_from_route(self,temp_route):
        self.route=temp_route.route
        self.locations=temp_route.locations
        self.state=temp_route.state
        self.grid=temp_route.grid
        self.time=temp_route.time
