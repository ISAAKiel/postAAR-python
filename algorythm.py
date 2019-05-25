import time
import math
from multiprocessing import Pool

import helper as hlp

def calcRectsInWindow (window, x_values, y_values, maximal_length_of_side, minimal_length_of_side, min_mid_dist, maximal_difference_between_comparable_sides_in_percent=0.1):
	rects = []

	maximal_length_of_side *= maximal_length_of_side
	minimal_length_of_side *= minimal_length_of_side

	distance_in_window = hlp.calcDistanceInWindow(window, x_values, y_values, squared=True)
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
										new_rect = [[x_values[window[a]],x_values[window[c]],x_values[window[potential_d]],x_values[window[b]],x_values[window[a]]],
													[y_values[window[a]],y_values[window[c]],y_values[window[potential_d]],y_values[window[b]],y_values[window[a]]], 
													[math.fabs(dist_bc/dist_ad-1)], 
													[(x_values[window[a]]+x_values[window[b]]+x_values[window[c]]+x_values[window[potential_d]])/4, (y_values[window[a]]+y_values[window[b]]+y_values[window[c]]+y_values[window[potential_d]])/4]]
										hlp.add_to_list(new_rect,rects, min_mid_dist=min_mid_dist)

						except ZeroDivisionError:
							pass
	return [rects]

def find_rects(windows, x_values, y_values, maximal_length_of_side, minimal_length_of_side, min_mid_dist, maximal_difference_between_comparable_sides_in_percent=0.1, multicore=True, number_of_computercores=4):
	start = time.time()

	calculated_rects = []
	if multicore:
		pool = Pool(processes=number_of_computercores)

		results = []
		for w in windows:
			results.append(pool.apply_async(calcRectsInWindow, (w, x_values, y_values, maximal_length_of_side, minimal_length_of_side, min_mid_dist, maximal_difference_between_comparable_sides_in_percent, )))

		current_calculated_windows = 0
		for result in results:
			calculated_rects.append(result.get())
			
			current_calculated_windows += 1
			print('\rCalculating rects {:3d}% - ({:3.3f}s)'.format(int(current_calculated_windows/len(windows)*100), (time.time()-start)), end='', flush=True)
	else:
		current_calculated_windows = 0
		for w in windows:
			calculated_rects.append(calcRectsInWindow(w, x_values, y_values, maximal_length_of_side, minimal_length_of_side, min_mid_dist, maximal_difference_between_comparable_sides_in_percent))
			
			current_calculated_windows += 1
			print('\rCalculating rects {:3d}% - ({:3.3f}s)'.format(int(current_calculated_windows/len(windows)*100), (time.time()-start)), end='', flush=True)

	print('\nConsolidating rects')
	found_rects = []
	for rects_in_window in calculated_rects:
		print('\rConsolidating rects - {}'.format(len(found_rects)), end='')
		for rect in rects_in_window[0]:
			hlp.add_to_list(rect, found_rects, min_mid_dist=min_mid_dist)
	print()
	return found_rects
