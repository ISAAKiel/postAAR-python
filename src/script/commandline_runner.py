import argparse
import time
import tempfile
import os
import sys

try:
    import algorithm.helper as hlp
    import algorithm.algorithm as alg


    # Argumente: filename, returnfilename, maximal_length_of_side, minimal_length_of_side, maximal_difference_between_comparable_sides_in_percent, number_of_computercores
    def parseCommandline():
        parser = argparse.ArgumentParser(prog='postAAR', description='Finding buildings in fields of posts')
        parser.add_argument('file', help='File containing postions of posts and their id - [id, x, y] per line')
        parser.add_argument('-outputfile', '-o', help='Filename for writing the results', default='output.buildings')
        parser.add_argument('-maximal_length_of_side', '-smax', help='Maximal length of the rectangle-sides', type=float, default=10.0)
        parser.add_argument('-minimal_length_of_side', '-smin', help='Minimal length of the rectangle-sides', type=float, default=2.0)
        parser.add_argument('-maximal_difference_between_area_to_perfect_rectangle', '-adiff', help='Maximal diffence for area from perfect enclosing to real rectangle', type=float, default=0.05)
        parser.add_argument('-number_of_computercores', '-cores', help='Number of computercores used in computations', type=int, default=4)

        return parser.parse_args()

    if __name__ == '__main__':
        try:
            print(str(sys.argv))
            start = time.time()

            arguments = parseCommandline()

            print('Loading data')
            posts = dict()
            with open(os.path.join(tempfile.gettempdir(), arguments.file)) as f:
                for line in f:
                    data = line.split()
                    posts[int(data[0])] = [float(data[1]), float(data[2])]

            print('Loaded data (', (time.time()-start), 'ms)', sep='')

            print('Building windows')
            windows = hlp.buildWindows(posts, arguments.maximal_length_of_side)
            print('Build windows (', (time.time()-start), 's)', sep='')

            print('Finding rects', end='' , flush=True)
            found_rects = alg.find_rects(windows, posts, arguments.maximal_length_of_side, arguments.minimal_length_of_side, arguments.maximal_difference_between_area_to_perfect_rectangle, number_of_computercores=arguments.number_of_computercores)
            print('\nFound {} rects in {:.3f}s'.format(len(found_rects), time.time()-start))

            print('Finding buildings', end='', flush=True)
            buildings = alg.findBuildings(found_rects, posts, number_of_computercores=arguments.number_of_computercores)
            print('\nFound {} buildings in {:.3f}s'.format(len(buildings), time.time()-start))

            print('Writing data to file', arguments.outputfile)

            with open(os.path.join(tempfile.gettempdir(), arguments.outputfile), 'w') as f:
                f.write('{\n\t"rectangles": [\n\t\t')
                f.write((",\n\t\t".join(rectangle.toJson() for rectangle in found_rects)))
                f.write('\n\t],\n\t"buildings": [\n\t\t')
                f.write((",\n\t\t".join(building.toJson() for building in buildings)))
                f.write('\t]\n}')

            input("\npress Enter to continue")
        except:
            print("Unexpected error:", sys.exc_info())
            input("\npress Enter to continue")

except:
    print("Unexpected error:", sys.exc_info())
    input("\npress Enter to continue")