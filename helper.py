import math
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool

#double result = atan2(P3.y - P1.y, P3.x - P1.x) -
#                atan2(P2.y - P1.y, P2.x - P1.x);
def degree_over_b(a, b, c):
    return math.atan2(c[1]-b[1],c[0]-b[0]) - math.atan2(a[1]-b[1],a[0]-b[0]) / math.pi * 90

def equal(a,b):
	return np.array_equal(np.sort(np.array(a)),np.sort(np.array(b)))

def distance_points(a,b):
		return math.hypot(abs(b[0] - a[0]), abs(b[1] - a[1]))

def add_to_list(new_rect, found_rects, min_mid_dist=0.0, replace = True, add=True):
	exists = False
	for r in range(len(found_rects)):
		if distance_points(found_rects[r][3], new_rect[3]) < min_mid_dist:
			if found_rects[r][2] > new_rect[2] and replace:
				found_rects[r] = new_rect
			exists = True
			break
	if not exists and add:
		found_rects.append(new_rect)
	return exists

def calcDistanceInWindow (window, x_values, y_values):
	window_distance = [[0.0 for point_a in range(len(window))] for point_b in range(len(window))]
	for point_a in range(len(window)):
		for point_b in range(len(window)):
			if point_a != point_b and (window_distance[point_a][point_b] == 0 or window_distance[point_b][point_a] == 0):
				distance_ab = math.sqrt(math.pow(x_values[window[point_b]] - x_values[window[point_a]], 2) + math.pow(y_values[window[point_b]] - y_values[window[point_a]],2))
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

def buildWindows(x_values, y_values, min_value_x, max_value_x, min_value_y, max_value_y, maximal_length_of_side):
    window_x = min_value_x
    window_y = min_value_y

    window_size = 3 * maximal_length_of_side

    windows = []

    while window_y < max_value_y:
        
        window_x = min_value_x

        while window_x < max_value_x:

            points_in_window = []
            for p in range(len(x_values)):
                if x_values[p] > window_x and x_values[p] < (window_x + window_size) and y_values[p] > window_y and y_values[p] < (window_y + window_size):
                    points_in_window.append(p)
            windows.append(points_in_window)
        
            window_x += window_size/2
        window_y += window_size/2
    return windows


def showPointPlot(x_values, y_values, block=True, name='Pfostenlöcher', x_axis='x in m', y_axis='y in m', point_size=10):
    plt.ion()
    fig_pfostenloecher = plt.figure()
    fig_pfostenloecher.canvas.set_window_title(name)

    pfostenloecher = fig_pfostenloecher.add_subplot(111)
    pfostenloecher.set_title(name)
    pfostenloecher.set_xlabel(x_axis)
    pfostenloecher.set_ylabel(y_axis)
    pfostenloecher.grid(True)
    pfostenloecher.scatter(x_values, y_values, c='r', s=point_size)
    fig_pfostenloecher.show()
    if block:
        print("Press Key to continue...")
        plt.waitforbuttonpress(0)

def showRectangales(rectangles, x_values, y_values, block=True, name='Rechtecke', x_axis='x in m', y_axis='y in m', point_size=10):
    
    fig_rectangle = plt.figure()
    fig_rectangle.canvas.set_window_title(name)
    rectangle_plot = fig_rectangle.add_subplot(111)
    rectangle_plot.set_title(name)
    rectangle_plot.set_xlabel(x_axis)
    rectangle_plot.set_ylabel(y_axis)
    rectangle_plot.grid(True)

    for r in rectangles:
        rectangle_plot.plot(r[0],r[1],'b',linewidth=1.0)

    rectangle_plot.scatter(x_values, y_values, c='r', s=point_size)

    fig_rectangle.show()
    if block:
        print("Press Key to continue...")
        plt.waitforbuttonpress(0)

def runInThread( function, args = () ):
    pool = Pool(processes=2)
    return pool.apply_async(function, args).get()
    