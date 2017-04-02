import Point
import Environment
class data_mid():
    route=[]
    #pointList show the people routin
    person_tag=0
    #people tag
    environment=Environment.Environment()
    #environment
    def __init__(self,envrionment,person_tag):
        self.person_tag=person_tag
        self.environment.set_environment(envrionment)
        self.route=[]

    def add_location(self, pointList):
        for item in pointList:
            self.route.append(item)
    def set_data_from_data(self, data_mid):
        self.route=data_mid.route
        self.person_tag=data_mid.person_tag
        self.environment=data_mid.environment
