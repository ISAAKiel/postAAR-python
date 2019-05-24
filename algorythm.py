import time
import math
from multiprocessing import Pool

import helper as hlp

def calcRectsInWindow (window, x_values, y_values, maximal_length_of_side, minimal_length_of_side, maximal_difference_to_perfect_point, min_mid_dist, maximal_degree_diviation_to_right_angle):
	rects = []
	possible_rects = []
	distance_in_window = hlp.calcDistanceInWindow(window, x_values, y_values)
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
							# expensive! - change to better
							t = ((x_values[window[c]]-x_values[window[a]]) * (x_values[window[b]]-x_values[window[a]]) + (y_values[window[c]]-y_values[window[a]]) * (y_values[window[b]]-y_values[window[a]])) / (math.pow(x_values[window[b]]-x_values[window[a]], 2) + math.pow(y_values[window[b]]-y_values[window[a]],2))
							possible_cx=x_values[window[a]]+t*(x_values[window[b]]-x_values[window[a]])
							possible_cy=y_values[window[a]]+t*(y_values[window[b]]-y_values[window[a]])

							dist_to_real_c = hlp.distance_points([x_values[window[a]], y_values[window[a]]], [possible_cx,possible_cy])

							if dist_to_real_c < maximal_difference_to_perfect_point:
								dx = x_values[window[c]] + x_values[window[b]] - x_values[window[a]]
								dy = y_values[window[c]] + y_values[window[b]] - y_values[window[a]]

								found_real_point = False
								for potential_d in window:
									dist_to_real_d = hlp.distance_points([x_values[potential_d], y_values[potential_d]], [dx,dy])
									if dist_to_real_d < maximal_difference_to_perfect_point:
										found_real_point = True
										new_rect = [[x_values[window[a]],x_values[window[c]],x_values[potential_d],x_values[window[b]],x_values[window[a]]],
													[y_values[window[a]],y_values[window[c]],y_values[potential_d],y_values[window[b]],y_values[window[a]]], 
													[dist_to_real_c + dist_to_real_d], 
													[(x_values[window[a]]+x_values[window[b]]+x_values[window[c]]+x_values[potential_d])/4, (y_values[window[a]]+y_values[window[b]]+y_values[window[c]]+y_values[potential_d])/4]]
										hlp.add_to_list(new_rect,rects, min_mid_dist=min_mid_dist)

								if not found_real_point:
									new_rect = [[x_values[window[a]],x_values[window[c]],dx,x_values[window[b]],x_values[window[a]]],[y_values[window[a]],y_values[window[c]],dy,y_values[window[b]],y_values[window[a]]],
												[dist_to_real_c + maximal_difference_to_perfect_point], 
												[(x_values[window[a]]+x_values[window[b]]+x_values[window[c]]+dx)/4, (y_values[window[a]]+y_values[window[b]]+y_values[window[c]]+dy)/4]]
									if not hlp.add_to_list(new_rect, rects, min_mid_dist=min_mid_dist, replace = False, add = False):
										hlp.add_to_list(new_rect,possible_rects, min_mid_dist=min_mid_dist)

						except ZeroDivisionError:
							pass
	return [rects, possible_rects]

def find_rects(windows, x_values, y_values, maximal_length_of_side, minimal_length_of_side, maximal_difference_to_perfect_point, min_mid_dist, maximal_degree_diviation_to_right_angle, multicore=True, number_of_computercores=4):
	start = time.time()

	calculated_rects = []
	if multicore:
		pool = Pool(processes=number_of_computercores)

		results = []
		for w in windows:
			results.append(pool.apply_async(calcRectsInWindow, (w, x_values, y_values, maximal_length_of_side, minimal_length_of_side, maximal_difference_to_perfect_point, min_mid_dist, maximal_degree_diviation_to_right_angle)))

		current_calculated_windows = 0
		for result in results:
			calculated_rects.append(result.get())
			
			current_calculated_windows += 1
			print('\rCalculating rects {:3d}% - ({:3.3f}s)'.format(int(current_calculated_windows/len(windows)*100), (time.time()-start)), end='', flush=True)
	else:
		current_calculated_windows = 0
		for w in windows:
			calculated_rects.append(calcRectsInWindow(w, x_values, y_values, maximal_length_of_side, minimal_length_of_side, maximal_difference_to_perfect_point, min_mid_dist, maximal_degree_diviation_to_right_angle))
			
			current_calculated_windows += 1
			print('\rCalculating rects {:3d}% - ({:3.3f}s)'.format(int(current_calculated_windows/len(windows)*100), (time.time()-start)), end='', flush=True)

	print('\nConsolidating rects')
	found_rects = []
	possible_rects = []
	for rects_in_window in calculated_rects:
		for rect in rects_in_window[0]:
			hlp.add_to_list(rect, found_rects, min_mid_dist=min_mid_dist)
		for possible_rect in rects_in_window[1]:
			hlp.add_to_list(possible_rect, possible_rects, min_mid_dist=min_mid_dist)

	return found_rects, possible_rects
