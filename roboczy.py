'''import arcpy

folder = "D:\Python_projects\PiPG-AB-290725\PiPG-AB-290725\dane"

# Nazwa geobazy
baza="BIELAK_egzamin"
geobaza = folder+'\\'+baza+".gdb"

# Utworzenie nowej geobazy za pomoca polecenia Create File GDB (skrzynka narzedziowa: data management) - jezeli jeszcze nie istnieje
if not arcpy.Exists(geobaza):
    arcpy.CreateFileGDB_management(folder,baza)

# Ustawienie przestrzeni roboczej w danej geobazie
arcpy.env.workspace = geobaza
#arcpy.env.workspace = "D:\Python_projects\PiPG-AB-290725\PiPG-AB-290725\dane"
arcpy.env.overwriteOutput = 1

inFeatures = "D:\Python_projects\PiPG-AB-290725\PiPG-AB-290725\dane\BUBD.shp"
#outFeatures = "D:\Python_projects\PiPG-AB-290725\PiPG-AB-290725\dane\BudynekTestowy.shp"
objectField = 'gmlId'
objectID = "PL.PZGIK.BDOT10k.BUBDA.18.6315774"

#arcpy.MakeFeatureLayer_management(inFeatures, 'budynki', ("'gmlId' = '" + objectID + "'"))
#arcpy.SelectLayerByAttribute_management('budynki', 'NEW_SELECTION', ("'gmlId' = '" + objectID + "'"))
#arcpy.CopyFeatures_management('budynek_testowy', 'budynki')
where_clause = '"' + objectField + '" = ' + "'" + objectID + "'"

arcpy.Select_analysis(inFeatures, 'BudynekTestowy', where_clause)
#arcpy.FeatureVerticesToPoints_management('BudynekTestowy','BudynekTestowyPunkty', "ALL")

'''

import arcpy
from math import sqrt, acos, pi, atan, fabs
import pandas as pd

def segmentLength(x1, y1, x2, y2):
    distance = sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))

    return distance

def azimuth(x1, y1, x2, y2):
    try:
        fi = (atan((fabs(x2 - x1)) / (fabs(y2 - y1)))) * 180 / pi
    except ZeroDivisionError:
        fi = 90

    if (x2 - x1) >= 0 and (y2 - y1) > 0:
        az = fi
    elif (x2 - x1) > 0 and (y2 - y1) <= 0:
        az = 180 - fi
    elif (x2 - x1) <= 0 and (y2 - y1) < 0:
        az = 180 + fi
    elif (x2 - x1) < 0 and (y2 - y1) >= 0:
        az = 360 - fi

    return az

#zdefiniowanie funkcji zwracajacej kat wewnetrzny (prawy) pomiedzy trzema punktami o zadanych wspolrzednych xy
def angleIn(x1, y1, x2, y2, x3, y3):
    angle =  azimuth(x1, y1, x2, y2) - azimuth(x2, y2, x3, y3) + 180
    if angle < 0:
        return angle + 360
    elif angle > 360:
        return angle - 360
    else:
        return angle

'''def angleIn(x1, y1, x2, y2, x3, y3):
    alfa = acos((segmentLength(x1, y1, x2, y2) ** 2 + segmentLength(x2, y2, x3, y3) ** 2 - segmentLength(x1, y1, x3, y3) ** 2) / (2 * segmentLength(x1, y1, x2, y2) * segmentLength(x2, y2, x3, y3)))
    angle = alfa * 180 / pi
    return angle'''


def listOfMinimumGeometries(geometry):
    list_of_geometry_type = ['RECTANGLE_BY_AREA', 'RECTANGLE_BY_WIDTH', 'CONVEX_HULL', 'CIRCLE', 'ENVELOPE']
    list_of_minimum_geometries = [arcpy.MinimumBoundingGeometry_management(geometry,  geometry_type+'.shp', geometry_type) for geometry_type in list_of_geometry_type]
    return list_of_minimum_geometries


arcpy.env.overwriteOutput = 1
arcpy.env.workspace ="D:\Python_projects\PiPG-AB-290725\PiPG-AB-290725\dane"

inFeatures = "D:\Python_projects\PiPG-AB-290725\PiPG-AB-290725\dane\BUBD.shp"
outFeatures = "D:\Python_projects\PiPG-AB-290725\PiPG-AB-290725\dane\BudynekTestowy.shp"

