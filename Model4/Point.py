#coding=gbk
class Point():
    #store the x,y for point
    location=[]
    #gridid ,store the gridID for the Point to make search easy
    gridID=-1
    # weight, the importance of the point. the higher,the more probability the point will visit
    weight=-1
    #ID, the points id. not equal to the gridid
    ID=-1
    #t,the time the point be visit
    t=0
    #state,the proceduer(home,work,commuting)the point was visited
    state=0
    def __init__(self,location,gridid,ID,t=0,state=0,weight=1):
        self.location=location
        self.gridID=gridid
        self.ID=ID
        self.t=t
        self.state=state
        self.weight=weight