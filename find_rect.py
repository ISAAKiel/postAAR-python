import csv
import math
import itertools
import matplotlib.pyplot as plt
import numpy as np
import time

# eigene Funktionen
import helper as hlp
import algorythm as alg

#Configuration
read_set_of_Data_from_end = False
number_of_computercores = 3

# pfahltest.txt
#filename = 'pfahltest.txt'
#x_value_position_in_dataset,y_value_position_in_dataset = 0,1
#maximal_length_of_side = 50.0
#minimal_length_of_side = 0.1
#maximal_difference_to_perfect_point = 2.0
#maximal_degree_diviation_to_right_angle = 20.0

# newtest.dat
filename = 'newtest.dat'
x_value_position_in_dataset,y_value_position_in_dataset = 1,2
maximal_length_of_side = 45.0
minimal_length_of_side = 2.5
maximal_difference_to_perfect_point = 5.0
maximal_degree_diviation_to_right_angle = 5.0

# zuerich_selected.txt
#filename = 'zuerich_selected.txt'
#x_value_position_in_dataset,y_value_position_in_dataset = 1,0
#read_set_of_Data_from_end = True
#maximal_length_of_side = 4.5
#minimal_length_of_side = 2.5
#maximal_difference_to_perfect_point = 5.0
#maximal_degree_diviation_to_right_angle = 20.0

min_mid_dist = 0.5

if __name__ == '__main__':
	print('Loading data')
	start = time.time()
	x_values, y_values = hlp.loadDataFromFile( filename, x_value_position_in_dataset, y_value_position_in_dataset, read_set_of_Data_from_end )
	print('Loaded data (',(time.time()-start),') max=(', min(x_values), ',', max(y_values), ') min=(', min(x_values), ',', min(y_values), ') diff= x=', max(x_values)-min(x_values), ', y=', max(y_values)-min(y_values), sep='')

	print('Visualising data')
	hlp.showPointPlot(x_values, y_values)

	print('Building windows')
	start = time.time()
	windows = hlp.buildWindows(x_values, y_values, min(x_values) - 1, max(x_values) + 1, min(y_values) - 1, max(y_values) + 1, maximal_length_of_side)
	print('Build windows (',(time.time()-start),'s)', sep='')

	print('Finding rects', end='' , flush=True)
	start = time.time()
	found_rects, poss_rects = alg.find_rects(windows, x_values, y_values, maximal_length_of_side, minimal_length_of_side, maximal_difference_to_perfect_point, min_mid_dist, maximal_degree_diviation_to_right_angle, multicore=False, number_of_computercores=number_of_computercores)
	end = time.time()
	print('Found {} rects, {} possible rects in {:.3f}s'.format(len(found_rects), len(poss_rects), end-start))
		
	hlp.showRectangales(poss_rects, x_values, y_values, block=False, name="Mögliche Rechtecke")
	hlp.showRectangales(found_rects, x_values, y_values, block=False, name="Gefundene Rechtecke")
	
	print('Press Enter to exit...')
	input()

