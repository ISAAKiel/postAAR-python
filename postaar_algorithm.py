import argparse
import time
import tempfile
import os
import sys

import helper as hlp
import algorythm as alg
    

# Argumente: filename, returnfilename, maximal_length_of_side, minimal_length_of_side, maximal_difference_between_comparable_sides_in_percent, number_of_computercores
def parseCommandline():
    parser = argparse.ArgumentParser(prog='postAAR', description='Finding buildings in fields of posts')
    parser.add_argument('file', help='File containing postions of posts and their id - [id, x, y] per line')
    parser.add_argument('-outputfile', '-o', help='Filename for writing the results', default='output.buildings')
    parser.add_argument('-maximal_length_of_side', '-smax', help='Maximal length of the rectangle-sides', type=float, default=10.0)
    parser.add_argument('-minimal_length_of_side', '-smin', help='Minimal length of the rectangle-sides', type=float, default=2.0)
    parser.add_argument('-maximal_difference_between_comparable_sides_in_percent', '-sdiff', help='Maximal diffence for parallel sides in percent', type=float, default=0.05)
    parser.add_argument('-maximal_length_of_diagonals', '-dmax', help='Maximal length of the diagonals in percentage of sides', type=float, default=1.5)
    parser.add_argument('-minimal_length_of_diagonals', '-dmin', help='Minimal length of the diagonals in percentage of sides', type=float, default=0.0)
    parser.add_argument('-maximal_difference_between_diagonals_in_percent', '-ddiff', help='Maximal diffence for diagonals in percent', type=float, default=1.0)
    parser.add_argument('-number_of_computercores', '-cores', help='Number of computercores used in computations', type=int, default=4)

    return parser.parse_args()

if __name__ == '__main__':
    try:
        print(str(sys.argv))
        start = time.time()

        arguments = parseCommandline()
        
        print('Loading data')
        posts = []
        with open(os.path.join(tempfile.gettempdir(), arguments.file)) as f:
            for line in f:
                data = line.split()
                posts.append([float(data[0]), float(data[1]), float(data[2])])

        print('Loaded data (', (time.time()-start), 'ms)', sep='')

        print('Building windows')
        windows = hlp.buildWindows(posts, arguments.maximal_length_of_side)
        print('Build windows (', (time.time()-start), 's)', sep='')

        print('Finding rects', end='' , flush=True)
        found_rects = alg.find_rects(windows, posts, arguments.maximal_length_of_side, arguments.minimal_length_of_side, arguments.maximal_difference_between_comparable_sides_in_percent, arguments.maximal_length_of_diagonals, arguments.minimal_length_of_diagonals, arguments.maximal_difference_between_diagonals_in_percent, number_of_computercores=arguments.number_of_computercores)
        print('\nFound {} rects in {:.3f}s'.format(len(found_rects), time.time()-start))

        #Add ids to rects
        id = 0
        for rect in found_rects:
            rect.setId(id)
            id += 1

        print('Finding buildings', end='', flush=True)
        buildings = alg.findBuildings(found_rects, posts, number_of_computercores=arguments.number_of_computercores)
        print('\nFound {} buildings in {:.3f}s'.format(len(buildings), time.time()-start))

        print('Writing data to file', arguments.outputfile)
        posts = []
        with open(os.path.join(tempfile.gettempdir(), arguments.outputfile), 'w') as f:
            f.write('rectangles\n')
            for rect in found_rects:
                f.write(str(rect.id) + ' ' + " ".join(str(i) for i in rect.corners[0:4]) + ' ' + str(rect.diff_sides_max) + ' ' + str(rect.diff_diagonals) + '\n')
            f.write('buildings\n')
            for building in buildings:
                f.write(" ".join(str(i.id) for i in building.rooms) + '\n')
    except:    
        input("\npress Enter to continue")