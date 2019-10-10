import math

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