#import bibliotek
import arcpy
from math import sqrt, acos, pi, atan, fabs
import pandas as pd
from numpy import array

#zdefiniowanie funkcji zwracającej odległosc pomiedzy dwoma punktami o zadanych wspolrzednych xy
def segmentLength(x1, y1, x2, y2):
    distance = sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))

    return distance

#zdefiniowanie funkcji zwracającej azymut pomiedzy dwoma punktami o zadanych wspolrzednych xy
def azimuth(x1, y1, x2, y2):
    try:
        fi = atan((fabs(x2 - x1)) / (fabs(y2 - y1))) * 180 / pi
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

#zdefiniowanie funkcji zwracającej kat wewnetrzny (prawy) pomiedzy trzema punktami o zadanych wspolrzednych xy
def angleIn(x1, y1, x2, y2, x3, y3):
    angle =  azimuth(x1, y1, x2, y2) - azimuth(x2, y2, x3, y3) + 180
    if angle < 0:
        return angle + 360
    elif angle > 360:
        return angle - 360
    else:
        return angle

#zdefinowanie funkcji zwracajacej liste geometri w postaci otoczek na podstawie geometri wejsciowej
def listOfMinimumGeometries(geometry):
    list_of_geometry_type = ['RECTANGLE_BY_AREA', 'RECTANGLE_BY_WIDTH', 'CONVEX_HULL', 'CIRCLE', 'ENVELOPE']
    list_of_minimum_geometries = [arcpy.MinimumBoundingGeometry_management(geometry,  geometry_type+'.shp', geometry_type) for geometry_type in list_of_geometry_type]
    return list_of_minimum_geometries

#nadpisywanie zmian
arcpy.env.overwriteOutput = 1

#zdefiniowanie folderu roboczego
arcpy.env.workspace = arcpy.GetParameterAsText(0)
workspace = arcpy.env.workspace

#zdefniowanie wejscowego pliku shapefile z budynkami
inFeatures = arcpy.GetParameterAsText(1)

#zdefniniowanie wyjsciowego pliku shapefile z wyselekcjonowanym budynkiem - znajdzie sie w katalogu roboczym
outFeatures = 'BudynekTestowy.shp'

#zdefiniowanie parametru w postaci wyrazenia SQL - uzytkownik bedznie mial za zadanie wskazanie pola z identyfikatorami
#oraz wskazanie ID konkretnego budynku
query = arcpy.GetParameterAsText(2)

#'wyciagniecie' z wprowadzonego wyrazenia SQL nazwy pola oraz ID obiektu oraz przypisanie do odpowiednich zmiennych
#oraz zabezbieczenie sie na wypadek spacji i innych nie potrzebnych znakow
index = query.index('=')
objectField = query[:index].strip()
objectID = query[index+1:].strip().strip('\'')

#wyselekcjonowanie jednego obiektu na podstawie zapytania SQL
arcpy.Select_analysis(inFeatures, outFeatures, query)

#utworzenie pliku z wszystkimi punktami budujacymi poligon - w tym wypadku konkretny budynek
#w przypadku tego sposobu nalezy pamietac ze punkt poczatkowy pojedynczej lini bedzie tozsamy z punktem koncowym
arcpy.FeatureVerticesToPoints_management('BudynekTestowy.shp','BudynekTestowyPunkty.shp', "ALL")

#utworzenie pustej listy ktora bedzie przechowywala tuple w postaci: (ID punktu, X ,Y)
list = []

#petla iterujaca po kazdym wierszu warstwy punktowej, ktorej zadaniem jest dodanie danych do listy w postaci tupli dla kazdego punktu
#ostatecznym wynikiem instrukcji bedzie lista tupli z danymi niezbednymi do dalszych operacji
for row in arcpy.da.SearchCursor('BudynekTestowyPunkty.shp', ["FID", "SHAPE@XY"]):
    pointID = row[0]
    pointXY = row[1]
    list.append((pointID, ) + pointXY)

#znalezienie duplikatow (ID punktow majacych taka sama lokalizacje) i zapisanie do pliku tekstowego
arcpy.management.FindIdentical('BudynekTestowyPunkty.shp', 'BudynekTestowyPunktyDuplikaty.txt', ["SHAPE"], output_record_option='ONLY_DUPLICATES')

#utworzenie pustej listy ktora bedzie przechowywala ID punktow poczatkowych i koncowych wielobokow 'budujacych' budynek
#bo nalezy pamietac ze budynki nie musza byc jedynie 'prostymi' prostokatami/kwadratami ale moga to byc rowniez budynki 'z dziurami'
list_of_duplicateID = []

