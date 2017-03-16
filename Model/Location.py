class location():
    loc=[]
    weight=1
    gridId=0
    accomadation=0
    def __init__(self):
        pass
    def set_loc(self,locxy):
        if(len(locxy)==2):
            self.loc=locxy
        else:
            print 'loc is out of form'
    def set_weight(self,weight):
        if(weight>0):
            self.weight=weight
        else:
            print 'loc weight is out of range'
    def set_gridId(self,grid_para):
        self.gridId=grid_para
    def set_accomadation(self,accomadation):
        pass
    def __init__(self,locxy,weight,id):
        self.set_loc(locxy)
        self.set_weight(weight)
        self.set_gridId(id)
