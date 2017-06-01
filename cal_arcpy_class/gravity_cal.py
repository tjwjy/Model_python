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
        dis_list=[]
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
                    dis_list.append(polyLine.length)

        ############################################################################

        temp_feature = arcpy.CreateScratchName('temp', data_type='FeatureClass ')
        arcpy.CopyFeatures_management(featureList, temp_feature)
        arcpy.MakeFeatureLayer_management(temp_feature, 'lyr')
        arcpy.AddField_management('lyr', field_name='p1', field_type='SHORT')
        arcpy.AddField_management('lyr', field_name='p2', field_type='SHORT')
        arcpy.AddField_management('lyr', field_name='dist', field_type='DOUBLE')
        arcpy.AddField_management('lyr',field_name='PN_O',field_type='DOUBLE')
        arcpy.AddField_management('lyr', field_name='PN_D', field_type='DOUBLE')
        arcpy.AddField_management('lyr', field_name='flux', field_type='DOUBLE')
        if arcpy.Exists(outFeature):
            arcpy.Delete_management(outFeature)
        arcpy.CopyFeatures_management('lyr', outFeature)
        arcpy.Delete_management(temp_feature)

        ##########################################################################


        ####
        with arcpy.da.UpdateCursor(outFeature, ['p1', 'p2','dist']) as curse:
            i = 0
            for row in curse:
                row[0] = field_list[i][0]
                row[1] = field_list[i][1]
                row[2]=dis_list[i]
                curse.updateRow(row)
                i += 1
            del curse, row
        ####
        print (0)

    def get_dis_list(self,field_dis):
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
        dislist = []
        id_list2=[]
        for  i,Multipn in enumerate(featureList):
            for j,Multipn2 in enumerate(featureList):
                if (Multipn != Multipn2):
                    dis = Multipn.distanceTo(Multipn2)
                    dislist.append(dis)
                    id_list2.append([i,j])
        return dislist,id_list2

    def cal_final_matrix(self, dis_field, id_list, dis_list):
        # dis_field=["DIS", "PN_INHABIT", "PD_INHABIT"]
        env.workspace = self.env
        ORG = self.inhabit_dis
        ORG_Field = dis_field  ##id ,num of population ,there parameter
        Trgt = "temp_feature"
        Trgt_Field = ['p1', 'p2', 'flux','PN_D','PN_D']
        ### left and right field in list

        ##get the value from ORG
        value_dic = {}
        with arcpy.da.SearchCursor(ORG, ORG_Field, spatial_reference=arcpy.Describe(ORG).spatialReference) as curse:
            for rows in curse:
                value_dic[rows[0]] = rows[1]

        ##get the value of Trgt
        value_list2 = []
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
                area_index = 0
                for index, item in enumerate(id_list):
                    if (item[0] == row[0] and item[1] == row[1]):
                        dis_list = index
                s = dis_list[area_index]
                row[2] =s
                row[3]=m
                row[4]=n
                value_list2.append([row[0]],row[1],m,n,s)
                curse.updateRow(row)
        return value_list2

    def get_flux_double(self,od_featrue,od_field,value_list):
        #od_field=["DIS_O","DIS_D","PD_COMMUTE "]
        ORG = self.inhabit_dis
        env.workspace = self.env
        feature2 = od_featrue
        feature2_Field = od_field
        answer = value_list
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

    def write_txt(self, path, value_list):
        with (open(path, 'w')) as f:
            temp_str = ""
            for value in value_list:
                if len(value)==6:
                    temp_str = str(value[0]) + " " + str(value[1]) + " " + str(value[2]) + " " + str(value[3]) +  " " + str(value[4])+ " " + str(value[5])+"\n"
                f.writelines(temp_str)

    def get_dis(self, field_dis):
        # fied_dis=DIS
        env.workspace = self.env
        pointFeature = self.point_object
        orignBuffer = self.inhabit_dis
        field_id = field_dis
        desc = arcpy.Describe(orignBuffer)
        with arcpy.da.SearchCursor(pointFeature, [field_id, "SHAPE@"],
                                   spatial_reference=desc.spatialReference) as curse:
            pointList = []
            Id_list = []
            for row in curse:
                Id_list.append(row[0])
                pn = row[1]
                pointList.append(pn)
            del row, curse
        dislist = []
        id_list2 = []
        for i, Multipn in enumerate(pointList):
            for j, Multipn2 in enumerate(pointList):
                if (Multipn != Multipn2):
                    dis = Multipn.distanceTo(Multipn2)
                    dislist.append(dis)
                    id_list2.append([i, j])
        return dislist, id_list2

# deal=deal_OD(env_path='E:/data/shenzhen/shenzhen.mdb',inhabit_dis="living_dis",point_object="random_split")
# deal.create_OD_line("DIS")
# disList,id_list=deal.get_dis_list(field_dis="DIS")
# deal.cal_final_matrix(id_list=id_list,dis_field=["DIS", "PN_INHABIT", "PD_INHABIT"],dis_list=disList)
# flux=deal.get_flux_double(od_featrue="OD_1",od_field=["DIS_O","DIS_D","PD_COMMUTE "])
# deal.write_txt("C:/temp.txt",flux)
deal=deal_OD(env_path='E:/data/shenzhen/shenzhen.mdb',inhabit_dis="shenzhen",point_object="shenzhen_random_split")
dis_list,_=deal.get_dis(field_dis="DIS")
print dis_list