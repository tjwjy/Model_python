import arcpy
from arcpy import env
env.workspace='E:/data/shenzhen/shenzhen.mdb'
field_id="DIS"
pointFeature='shenzhen_random_split'
outFeature="temp_feature"
with arcpy.da.SearchCursor(pointFeature,[field_id,"SHAPE@XY"]) as curse:
    xyList=[]
    Id_list=[]
    pn=arcpy.Point()
    for row in curse:
        Id_list.append(row[0])
        pn=row[1]
        xyList.append([pn[0],pn[1]])
    del row,curse
featureList = []
field_list=[]
temp_point=arcpy.Point()
for pn in xyList:
    for pn1 in xyList:
        if(pn!=pn1):
            temp_point.X=pn[0]
            temp_point.Y=pn[1]
            array=arcpy.Array()
            array.add(temp_point)
            temp_point.X=pn1[0]
            temp_point.Y=pn1[1]
            array.add(temp_point)
            polyLine=arcpy.Polyline(array)
            featureList.append(polyLine)
            field_list.append([Id_list[xyList.index(pn)],Id_list[xyList.index(pn1)]])

############################################################################

temp_feature=arcpy.CreateScratchName('temp',data_type='FeatureClass ')
arcpy.CopyFeatures_management(featureList,temp_feature)
arcpy.MakeFeatureLayer_management(temp_feature,'lyr')
arcpy.AddField_management('lyr',field_name='p1',field_type='SHORT')
arcpy.AddField_management('lyr',field_name='p2',field_type='SHORT')
arcpy.AddField_management('lyr',field_name='flux',field_type='DOUBLE')
if arcpy.Exists(outFeature):
    arcpy.Delete_management(outFeature)
arcpy.CopyFeatures_management('lyr',outFeature)
arcpy.Delete_management(temp_feature)

##########################################################################


####
with arcpy.da.UpdateCursor(outFeature,['p1','p2']) as curse:
    i=0
    for row in curse:
        row[0]=field_list[i][0]
        row[1]=field_list[i][1]
        curse.updateRow(row)
        i+=1
    del curse,row
####
print (0)
