import math
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool
import random
import time

#double result = atan2(P3.y - P1.y, P3.x - P1.x) -
#                atan2(P2.y - P1.y, P2.x - P1.x);
def degree_over_b(a, b, c):
    return math.atan2(c[1]-b[1],c[0]-b[0]) - math.atan2(a[1]-b[1],a[0]-b[0]) / math.pi * 90

def distance_points(a,b):
		return math.hypot(abs(b[0] - a[0]), abs(b[1] - a[1]))

def calcDistanceInWindow (window, posts):
    window_distance = [[0.0 for point_a in range(len(window))] for point_b in range(len(window))]
    for point_a in range(len(window)):
        for point_b in range(len(window)):
            if point_a != point_b and (window_distance[point_a][point_b] == 0 or window_distance[point_b][point_a] == 0):
                distance_ab = math.sqrt(math.pow(posts[window[point_b]][1] - posts[window[point_a]][1], 2) + math.pow(posts[window[point_b]][2] - posts[window[point_a]][2],2))
                window_distance[point_a][point_b] = distance_ab
                window_distance[point_b][point_a] = distance_ab
    return window_distance

def loadDataFromFile( filename, x_value_position_in_dataset, y_value_position_in_dataset, readFromEnd=False ):
    x_values,y_values = [],[]
    with open(filename) as f:
        for l in f:
            temp = l.split()
            if len(temp) >= x_value_position_in_dataset and len(temp) >= y_value_position_in_dataset:
                try:
                    if readFromEnd:
                        x_values.append(float(temp[len(temp)-x_value_position_in_dataset-1]))
                        y_values.append(float(temp[len(temp)-y_value_position_in_dataset-1]))
                    else:
                        x_values.append(float(temp[x_value_position_in_dataset]))
                        y_values.append(float(temp[y_value_position_in_dataset]))
                except ValueError:
                    pass

    return x_values, y_values

def buildWindows(posts, maximal_length_of_side):
    min_value_x = min([post[1] for post in posts]) - 1
    min_value_y = min([post[2] for post in posts]) - 1
    max_value_x = max([post[1] for post in posts]) + 1
    max_value_y = max([post[2] for post in posts]) + 1

    window_x = min_value_x
    window_y = min_value_y

    window_size = 3 * maximal_length_of_side

    windows = []

    while window_y < max_value_y:
        
        window_x = min_value_x

        while window_x < max_value_x:

            points_in_window = []
            for p in range(len(posts)):
                if posts[p][1] > window_x and posts[p][1] < (window_x + window_size) and posts[p][2] > window_y and posts[p][2] < (window_y + window_size):
                    points_in_window.append(p)
            windows.append(points_in_window)
        
            window_x += window_size/2
        window_y += window_size/2
    return windows

def showRectangales(rectangles, posts, block=True, name='Rechtecke', x_axis='x in m', y_axis='y in m', point_size=10):
    
    fig_rectangle = plt.figure()
    fig_rectangle.canvas.set_window_title(name)
    rectangle_plot = fig_rectangle.add_subplot(111)
    rectangle_plot.set_title(name)
    rectangle_plot.set_xlabel(x_axis)
    rectangle_plot.set_ylabel(y_axis)
    rectangle_plot.grid(True)
    rectangle_plot.axis('equal')

    for r in rectangles:
        x_points, y_points = [], []
        for p in r.corners:
            x_points.append(posts[p][1])
            y_points.append(posts[p][2])
        rectangle_plot.plot(x_points, y_points,'b',linewidth=1.0)

    rectangle_plot.scatter([post[1] for post in posts], [post[2] for post in posts], c='r', s=point_size)

    fig_rectangle.show()
    if block:
        print("Press Key to continue...")
        plt.waitforbuttonpress(0)

def runInThread( function, args = () ):
    pool = Pool(processes=2)
    return pool.apply_async(function, args).get()

def showBuildings(buildings, posts, block=True, name='Gebäude', x_axis='x in m', y_axis='y in m', point_size=10):
    
	fig_rectangle = plt.figure()
	fig_rectangle.canvas.set_window_title(name)
	rectangle_plot = fig_rectangle.add_subplot(111)
	rectangle_plot.set_title(name)
	rectangle_plot.set_xlabel(x_axis)
	rectangle_plot.set_ylabel(y_axis)
	rectangle_plot.grid(True)
	rectangle_plot.axis('equal')

	for building in buildings:
		building_color = (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))
		for r in building.rooms:
			x_points, y_points = [], []
			for p in r.corners:
				x_points.append(posts[p][1])
				y_points.append(posts[p][2])
			rectangle_plot.plot(x_points, y_points, c=building_color,linewidth=1.0)

	rectangle_plot.scatter([post[1] for post in posts], [post[2] for post in posts], c='r', s=point_size)

	fig_rectangle.show()
	if block:
		print("Press Key to continue...")
		plt.waitforbuttonpress(0)
    