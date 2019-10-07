import argparse
import time

import helper as hlp
import algorythm as alg

# Argumente: filename, returnfilename, maximal_length_of_side, minimal_length_of_side, maximal_difference_between_comparable_sides_in_percent, number_of_computercores
def parseCommandline():
    parser = argparse.ArgumentParser(prog='postAAR', description='Finding buildings in fields of posts')
    parser.add_argument('file', help='File containing postions of posts and their id - [id, x, y] per line')
    parser.add_argument('-outputfile', '-o', help='Filename for writing the results', default='output.buildings')
    parser.add_argument('-maximal_length_of_side', '-smax', help='Maximal length of the rectangle-sides', type=float, default=10.0)
    parser.add_argument('-minimal_length_of_side', '-smin', help='Minimal length of the rectangle-sides', type=float, default=2.0)
    parser.add_argument('-maximal_difference_between_comparable_sides_in_percent', '-diff', help='Maximal diffence for parallel sides in percent', type=float, default=0.05)
    parser.add_argument('-number_of_computercores', '-cores', help='Number of computercores used in computations', type=int, default=4)

    return parser.parse_args()

if __name__ == '__main__':
    start = time.time()

    arguments = parseCommandline()

    print('Loading data')
    posts = []
    with open(arguments.file) as f:
        for line in f:
            data = line.split()
            posts.append([float(data[0]), float(data[1]), float(data[2])])

    print('Loaded data (', (time.time()-start), 'ms)', sep='')

    print('Building windows')
    windows = hlp.buildWindows(posts, arguments.maximal_length_of_side)
    print('Build windows (', (time.time()-start), 's)', sep='')

    print('Finding rects', end='' , flush=True)
    found_rects = alg.find_rects(windows, posts, arguments.maximal_length_of_side, arguments.minimal_length_of_side, arguments.maximal_difference_between_comparable_sides_in_percent, number_of_computercores=arguments.number_of_computercores)
    print('Found {} rects in {:.3f}s'.format(len(found_rects), time.time()-start))

    #Add ids to rects
    id = 0
    for rect in found_rects:
        rect.setId(id)
        id += 1

    print('Finding buildings', flush=True)
    buildings = alg.findBuildings(found_rects, posts)
    print('\nFound {} buildings in {:.3f}s'.format(len(buildings), time.time()-start))

    print('Writing data to file', arguments.outputfile)
    posts = []
    with open(arguments.outputfile, 'w') as f:
        f.write('rectangles\n')
        for rect in found_rects:
            f.write(str(rect.id) + ' ' + " ".join(str(i) for i in rect.corners) + '\n')
        f.write('buildings\n')
        for building in buildings:
            f.write(" ".join(str(i.id) for i in building.rooms) + '\n')

"""
import csv
import math
import itertools
import matplotlib.pyplot as plt
import numpy as np

# eigene Funktionen
import helper as hlp
import algorythm as alg

if __name__ == '__main__':
	print('Loading data')
	start = time.time()
	x_values, y_values = hlp.loadDataFromFile( filename, x_value_position_in_dataset, y_value_position_in_dataset, read_set_of_Data_from_end )
	print('Loaded data (',(time.time()-start),') max=(', max(x_values), ',', max(y_values), ') min=(', min(x_values), ',', min(y_values), ') diff= x=', max(x_values)-min(x_values), ', y=', max(y_values)-min(y_values), sep='')

	print('Visualising data')
	hlp.showPointPlot(x_values, y_values)

	print('Building windows')
	start = time.time()
	windows = hlp.buildWindows(x_values, y_values, min(x_values) - 1, max(x_values) + 1, min(y_values) - 1, max(y_values) + 1, maximal_length_of_side)
	print('Build windows (',(time.time()-start),'s)', sep='')

	print('Finding rects', end='' , flush=True)
	start = time.time()
	found_rects = alg.find_rects(windows, x_values, y_values, maximal_length_of_side, minimal_length_of_side, maximal_difference_between_comparable_sides_in_percent,  number_of_computercores=number_of_computercores)
	print('Found {} rects in {:.3f}s'.format(len(found_rects), time.time()-start))
		
	hlp.showRectangales(found_rects, x_values, y_values, block=False, name="Gefundene Rechtecke")

	print('Finding buildings', flush=True)
	start = time.time()
	buildings = alg.findBuildings(found_rects, x_values, y_values)
	print('Found {} buildings in {:.3f}s'.format(len(buildings), time.time()-start))

	hlp.showBuildings(buildings, x_values, y_values, False)
	buildings.sort(key=lambda l : len(l), reverse=True)
	hlp.showBuildings(buildings[:10], x_values, y_values, False, name="10 größten Gebäude")

	print('Press Enter to exit...')
	input()
"""