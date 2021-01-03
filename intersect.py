import arcpy
import sys

def intersect(geometry1, geometry2):


    # Evaluate various polygon methods

    test1 = geometry1.contains(geometry2)
    test2 = geometry1.crosses(geometry2)
    test3 = geometry1.disjoint(geometry2)
    test4 = geometry1.equals(geometry2)
    test5 = geometry1.overlaps(geometry2)
    test6 = geometry1.touches(geometry2)
    test7 = geometry1.within(geometry2)

    # Evaluate obverse

    test8 = geometry2.contains(geometry1)
    test9 = geometry2.crosses(geometry1)
    test10 = geometry2.disjoint(geometry1)
    test11 = geometry2.equals(geometry1)
    test12 = geometry2.overlaps(geometry1)
    test13 = geometry2.touches(geometry1)
    test14 = geometry2.within(geometry1)

    print 'geometry1.contains(geometry1)  = ', test1
    print 'geometry1.crosses(geometry2)  = ', test2
    print 'geometry1.disjoint(geometry2)  = ', test3
    print 'geometry1.equals(geometry2)  = ', test4
    print 'geometry1.overlaps(geometry2)  = ', test5
    print 'geometry1.touches(geometry2)  = ', test6
    print 'geometry1.within(geometry2)  = ', test7


    print 'geometry2.contains(geometry1)  = ', test8
    print 'geometry2.crosses(geometry1)  = ', test9
    print 'geometry2.disjoint(geometry1) = ', test10
    print 'geometry2.equals(geometry1) = ', test11
    print 'geometry2.overlaps(geometry1) = ', test12
    print 'geometry2.touches(geometry1) = ', test12
    print 'geometry2.within(geometry1) = ', test12


'''
#
# test of the various geometry or poly interaction methods
#
import arcpy
import sys

# define coordinate lists

clist1 = [[0,0], [0,10],[10,10],[10,0],[0,0]]
clist2 = [[5,0],[5,10],[20,10],[20,0],[5,0]]

# define geometry objects
#
#   (0, 10) -------(10, 10)---------(20, 10)
#           |  P1  |       |   P2  |
#   (0,  0) -------(10,  0)---------(20,  0)
#
# Intersection along the line (10,0) to (10,10)

aPt = arcpy.Point()
anArray = arcpy.Array()

# Make first polygon

for coordpair in clist1:
    aPt.X, aPt.Y = coordpair[0], coordpair[1]
    anArray.add(aPt)

polygon1 = arcpy.Polygon(anArray)

# Clear array and push in second coordinate list

anArray.removeAll()

# Make second polygon

for coordpair in clist2:
    aPt.X, aPt.Y = coordpair[0], coordpair[1]
    anArray.add(aPt)

polygon2 = arcpy.Polygon(anArray)

# Method Explanation
#
#   contains (second_geometry) Indicates if this geometry contains the other geometry.
#   crosses (second_geometry) Indicates if the two geometries intersect in a geometry of lesser dimension.
#   disjoint (second_geometry) Indicates if the two geometries share no points in common.
#   equals (second_geometry) Indicates if the two geometries are of the same type and define the same set of points in the plane.
#   overlaps (second_geometry) Indicates if the intersection of the two geometries has the same dimension as one of the input geometries.
#   touches (second_geometry) Indicates if the boundaries of the geometries intersect.
#   within (second_geometry) Indicates if this geometry is contained within another geometry.

# Based on coordinate lists and definitions

# Polygon1 contains Polygon2 = False
# Polygon1 crosses Polygon2 = True Two two-dimensional polygons share a one-dimensional boundary, the line from (10,0) to (10,10)
# Polygon1 disjoint Polygon2 = False
# Polygon1 equals Polygon2 = False
# Polygon1 overlaps Polygon2 = False (Intersection is one-dimensional line (10,0) to (10,10)
# Polygon1 touches Polygon2 = True (Intersect along line (10,0) to (10,10)
# Polygon1 within Polygon2 = False

# Evaluate various polygon methods

test1 = polygon1.contains(polygon2)
test2 = polygon1.crosses(polygon2)
test3 = polygon1.disjoint(polygon2)
test4 = polygon1.equals(polygon2)
test5 = polygon1.overlaps(polygon2)
test6 = polygon1.touches(polygon2)
test7 = polygon1.within(polygon2)

# Evaluate obverse

test8 = polygon2.contains(polygon1)
test9 = polygon2.crosses(polygon1)
test10 = polygon2.disjoint(polygon1)
test11 = polygon2.equals(polygon1)
test12 = polygon2.overlaps(polygon1)
test13 = polygon2.touches(polygon1)
test14 = polygon2.within(polygon1)

print 'polygon1.contains(polygon2)  = ', test1
print 'polygon1.crosses(polygon2)  = ', test2
print 'polygon1.disjoint(polygon2)  = ', test3
print 'polygon1.equals(polygon2)  = ', test4
print 'polygon1.overlaps(polygon2)  = ', test5
print 'polygon1.touches(polygon2)  = ', test6
print 'polygon1.within(polygon2)  = ', test7

print ' '

print 'polygon2.contains(polygon1)  = ', test8
print 'polygon2.crosses(polygon1)  = ', test9
print 'polygon2.disjoint(polygon1) = ', test10
print 'polygon2.equals(polygon1) = ', test11
print 'polygon2.overlaps(polygon1) = ', test12
print 'polygon2.touches(polygon1) = ', test12
print 'polygon2.within(polygon1) = ', test12

'''
