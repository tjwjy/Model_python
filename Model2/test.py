import Person
args_model=[0,0.6,-0.21]
args_time=[-2,0,5,10000]
args_steps=[-1.80,5]
args_grid=[[20,20],[10,2,10,2],200]
time=100
person1=Person.normal_person(args_model,args_steps,args_time,args_grid,time)
person1.simulate()