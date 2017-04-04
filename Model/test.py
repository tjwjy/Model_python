#coding=gbk
from matplotlib import pyplot as  plt
import Model2
import Cal_para
args_model=[0,0.6,-0.21]
args_time=[-1.55,0,17,10000]
args_steps=[-1.80,5]
args_grid=[[20,20],[10,2,10,2],200]
time=10000
route=[]
newModel=Model2.Normal_Model(args_model=args_model, args_grid=args_grid, args_step=args_steps, args_t=args_time,simulate_time=time)
route=newModel.get_route()
draw=Cal_para.draw(route, newModel)
#draw.draw_visit_location_number_disput()
#draw.draw_location_disput()
draw.draw_location_disput_raster()