objectField = 'gmlId'
objectID = 'PL.PZGIK.BDOT10k.BUBDA.18.6326392'

where_clause = '"' + objectField + '" = ' + "'" + objectID + "'"

#arcpy.MakeFeatureLayer_management(inFeatures, 'budynki', ("'gmlId' = '" + objectID + "'"))
#arcpy.SelectLayerByAttribute_management('budynki', 'NEW_SELECTION', ("'gmlId' = '" + objectID + "'"))
#arcpy.CopyFeatures_management('budynek_testowy', 'budynki')

arcpy.Select_analysis(inFeatures, 'BudynekTestowy.shp', where_clause)
arcpy.FeatureVerticesToPoints_management('BudynekTestowy.shp','BudynekTestowyPunkty.shp', "ALL")

list = []

# Enter for loop for each feature
for row in arcpy.da.SearchCursor('BudynekTestowyPunkty.shp', ["FID", "SHAPE@XY"]):
    # Print x,y coordinates of each point feature
    pointID = row[0]
    pointXY = row[1]
    list.append((pointID, ) + pointXY)
list = list[:-1]

data_list = []

#tutaj trzeba bedzie jeszcze ogarnac 'dziury' w budynkach - najlepiej sprawdzaac po wspolrzednych - jesli beda obie rowne
#to wtedy bedzie trzeba skopiowac pierwszy i wkleic do ostatniego i dalej od poczatku to samo - bedzie to kilka zapetlonych w sobie petli


for point in list:
    pointID_center = point[0]
    X_center = point[1]
    Y_center = point[2]

    #if X_center != X_in and Y_center != Y_in:
    #else if X_center == X_in and Y_center == Y_in:

    if pointID_center > list[0][0]:
        pointID_in = list[pointID_center-1][0]
        X_in = list[pointID_center-1][1]
        Y_in = list[pointID_center-1][2]
    else:
        pointID_in = list[-1][0]
        X_in = list[-1][1]
        Y_in = list[-1][2]

    if pointID_center < list[-1][0]:
        pointID_out = list[pointID_center+1][0]
        X_out = list[pointID_center+1][1]
        Y_out = list[pointID_center+1][2]
    else:
        pointID_out = list[0][0]
        X_out = list[0][1]
        Y_out = list[0][2]

    length_in = segmentLength(X_in, Y_in, X_center, Y_center)
    #print('%s - %s : %0.3f [m]' %(pointID_in, pointID_center, length_in))
    length_out = segmentLength(X_center, Y_center, X_out, Y_out)
    #print('%s - %s : %0.3f [m]' %(pointID_center, pointID_out, length_out))
    angle_in = angleIn(X_in, Y_in, X_center, Y_center, X_out, Y_out)
    #print('%s - %s - %s: %0.8f [deg] \n' %(pointID_in, pointID_center, pointID_out, angle_in))

    data_list.append([objectID, pointID_center, length_in, length_out, angle_in])
data_list.append([objectID] + [pointID_center + 1] + data_list[0][2:])

#print data_list
#print len(data_list)

list = listOfMinimumGeometries('BudynekTestowyPunkty.shp')

for geometry in list:
    near_features = arcpy.FeatureToLine_management(geometry, str(geometry)[:-4] + '_lines.shp', "0.001 Meters", "ATTRIBUTES")
    in_features = 'BudynekTestowyPunkty.shp'
    # execute the function
    arcpy.Near_analysis(in_features, near_features, location='LOCATION', angle='ANGLE')
    i = 0
    for row in arcpy.da.SearchCursor(in_features, ["NEAR_DIST"]):
        data_list[i].append(row[0])
        i += 1

column_names = ['ID budynku', 'Numer kolejny wierzcholka', 'Dlugosc segmentu przed [m]', 'Dlugosc segmentu po [m]', 'Kat wewnetrzny [deg]',
                'Strzalka do boku RECTANGLE_BY_AREA [m]', 'Strzalka do boku RECTANGLE_BY_WIDTH [m]', 'Strzalka do boku CONVEX_HULL [m]',
                'Strzalka do boku CIRCLE [m]', 'Strzalka do boku ENVELOPE [m]']

df = pd.DataFrame(data_list, columns=column_names)
df.to_csv('results.csv', index=False, float_format='%.3f')
print df