import math
import time
from json import JSONEncoder


# double result = atan2(P3.y - P1.y, P3.x - P1.x) - atan2(P2.y - P1.y, P2.x - P1.x);
def degree_over_b(a, b, c):
    return math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]) / math.pi * 90


def distance_points(a, b):
    return math.hypot(abs(b[0] - a[0]), abs(b[1] - a[1]))


from scipy.spatial import distance
def calcDistance(windows, posts, max_distance, min_distance):
    all_distances = dict()

    for w in windows:
        p = [(posts[w[i]][0], posts[w[i]][1]) for i in range(len(w))]
        d = distance.cdist(p, p, 'euclidean')

        for i in range(len(w)):
            if w[i] not in all_distances:
                all_distances[w[i]] = dict()
            for j in range(len(w)):
                if min_distance <= d[i][j] <= max_distance:
                    all_distances[w[i]][w[j]] = d[i][j]
                else:
                    all_distances[w[i]][w[j]] = max_distance * 2

    calcs = 0
    for distances in all_distances.values():
        calcs += len(distances)
    print(calcs)

    return all_distances


def buildWindows(posts, maximal_length_of_side):
    min_value_x = min([post[0] for post in posts.values()]) - 1
    min_value_y = min([post[1] for post in posts.values()]) - 1
    max_value_x = max([post[0] for post in posts.values()]) + 1
    max_value_y = max([post[1] for post in posts.values()]) + 1

    window_x = min_value_x
    window_y = min_value_y

    window_size = 3 * maximal_length_of_side

    windows = []

    while window_y < max_value_y:

        window_x = min_value_x

        while window_x < max_value_x:

            points_in_window = []
            for post in posts.keys():
                if window_x < posts[post][0] < (window_x + window_size) and window_y < posts[post][1] < (window_y + window_size):
                    points_in_window.append(post)
            if len(points_in_window) > 0:
                windows.append(points_in_window)

            window_x += window_size / 2
        window_y += window_size / 2

    return windows


# https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
def ccw(A, B, C, posts):
    return (posts[C][1] - posts[A][1]) * (posts[B][0] - posts[A][0]) > (posts[B][1] - posts[A][1]) * (
                posts[C][0] - posts[A][0])


def intersect(A, B, C, D, posts):
    return ccw(A, C, D, posts) != ccw(B, C, D, posts) and ccw(A, B, C, posts) != ccw(A, B, D, posts)


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

    def printProgress(self, text, percent):
        if not self.started:
            self.startTimer()

        if (time.time() - self.last_progress_report) >= self.step:
            self.last_progress_report = time.time()
            print('\r{} {:3d}% - ({:3.3f}s)'.format(text, int(percent * 100), (time.time() - self.start_time)), end='',
                  flush=True)
        if self.break_on_end and percent >= 1:
            print('\r{} {:3d}% - ({:3.3f}s)'.format(text, int(percent * 100), (time.time() - self.start_time)),
                  end='\n', flush=True)
