import Person
import Draw2
import Route
import matplotlib.pyplot as plt
args_model=[0,0.6,-0.21]
args_time=[-2,0,5,10000]
args_steps=[-1.80,5]
args_grid=[[20,20],[10,2,10,2],200]
time=100
temp_routeList=[]
person1=Person.normal_person(args_model,args_steps,args_time,time,args_grid=args_grid)
person1.simulate()
fig1=plt.figure(1)
fig2=plt.figure(2)
commute_Route=Route.route(person1.grid,person1.locations)
commute_Route.route=person1.commute_LocationList
draw=Draw2.Draw(commute_Route,[person1.home_loc,person1.work_loc],[fig1,fig2],'commute')

draw.draw_visit_location_number_disput()
draw.draw_location_disput_raster()

fig3=plt.figure(3)
fig4=plt.figure(4)
draw=Draw2.Draw(person1.Personroute,[person1.home_loc,person1.work_loc],[fig3,fig4],"name")

draw.draw_visit_location_number_disput()
draw.draw_location_disput_raster()

