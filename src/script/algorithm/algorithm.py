import time
from multiprocessing import Pool

from .building import Building
from .helper import *
from .rect import Rect


def calcRectsInWindow (window, posts, maximal_length_of_side, minimal_length_of_side, maximal_bounding_area_difference):
    rects = set()

    calcDistanceInWindow(window, posts, maximal_length_of_side, minimal_length_of_side)
    
    for a in window:
        for b in window:
            if a == b:
                break

            dist_side_ab = getDistanceAB(a, b)

            if minimal_length_of_side <= dist_side_ab <= maximal_length_of_side:
                for d in window:
                    if d == b or d == a:
                        break

                    dist_side_ad = getDistanceAB(a, d)
                    
                    if minimal_length_of_side <= dist_side_ad <= maximal_length_of_side:
                        
                        for potential_c in window:
                            
                            dist_side_bc = getDistanceAB(b, potential_c)
                            dist_side_dc = getDistanceAB(d, potential_c)
                                
                            if (
                                minimal_length_of_side <= dist_side_bc <= maximal_length_of_side and 
                                minimal_length_of_side <= dist_side_dc <= maximal_length_of_side and

                                intersect(a, potential_c, b, d, posts)
                                ):


                                possible_rect = Rect([a, b, potential_c, d], posts, 0, 0)
                        
                                if possible_rect.isRectangle(maximal_bounding_area_difference):
                                    rects.add(possible_rect)
    return rects


def find_rects(windows, posts, maximal_length_of_side, minimal_length_of_side, maximal_bounding_area_difference, number_of_computercores=4, debug=True):
    progress = ProgressReport()
    resetDistances()

    calculated_rects = []
    if number_of_computercores > 1:
        pool = Pool(processes=number_of_computercores)

        results = []
        for w in windows:
            results.append(pool.apply_async(calcRectsInWindow, (w, posts, maximal_length_of_side, minimal_length_of_side, maximal_bounding_area_difference, )))

        current_calculated_windows = 0
        for result in results:
            calculated_rects.append(result.get())

            if debug:
                current_calculated_windows += 1
                progress.printProgress('Calculating rects', current_calculated_windows/len(windows))
    
        found_rects = []
        for rects_in_window in calculated_rects:
            found_rects += rects_in_window
    else:
        results = []
        current_calculated_windows = 0
        for w in windows:
            calculated_rects.append(calcRectsInWindow(w, posts, maximal_length_of_side, minimal_length_of_side, maximal_bounding_area_difference ))

            if debug:
                current_calculated_windows += 1
                progress.printProgress('Calculating rects', current_calculated_windows/len(windows))
    
        found_rects = []
        for rects_in_window in calculated_rects:
            found_rects += rects_in_window

    rectangles = list(set(found_rects))

    id = 0
    for rect in rectangles:
        rect.setId(id)
        id += 1

    return rectangles

def findBuildings(found_rects, posts, number_of_computercores=4):
    progress = ProgressReport()

    if number_of_computercores > 1:
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
            progress.printProgress('Finding buildings', current_checked_rects/len(results))
    else:
        building_list = []
        for rect in found_rects:
            building_list.append(Building(rect))
        
        buildings = set()
        current_checked_rects = 0
        for building in constructBuilding(building_list, found_rects, posts ):
            if len(building.rooms) > 1:
                buildings.add(building)

            current_checked_rects += 1
            progress.printProgress('Finding buildings', current_checked_rects/len(building_list))

    id = 0
    for building in buildings:
        building.setId(id)
        id += 1

    return buildings

def constructBuilding(building_list, found_rects, posts):
    for building in building_list:
        for rect_to_add in found_rects:
            if building.hasRoom(rect_to_add):
                continue
            if isPartOfBuilding(rect_to_add, building, posts):
                building.addRoom(rect_to_add)
        
    return building_list


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
            try:
                if part.polygon.overlaps(rect.polygon) or rect.polygon.overlaps(part.polygon):
                    overlaps += 1
                    if strict:
                        return False
                if part.polygon.contains(rect.polygon) or rect.polygon.contains(part.polygon):
                    return False
            except:
                print(building, rect)
                return False
        
        if strict and overlaps == 0 and contains == 0:        
            return True
        if not strict and overlaps == 0:
            return True
    return False
