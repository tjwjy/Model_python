import arcpy
from arcpy import env
def get_buffer_list():
    env.workspace='E:/data/shenzhen/shenzhen.mdb'
    pointFeature='shenzhen_random_split'
    orignBuffer='shenzhen'
    field_id="DIS"
    desc=arcpy.Describe(orignBuffer)
    with arcpy.da.SearchCursor(pointFeature,[field_id,"SHAPE@XY"],spatial_reference=desc.spatialReference) as curse:
        xyList=[]
        Id_list=[]
        for row in curse:
            Id_list.append(row[0])
            pn=row[1]
            xyList.append([pn[0],pn[1]])
        del row,curse
    featureList = []
    temp_point=arcpy.Point()
    for pn in xyList:
        temp_point.X=pn[0]
        temp_point.Y=pn[1]
        array=arcpy.Array()
        array.add(temp_point)
        MultiPn=arcpy.Multipoint(array)
        featureList.append(MultiPn)
    bufferList=[]
    bufferList2=[]
    for Multipn in featureList:
        temp_bufferlist=[]
        for Multipn2 in featureList:
            if(Multipn !=Multipn2):
                dis=Multipn.distanceTo(Multipn2)
                temp_poly=Multipn.buffer(dis)
                temp_poly2=temp_poly.projectAs(arcpy.Describe(orignBuffer).spatialReference)
                temp_bufferlist.append(temp_poly2)
                bufferList2.append(temp_poly2)
        bufferList.append(temp_bufferlist)

    #arcpy.CopyFeatures_management(bufferList2, outFeature)
    return bufferList,Id_list
def cal_interect_area(bufferList):
    env.workspace = 'E:/data/shenzhen/shenzhen.mdb'
    polygonfeature = 'shenzhen'
    denisity=[]
    id_List=[]
    feature_list=[]
    desc=arcpy.Describe(polygonfeature)
    with arcpy.da.SearchCursor(polygonfeature, ["OID@", "SHAPE@","PD_INHABIT"],spatial_reference=desc.spatialReference) as curse:
        for row in curse:
            id=row[0]
            poly=row[1]
            DN=row[2]
            id_List.append(id)
            feature_list.append(poly)
            denisity.append(DN)
    #arcpy.CopyFeatures_management(feature_list, "laxi")
    area_list=[]
    for polylist in bufferList:
        for poly in polylist:
            area_sum=0
            for i,feature in enumerate(feature_list):
                # if(poly.contains(feature)):
                #     area_sum+=feature.getArea("PLANAR")
                if not poly.disjoint(feature):
                    temp_poly=poly.intersect(feature,4)
                    area=temp_poly.getArea('PLANAR')
                    area_sum+=area*denisity[i]
            area_list.append(area_sum)
    return area_list
def cal_final_flx(area_list):
    env.workspace = 'E:/data/shenzhen/shenzhen.mdb'
    ORG="shenzhen"
    ORG_Field=["DIS","PN_INHABIT","PD_INHABIT"]##id and density,num of population ,there parameter
    Trgt="temp_feature"
    Trgt_Field=['p1','p2','flux']
    ### left and right field in list

    ##get the value from ORG
    value_dic = {}
    with arcpy.da.SearchCursor(ORG,ORG_Field,spatial_reference=arcpy.Describe(ORG).spatialReference) as curse:
        for rows in curse:
            value_dic[rows[0]]=rows[1]

    ##get the value of Trgt
    value_list2 = []
    with arcpy.da.UpdateCursor(Trgt,Trgt_Field,spatial_reference=arcpy.Describe(Trgt).spatialReference)as curse:
        for row in curse:
            m, n, s = 0, 0, 0
            if value_dic.has_key(row[0]):
                m = value_dic[row[0]]
            if value_dic.has_key(row[1]):
                n = value_dic[row[1]]
            s = 1
            answer=radiation_model(m,n,s)
            value_list2.append(answer)
            row[2]=answer
            curse.updateRow(row)
    return value_list2

def radiation_model(m,n,s):
    mn=m*n
    return mn/((m+s)*(n+m+s))
def get_flux_double():
    ORG="shenzhen"
    env.workspace = 'E:/data/shenzhen/shenzhen.mdb'
    feature1="temp_feature"
    feature2=""
    feature1_Field = ['p1', 'p2', 'flux']
    feature2_Field=[]
    answer=[]
    with arcpy.da.SearchCursor(feature1,feature1_Field,spatial_reference=arcpy.Describe(ORG).spatialReference) as curse:
        for row in curse:
            temp_list=[]
            for temp in row:
                temp_list.append(temp)
            answer.append(temp_list)
    with arcpy.da.SearchCursor(feature2,feature2_Field,spatial_reference=arcpy.Describe(ORG).spatialReference)as curse:
        for row in curse:
            temp1=row[0]
            temp2=row[1]
            for answer_temp in answer:
                if(answer_temp[0]==temp1 and answer_temp[1]==temp2):
                    answer_temp.append(row[2])
                    break
    return answer

bfferlist,idlist=get_buffer_list()
area_list=cal_interect_area(bfferlist)
flux_list=cal_final_flx(area_list)


