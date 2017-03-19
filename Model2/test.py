import Person
import Draw2
import Route
args_model=[0,0.6,-0.21]
args_time=[-2,0,5,10000]
args_steps=[-1.80,5]
args_grid=[[20,20],[10,2,10,2],200]
time=100
person1=Person.normal_person(args_model,args_steps,args_time,args_grid,time)
person1.simulate()
draw=Draw2.Draw(person1.Personroute,[person1.home_loc,person1.work_loc])

# commute_Route=Route.route(person1.grid,person1.locations)
# commute_Route.route=person1.commute_LocationList
# draw=Draw2.Draw(commute_Route,[person1.home_loc,person1.work_loc])

draw.draw_visit_location_number_disput()
draw.draw_location_disput_raster()