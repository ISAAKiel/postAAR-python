import time
import math
from multiprocessing import Pool
from shapely.geometry import Polygon

from helper import * 

def calcRectsInWindow (window, posts, maximal_length_of_side, minimal_length_of_side, maximal_difference_between_comparable_sides_in_percent=0.1):
    rects = set()

    distance_in_window = calcDistanceInWindow(window, posts)

    for a in range(len(window)):
        for b in range(len(window)):
            if a == b:
                break

            dist_ab = distance_in_window[a][b]
            if dist_ab < maximal_length_of_side and dist_ab > minimal_length_of_side:
                for c in range(len(window)):
                    if c == b or c == a:
                        break

                    dist_ac = distance_in_window[a][c]
                    
                    if dist_ac < maximal_length_of_side and dist_ac > minimal_length_of_side:
                        try:
                            dist_bc = distance_in_window[b][c]

                            if dist_ab < dist_bc:
                                for potential_d in range(len(window)):
                                    dist_bd = distance_in_window[b][potential_d]
                                    dist_ad = distance_in_window[a][potential_d]
                                    dist_cd = distance_in_window[c][potential_d]
                                    if (
                                        dist_bd < maximal_length_of_side and 
                                        dist_bd > minimal_length_of_side and
                                        dist_bc > dist_bd and
                                        dist_ac < dist_ad and
                                        math.fabs((dist_bc/dist_ad)-1) < maximal_difference_between_comparable_sides_in_percent and
                                        math.fabs((dist_ab/dist_cd)-1) < maximal_difference_between_comparable_sides_in_percent and
                                        math.fabs((dist_ac/dist_bd)-1) < maximal_difference_between_comparable_sides_in_percent):
                                        diagon_comp = math.fabs(max((dist_ad/dist_bc),(dist_bc/dist_ad))-1) 
                                        rects.add(FoundRect([window[a], window[c], window[potential_d], window[b], window[a]], posts))
                        except ZeroDivisionError:
                            pass
    return rects

class FoundRect:
    def __init__(self, corners, posts):
        self.corners = corners.copy()
        corners.sort()
        self.ident = str(corners)
        
        rect_points = []
        for point in self.corners:
            rect_points.append((posts[point][1], posts[point][2]))
        self.polygon = Polygon(rect_points)

    def setId(self, id):
        self.id = id

    def __eq__(self, other):
        return isinstance(other, FoundRect) and self.ident == other.ident

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.ident)
        
    def __lt__(self, other):
        return self.ident < other.ident

def find_rects(windows, posts, maximal_length_of_side, minimal_length_of_side, maximal_difference_between_comparable_sides_in_percent=0.1, number_of_computercores=4):
    start = time.time()

    calculated_rects = []

    pool = Pool(processes=number_of_computercores)

    results = []
    for w in windows:
        results.append(pool.apply_async(calcRectsInWindow, (w, posts, maximal_length_of_side, minimal_length_of_side, maximal_difference_between_comparable_sides_in_percent, )))

    current_calculated_windows = 0
    for result in results:
        calculated_rects.append(result.get())

        current_calculated_windows += 1
        print('\rCalculating rects {:3d}% - ({:3.3f}s)'.format(int(current_calculated_windows/len(windows)*100), (time.time()-start)), end='', flush=True)
  
    found_rects = []
    for rects_in_window in calculated_rects:
        found_rects += rects_in_window

    return list(set(found_rects))

def findBuildings(found_rects, posts, number_of_computercores=4):
    start = time.time()
    pool = Pool(processes=number_of_computercores)

    building_lists = []
    building_list = []
    divider = int(len(found_rects)/100) + 1
    i = 0
    for rect in found_rects:
        building_list.append(Building(rect))
        i += 1
        if i%divider == 0:
            building_lists.append(building_list)
            building_list = []
    
    results = []
    for building_list in building_lists:    
        results.append(pool.apply_async(constructBuilding, (building_list, found_rects, posts, )))

    buildings = set()
    current_checked_rects = 0
    for result in results:
        for building in result.get():
            if len(building.rooms) > 1:
                buildings.add(building)

        current_checked_rects += 1
        print('\rFinding buildings {:3d}% - ({:3.3f}s)'.format(int(current_checked_rects/len(results)*100), (time.time()-start)), end='', flush=True)

    return buildings

def constructBuilding(building_list, found_rects, posts):
    for building in building_list:
        for rect_to_add in found_rects:
            if building.hasRoom(rect_to_add):
                continue
            if isPartOfBuilding(rect_to_add, building, posts):
                building.addRoom(rect_to_add)
        
    return building_list

class Building:
    def __init__(self, rect):
        self.rooms = set()
        self.rooms.add(rect)
        self.ident = str([rect])

    def addRoom(self, rect):
        self.rooms.add(rect)
        self.ident = str(sorted(self.rooms))

    def hasRoom(self, rect):
        return rect in self.rooms

    def __eq__(self, other):
        return isinstance(other, Building) and self.ident == other.ident

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.ident)


def isPartOfBuilding(rect, building, posts, strict=True):

    connected = False

    for part in building.rooms:
        point_of_part_in_rect = []
        for point in part.corners:
            if point in rect.corners:
                point_of_part_in_rect.append(point)
        if len(point_of_part_in_rect) == 2:
            if (
                math.fabs(part.corners.index(point_of_part_in_rect[0]) - part.corners.index(point_of_part_in_rect[1])) == 1 and
                math.fabs(rect.corners.index(point_of_part_in_rect[0]) - rect.corners.index(point_of_part_in_rect[1])) == 1
            ):
                connected = True
                break
            
    if connected:
        overlaps = 0
        contains = 0

        for part in building.rooms:
            if part.polygon.overlaps(rect.polygon) or rect.polygon.overlaps(part.polygon):
                overlaps += 1
                if strict:
                    return False    
            if part.polygon.contains(rect.polygon) or rect.polygon.contains(part.polygon):
                return False
        
        if strict and overlaps == 0 and contains == 0:        
            return True
        if not strict and overlaps == 0:
            return True
    return False