#wczystanie pliku tekstowego z duplikatami i dodanie ID punktow do listy
with open(workspace + '\BudynekTestowyPunktyDuplikaty.txt') as file:
    next(file)
    for line in file:
        row = line.split(';')
        list_of_duplicateID.append(int(row[1]))

#stworzenie listy punktow poczatkowych i koncowych
list_of_begin_pointID = list_of_duplicateID[0::2]
list_of_end_pointID = list_of_duplicateID[1::2]

#zdefiniowanie zmiennych  pomocniczych: indeksu, ID punktu poczatkowego i koncowego wieloboku
index = 0
pointID_end = list[list_of_end_pointID[index]][0]
pointID_begin = list[list_of_begin_pointID[index]][0]

#utworzenie pustej listy ktora 'w przyszlosci' bedzie wszystkie dane wymagane w ostatecznym pliku 'results.csv'
data_list = []

for point in list:
    #punkt centralny
    pointID_center = point[0]
    X_center = point[1]
    Y_center = point[2]

    print('Punkt centralny: %s' %pointID_center)

    #podzielenie punktow na 3 przypadki (gdyby wszystkie budynki byly figurami bez wolnych przestrzeni zadanie bylo by o wiele prostsze):
    # 1) wowczas kiedy punkt centralny jest pierwszym punktem
    # 2) wowczas kiedy punkt centralny jest ostatnim punktem
    # 3) pozostale przypadki

    # przypadek 1)
    if pointID_center == min(array(list)[:, 0]):
        pointID_in = list[list_of_end_pointID[0] - 1][0]
        X_in = list[list_of_end_pointID[0] - 1][1]
        Y_in = list[list_of_end_pointID[0] - 1][2]
        pointID_out = list[list_of_begin_pointID[0] + 1][0]
        X_out = list[list_of_begin_pointID[0] + 1][1]
        Y_out = list[list_of_begin_pointID[0] + 1][2]

        length_in = segmentLength(X_center, Y_center, X_in, Y_in)
        print('%s - %s : %0.3f [m]' % (pointID_in, pointID_center, length_in))
        length_out = segmentLength(X_center, Y_center, X_out, Y_out)
        print('%s - %s : %0.3f [m]' % (pointID_center, pointID_out, length_out))
        angle_in = angleIn(X_in, Y_in, X_center, Y_center, X_out, Y_out)
        print('%s - %s - %s: %0.8f [deg]' %(pointID_in, pointID_center, pointID_out, angle_in))
        print('-------------------------------------------')

    # przypadek 3)
    elif (pointID_center < max(array(list)[:, 0])) and (pointID_center > min(array(list)[:,0])):
        pointID_out = list[pointID_center + 1][0]
        X_out = list[pointID_center + 1][1]
        Y_out = list[pointID_center + 1][2]
        pointID_in = list[pointID_center - 1][0]
        X_in = list[pointID_center - 1][1]
        Y_in = list[pointID_center - 1][2]

        #ponowne rozbicie na 3 przypadki:
        #a) wowczas kiedy punkt centralny bedzie punktem koncowym wieloboku
        #b) wowczas kiedy punkt centralnyc bedzie punktem koncowym wieloboku
        #c) pozostale przypadki

        # przypadek a)
        if pointID_center in list_of_end_pointID:
            length_in = segmentLength(X_in, Y_in, X_center, Y_center)
            print('%s - %s : %0.3f [m]' % (pointID_in, pointID_center, length_in))
            length_out = segmentLength(X_center, Y_center, list[pointID_begin + 1][1], list[pointID_begin + 1][2])
            print('%s - %s : %0.3f [m]' % (pointID_center, pointID_begin + 1, length_out))
            angle_in = angleIn(X_in, Y_in, X_center, Y_center, list[pointID_begin + 1][1], list[pointID_begin + 1][2])
            print('%s - %s - %s: %0.8f [deg]' % (pointID_in, pointID_center, pointID_begin + 1, angle_in))
            print('-------------------------------------------')

            #przestawienie indeksu o jeden i tym samym zmiana ID punktu poczatkowego, koncowego
            if index < len(list_of_end_pointID)-1:
                index += 1
                pointID_end = list[list_of_end_pointID[index]][0]
                pointID_begin = list[list_of_begin_pointID[index]][0]

        # przypadek b)
        elif pointID_center in list_of_begin_pointID:
            length_in = segmentLength(list[pointID_end - 1][1], list[pointID_end - 1][2], X_center, Y_center)
            print('%s - %s : %0.3f [m]' % (pointID_end - 1, pointID_center, length_in))
            length_out = segmentLength(X_center, Y_center, X_out, Y_out)
            print('%s - %s : %0.3f [m]' % (pointID_center, pointID_out, length_out))
            angle_in = angleIn(list[pointID_end - 1][1], list[pointID_end - 1][2], X_center, Y_center, X_out, Y_out)
            print('%s - %s - %s: %0.8f [deg]' % (pointID_end - 1, pointID_center, pointID_out, angle_in))
            print('-------------------------------------------')

        # przypadek c)
        else:
            length_in = segmentLength(X_in, Y_in, X_center, Y_center)
            print('%s - %s : %0.3f [m]' % (pointID_in, pointID_center, length_in))
            length_out = segmentLength(X_center, Y_center, X_out, Y_out)
            print('%s - %s : %0.3f [m]' % (pointID_center, pointID_out, length_out))
            angle_in = angleIn(X_in, Y_in, X_center, Y_center, X_out, Y_out)
            print('%s - %s - %s: %0.8f [deg]' % (pointID_in, pointID_center, pointID_out, angle_in))
            print('-------------------------------------------')

    # przypadek 2)
    else:
        pointID_in = list[pointID_center - 1][0]
        X_in = list[pointID_center - 1][1]
        Y_in = list[pointID_center - 1][2]
        pointID_out = list[list_of_begin_pointID[-1] + 1][0]
        X_out = list[list_of_begin_pointID[-1] + 1][1]
        Y_out = list[list_of_begin_pointID[-1] + 1][2]
        length_in = segmentLength(X_center, Y_center, X_in, Y_in)
        print('%s - %s : %0.3f [m]' % (pointID_in, pointID_center, length_in))
        length_out = segmentLength(X_center, Y_center, X_out, Y_out)
        print('%s - %s : %0.3f [m]' % (pointID_center, pointID_out, length_out))
        angle_in = angleIn(X_in, Y_in, X_center, Y_center, X_out, Y_out)
        print('%s - %s - %s: %0.8f [deg]' %(pointID_in, pointID_center, pointID_out, angle_in))
        print('-------------------------------------------')

    #dodanie danych do listy
    data_list.append([objectID, pointID_center, length_in, length_out, angle_in])


