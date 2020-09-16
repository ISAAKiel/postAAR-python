import math
import time
from json import JSONEncoder

#double result = atan2(P3.y - P1.y, P3.x - P1.x) -
#                atan2(P2.y - P1.y, P2.x - P1.x);
def degree_over_b(a, b, c):
    return math.atan2(c[1]-b[1],c[0]-b[0]) - math.atan2(a[1]-b[1],a[0]-b[0]) / math.pi * 90

def distance_points(a,b):
        return math.hypot(abs(b[0] - a[0]), abs(b[1] - a[1]))

all_distances = dict()

def resetDistances():
    all_distances.clear()

def calcDistanceInWindow (window, posts, max_distance, min_distance):
    for point_a in range(len(window)):
        if not window[point_a] in all_distances:
            all_distances[window[point_a]] = dict()

        point_a_x = posts[window[point_a]][1]
        point_a_y = posts[window[point_a]][2]
    
        for point_b in range(len(window)):
            point_b_x = posts[window[point_b]][1]
            point_b_y = posts[window[point_b]][2]

            if window[point_a] < window[point_b]:
                if min_distance < (abs(point_b_x - point_a_x) + abs(point_b_y - point_a_y)) < max_distance*2:
                    distance_ab = math.sqrt(math.pow(point_b_x - point_a_x, 2) + math.pow(point_b_y - point_a_y,2))
                    all_distances[window[point_a]][window[point_b]] = distance_ab
                else:
                    all_distances[window[point_a]][window[point_b]] = max_distance * 2

def getDistanceAB(point_a, point_b):
    if point_a != point_b:
        if point_a < point_b:
            return all_distances[point_a][point_b]
        else:
            return all_distances[point_b][point_a]
    else:
        return 0

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

# https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
def ccw(A, B, C, posts):
    return (posts[C][2]-posts[A][2])*(posts[B][1]-posts[A][1]) > (posts[B][2]-posts[A][2])*(posts[C][1]-posts[A][1])

def intersect(A, B, C, D, posts):
    return ccw(A,C,D, posts) != ccw(B,C,D, posts) and ccw(A,B,C, posts) != ccw(A,B,D, posts)

class ProgressReport:
    def __init__(self, step=0.25, break_on_end=True):
        self.step = step
        self.break_on_end = break_on_end
        self.started = False

        self.restartTimer()

    def restartTimer(self):
        self.start_time = time.time()
        self.last_progress_report = time.time()
        self.started = True

    def printProgress( self, text, percent ):
        if not self.started:
            self.startTimer()

        if (time.time() - self.last_progress_report) >= self.step:
            self.last_progress_report = time.time()
            print('\r{} {:3d}% - ({:3.3f}s)'.format(text, int(percent*100), (time.time() - self.start_time)), end='', flush=True)
        if self.break_on_end and percent >= 1:
            print('\r{} {:3d}% - ({:3.3f}s)'.format(text, int(percent*100), (time.time() - self.start_time)), end='\n', flush=True)
