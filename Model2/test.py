import Person
import Draw2
import Route
args_model=[0,0.6,-0.21]
args_time=[-2,0,5,10000]
args_steps=[-1.80,5]
args_grid=[[20,20],[10,2,10,2],200]
time=10
temp_routeList=[]
for i in range(0,10):
    person1=Person.normal_person(args_model,args_steps,args_time,args_grid,time)
    person1.simulate()
    temp_routeList.append(person1.Personroute)
temp_routeClass=Route.route(temp_routeList[0].grid,temp_routeList[1].locations)
for item in temp_routeList:
    temp_routeClass.add_item(routes=item.route,times=item.time,states=item.state)

draw=Draw2.Draw(temp_routeClass)

# commute_Route=Route.route(person1.grid,person1.locations)
# commute_Route.route=person1.commute_LocationList
# draw=Draw2.Draw(commute_Route,[person1.home_loc,person1.work_loc])

draw.draw_visit_location_number_disput()
draw.draw_location_disput_raster()