#wywolanie funkcji listOfMinimumGeometries, w ktorej wyniku otrzymamy poligony otoczek
#i przypisanie wynikow do zmiennej w postaci listy
list_of_min_geom = listOfMinimumGeometries('BudynekTestowyPunkty.shp')

#przekonwertowanie poligonow na linie i zapis poszcaegolnych warstw w katalogu roboczym
for geometry in list_of_min_geom:
    near_features = arcpy.FeatureToLine_management(geometry, str(geometry)[:-4] + '_lines.shp', "0.001 Meters", "ATTRIBUTES")
    in_features = 'BudynekTestowyPunkty.shp'
    #wykorzystanie funkcji z biblioteki arcpy do znaleznienia najkrotsyzch odleglosci do krawedzi poszczegolnych otoczek
    arcpy.Near_analysis(in_features, near_features, location='LOCATION', angle='ANGLE')
    #dodanie do tupli poszczegolnyego punktu w liscie data_list informacji dotyczacych odleglosci do krawedzi otoczek
    i = 0
    for row in arcpy.da.SearchCursor(in_features, ["NEAR_DIST"]):
        data_list[i].append(row[0])
        i += 1
#zdefiniowanie nazw kolumn
column_names = ['ID_budynku', 'Numer_kolejny_wierzcholka', 'Dlugosc_segmentu_przed [m]', 'Dlugosc_segmentu_po [m]', 'Kat_wewnetrzny [deg]',
                'Strzalka_do_boku_RECTANGLE_BY_AREA [m]', 'Strzalka_do_boku_RECTANGLE_BY_WIDTH [m]', 'Strzalka_do_boku_CONVEX_HULL [m]',
                'Strzalka_do_boku_CIRCLE [m]', 'Strzalka_do_boku_ENVELOPE [m]']

#zdefiniowanie folderu w ktorym znajdzie sie ostateczny plik wyjsciowy
output_folder = arcpy.GetParameterAsText(3)
output = output_folder + '\\results.csv'

#utworzenie DataFrame z wynikami
df = pd.DataFrame(data_list, columns=column_names)

#eksport DataFrame do pliku wyjsciowego 'results.csv'
df.to_csv(output, index=False, sep='\t', float_format='%.3f')
