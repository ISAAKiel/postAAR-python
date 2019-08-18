import time
import math
from multiprocessing import Pool
from shapely.geometry import Polygon
#from qgis.core import QgsMessageLog

from .helper import * 

def calcRectsInWindow (window, x_values, y_values, maximal_length_of_side, minimal_length_of_side, maximal_difference_between_comparable_sides_in_percent=0.1):
    rects = []

    maximal_length_of_side *= maximal_length_of_side
    minimal_length_of_side *= minimal_length_of_side

    distance_in_window = calcDistanceInWindow(window, x_values, y_values, squared=True)
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
                                        dist_bd < maximal_length_of_side and dist_bd > minimal_length_of_side and
                                        dist_bc > dist_bd and
                                        dist_ac < dist_ad and
                                        math.fabs((dist_bc/dist_ad)-1) < maximal_difference_between_comparable_sides_in_percent and
                                        math.fabs((dist_ab/dist_cd)-1) < maximal_difference_between_comparable_sides_in_percent and
                                        math.fabs((dist_ac/dist_bd)-1) < maximal_difference_between_comparable_sides_in_percent):
                                        new_rect = [[window[a],window[c],window[potential_d],window[b],window[a]], 
                                                    [math.fabs(dist_bc/dist_ad-1)]]
                                        add_to_list(new_rect,rects)

                        except ZeroDivisionError:
                            pass
    return [rects]

def find_rects(windows, x_values, y_values, maximal_length_of_side, minimal_length_of_side, maximal_difference_between_comparable_sides_in_percent=0.1, multicore=False, number_of_computercores=4):
    start = time.time()

    calculated_rects = []
    if multicore:
        pool = Pool(processes=number_of_computercores)

        results = []
        for w in windows:
            results.append(pool.apply_async(calcRectsInWindow, (w, x_values, y_values, maximal_length_of_side, minimal_length_of_side, maximal_difference_between_comparable_sides_in_percent, )))

        current_calculated_windows = 0
        for result in results:
            calculated_rects.append(result.get())
            
            current_calculated_windows += 1
            print('\rCalculating rects {:3d}% - ({:3.3f}s)'.format(int(current_calculated_windows/len(windows)*100), (time.time()-start)), end='', flush=True)
#            info2user='Calculating rects {:3d}% - ({:3.3f}s)'.format(int(current_calculated_windows/len(windows)*100), (time.time()-start))
#            QgsMessageLog.logMessage(info2user, "Dataprocessing")
    else:
        current_calculated_windows = 0
        for w in windows:
            calculated_rects.append(calcRectsInWindow(w, x_values, y_values, maximal_length_of_side, minimal_length_of_side, maximal_difference_between_comparable_sides_in_percent))
        
            current_calculated_windows += 1
            print('\rCalculating rects {:3d}% - ({:3.3f}s)'.format(int(current_calculated_windows/len(windows)*100), (time.time()-start)), end='', flush=True)
            
    print('\nConsolidating rects')
    found_rects = []
    for rects_in_window in calculated_rects:
        print('\rConsolidating rects - {}'.format(len(found_rects)), end='')
        for rect in rects_in_window[0]:
            add_to_list(rect, found_rects)
    print()
    return found_rects

def findBuildings( found_rects, x_values, y_values):
    buildings = []
    for base_rect in range(len(found_rects)):
        building = []
        building.append(found_rects[base_rect])
        for rect_to_add in range(len(found_rects)):
            if rect_to_add == base_rect:
                continue
            if isPartOfBuilding(found_rects[rect_to_add], building, x_values, y_values):
                building.append(found_rects[rect_to_add])
        if len(building) > 1:
            buildings.append(building)
    return buildings

def isPartOfBuilding(rect,building, x_values, y_values, strict=True):

    connected = False

    for part in building:
        point_of_part_in_rect = []
        for point in part[0]:
            if point in rect[0]:
                point_of_part_in_rect.append(point)
        if len(point_of_part_in_rect) == 2:
            if (
                math.fabs(part[0].index(point_of_part_in_rect[0]) - part[0].index(point_of_part_in_rect[1])) == 1 and
                math.fabs(rect[0].index(point_of_part_in_rect[0]) - rect[0].index(point_of_part_in_rect[1])) == 1
            ):
                connected = True
                break
            
    if connected:
        overlaps = 0
        contains = 0

        rect_points = []
        for point in rect[0]:
            rect_points.append((x_values[point], y_values[point]))
        rect_polygon = Polygon(rect_points)
        for part in building:
            part_points = []
            for point in part[0]:
                part_points.append((x_values[point], y_values[point]))

            part_polygon = Polygon(part_points)
            if part_polygon.overlaps(rect_polygon) or rect_polygon.overlaps(part_polygon):
                overlaps += 1    
            if part_polygon.contains(rect_polygon) or rect_polygon.contains(part_polygon):
                contains += 1
        
        if strict and overlaps == 0 and contains == 0:        
            return True
        if not strict and overlaps == 0:
            return True
    return False
