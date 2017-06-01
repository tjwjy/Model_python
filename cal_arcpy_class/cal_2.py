import arcpy
from arcpy import env
class deal_OD():
    def __init__(self,env_path,inhabit_dis,point_object):
        self.env=env_path
        self.inhabit_dis=inhabit_dis
        self.point_object=point_object
    def create_OD_line(self,dis_feild):
        #dis_feild="DIS"
        env.workspace=self.env
        pointFeature=self.point_object
        outFeature="temp_feature"
        field_id=dis_feild
        with arcpy.da.SearchCursor(pointFeature, [field_id, "SHAPE@XY"]) as curse:
            xyList = []
            Id_list = []
            pn = arcpy.Point()
            for row in curse:
                Id_list.append(row[0])
                pn = row[1]
                xyList.append([pn[0], pn[1]])
            del row, curse
        featureList = []
        field_list = []
        temp_point = arcpy.Point()
        for pn in xyList:
            for pn1 in xyList:
                if (pn != pn1):
                    temp_point.X = pn[0]
                    temp_point.Y = pn[1]
                    array = arcpy.Array()
                    array.add(temp_point)
                    temp_point.X = pn1[0]
                    temp_point.Y = pn1[1]
                    array.add(temp_point)
                    polyLine = arcpy.Polyline(array)
                    featureList.append(polyLine)
                    field_list.append([Id_list[xyList.index(pn)], Id_list[xyList.index(pn1)]])

        ############################################################################

        temp_feature = arcpy.CreateScratchName('temp', data_type='FeatureClass ')
        arcpy.CopyFeatures_management(featureList, temp_feature)
        arcpy.MakeFeatureLayer_management(temp_feature, 'lyr')
        arcpy.AddField_management('lyr', field_name='p1', field_type='SHORT')
        arcpy.AddField_management('lyr', field_name='p2', field_type='SHORT')
        arcpy.AddField_management('lyr', field_name='flux', field_type='DOUBLE')
        if arcpy.Exists(outFeature):
            arcpy.Delete_management(outFeature)
        arcpy.CopyFeatures_management('lyr', outFeature)
        arcpy.Delete_management(temp_feature)

        ##########################################################################


        ####
        with arcpy.da.UpdateCursor(outFeature, ['p1', 'p2']) as curse:
            i = 0
            for row in curse:
                row[0] = field_list[i][0]
                row[1] = field_list[i][1]
                curse.updateRow(row)
                i += 1
            del curse, row
        ####
        print (0)

    def get_buffer_list(self,field_dis):
        #fied_dis=DIS
        env.workspace =self.env
        pointFeature = self.point_object
        orignBuffer =self.inhabit_dis
        field_id = field_dis
        desc = arcpy.Describe(orignBuffer)
        with arcpy.da.SearchCursor(pointFeature, [field_id, "SHAPE@XY"],
                                   spatial_reference=desc.spatialReference) as curse:
            xyList = []
            Id_list = []
            for row in curse:
                Id_list.append(row[0])
                pn = row[1]
                xyList.append([pn[0], pn[1]])
            del row, curse
        featureList = []
        temp_point = arcpy.Point()
        for pn in xyList:
            temp_point.X = pn[0]
            temp_point.Y = pn[1]
            array = arcpy.Array()
            array.add(temp_point)
            MultiPn = arcpy.Multipoint(array)
            featureList.append(MultiPn)
        bufferList = []
        id_list2=[]
        for  i,Multipn in enumerate(featureList):
            temp_bufferlist = []
            for j,Multipn2 in enumerate(featureList):
                if (Multipn != Multipn2):
                    dis = Multipn.distanceTo(Multipn2)
                    temp_poly = Multipn.buffer(dis)
                    temp_poly2 = temp_poly.projectAs(arcpy.Describe(orignBuffer).spatialReference)
                    temp_bufferlist.append(temp_poly2)
                    bufferList.append(temp_poly2)
                    id_list2.append([i,j])

        # arcpy.CopyFeatures_management(bufferList2, outFeature)
        return bufferList, id_list2

    def cal_interect_area(self,bufferList,pd_fied):
        #pd_fied="PD_INHABIT
        env.workspace = self.env
        polygonfeature =self.inhabit_dis
        polygonfeature_fied=["OID@", "SHAPE@",pd_fied]
        denisity = []
        id_List = []
        feature_list = []
        desc = arcpy.Describe(polygonfeature)
        with arcpy.da.SearchCursor(polygonfeature,polygonfeature_fied ,
                                   spatial_reference=desc.spatialReference) as curse:
            for row in curse:
                id = row[0]
                poly = row[1]
                DN = row[2]
                id_List.append(id)
                feature_list.append(poly)
                denisity.append(DN)
        # arcpy.CopyFeatures_management(feature_list, "laxi")
        area_list = []
        for poly in bufferList:
                area_sum = 0
                for i, feature in enumerate(feature_list):
                    # if(poly.contains(feature)):
                    #     area_sum+=feature.getArea("PLANAR")
                    if not poly.disjoint(feature):
                        temp_poly = poly.intersect(feature, 4)
                        area = temp_poly.getArea('PLANAR')
                        area_sum += area * denisity[i]/1000000
                area_list.append(area_sum)
        return area_list

    def cal_final_flx(self,dis_field,id_list,area_list):
        #dis_field=["DIS", "PN_INHABIT", "PD_INHABIT"]
        env.workspace =self.env
        ORG = self.inhabit_dis
        ORG_Field = dis_field  ##id and density,num of population ,there parameter
        Trgt = "temp_feature"
        Trgt_Field = ['p1', 'p2', 'flux']
        ### left and right field in list

        ##get the value from ORG
        value_dic = {}
        with arcpy.da.SearchCursor(ORG, ORG_Field, spatial_reference=arcpy.Describe(ORG).spatialReference) as curse:
            for rows in curse:
                value_dic[rows[0]] = rows[1]

        ##get the value of Trgt
        value_list2=[]
        # with arcpy.da.SearchCursor(Trgt, Trgt_Field, spatial_reference=arcpy.Describe(Trgt).spatialReference)as curse:
        #     temp_list=[]
        #     for row in curse:
        #         m, n, s = 0, 0, 0
        #         if value_dic.has_key(row[0]):
        #             m = value_dic[row[0]]
        #         if value_dic.has_key(row[1]):
        #             n = value_dic[row[1]]
        #         s = 1
        #         answer = self.radiation_model(m, n, s)
        #         value_dic[]
        with arcpy.da.UpdateCursor(Trgt, Trgt_Field, spatial_reference=arcpy.Describe(Trgt).spatialReference)as curse:
            for row in curse:
                if value_dic.has_key(row[0]):
                    m = value_dic[row[0]]
                if value_dic.has_key(row[1]):
                    n = value_dic[row[1]]
                area_index=0
                for index,item in enumerate(id_list):
                    if(item[0]==row[0]and item[1]==row[1]):
                        area_index=index
                s=area_list[area_index]
                answer = self.radiation_model(m, n, s)
                value_list2.append(answer)
                row[2] = answer*m
                curse.updateRow(row)
        return value_list2

    def radiation_model(self,m, n, s):
        mn = m * n
        return (mn +0.001)/ ((m + s) * (n + m + s))

    def get_flux_double(self,od_featrue,od_field):
        #od_field=["DIS_O","DIS_D","PD_COMMUTE "]
        ORG = self.inhabit_dis
        env.workspace = self.env
        feature1 = "temp_feature"
        feature2 = od_featrue
        feature1_Field = ['p1', 'p2', 'flux']
        feature2_Field = od_field
        answer = []
        with arcpy.da.SearchCursor(feature1, feature1_Field,
                                   spatial_reference=arcpy.Describe(ORG).spatialReference) as curse:
            for row in curse:
                temp_list = []
                for temp in row:
                    temp_list.append(temp)
                answer.append(temp_list)
        with arcpy.da.SearchCursor(feature2, feature2_Field,
                                   spatial_reference=arcpy.Describe(ORG).spatialReference)as curse:
            for row in curse:
                temp1 = row[0]
                temp2 = row[1]
                for answer_temp in answer:
                    if (answer_temp[0] == temp1 and answer_temp[1] == temp2):
                        answer_temp.append(row[2])
                        break
        return answer
    def write_txt(self,path,value_list):
        with (open(path, 'w')) as f:
            temp_str=""
            for value in value_list:
                temp_str=str(value[0])+" "+str(value[1])+" "+str(value[2])+" "+str(value[3])+"\n"
                f.writelines(temp_str)
    def read_txt(slef,path):
        value_list=[]
        with open(path,'r') as f:
            temp_str=f.readline()
            temp_str=temp_str.rstrip('\n')
            tag=True
            while(tag):
                temp_str = f.readline()
                temp_str = temp_str.rstrip('\n')
                if(temp_str):
                    temp_str = temp_str.split(' ')
                    temp_list=[]
                    for item in temp_str:
                        temp_list.append(float(item))
                else:
                    break
            return value_list

deal=deal_OD(env_path='E:/data/shenzhen/shenzhen.mdb',inhabit_dis="living_dis",point_object="random_split")
deal.create_OD_line("DIS")
bufferList,id_list=deal.get_buffer_list(field_dis="DIS")
area_list=deal.cal_interect_area(bufferList,pd_fied="PD_INHABIT")
deal.cal_final_flx(area_list=area_list,dis_field=["DIS", "PN_INHABIT", "PD_INHABIT"],id_list=id_list)
flux=deal.get_flux_double(od_featrue="OD_1",od_field=["DIS_O","DIS_D","PD_COMMUTE "])
deal.write_txt("C:/temp.txt",flux)