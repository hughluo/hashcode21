import sys
from collections import defaultdict
import time


def read_input(filename):
    D, I, S, V, F = 0, 0, 0, 0, 0

    intersection_to_streets_map = defaultdict(set) # k: intersection, v: set of street
    street_to_traffic_map = defaultdict(int) # k: street, v: amount of cars that have this street in his route

    with open(filename, "r") as f:
        first_line = f.readline().strip()
        D, I, S, V, F = first_line.split(" ")

        for _ in range(int(S)):
            line = f.readline().strip()
            B, E, S_name, L = line.split(" ")
            intersection_to_streets_map[E].add(S_name)

        for _ in range(int(V)):
            line = f.readline().strip()
            P = line[0]
            V_streets = line[1:].strip().split(" ")
            for street in V_streets:
                street_to_traffic_map[street] += 1

    return int(D), int(I), int(S), int(V), int(F), intersection_to_streets_map, street_to_traffic_map



def output_weighted_street_traffic(f, street_to_traffic_map , intersection_to_streets_map):
    with open(f + ".output", "w") as f:
        total_intersections = len(intersection_to_streets_map)
        f.write(str(total_intersections) + "\n")
        for i in intersection_to_streets_map:
            f.write(str(i)+"\n")
            total_streets = len(intersection_to_streets_map[i])
            f.write(str(total_streets)+"\n")

            for steet in intersection_to_streets_map[i]:
                green_sec_base = 0.3
                green_sec = street_to_traffic_map[steet] * green_sec_base
                green_sec = max(1, int(green_sec))
                f.writelines("{} {}\n".format(steet, green_sec))

# drop intersections if it has street amount less than `threshhold`
def drop_intersections(intersection_to_streets_map, threshhold):
    return {k: v for k, v in intersection_to_streets_map.items() if len(v) >= threshhold}

# drop streets if it has car traffic less than `threshhold`.
def drop_streets(intersection_to_streets_map, street_to_traffic_map, threshhold):
    available_streets = set()
    for k, v in intersection_to_streets_map.items():
        for s in v:
            available_streets.add(s)

    new_street_to_traffic_map = {k: v for k, v in street_to_traffic_map.items() if k in available_streets and street_to_traffic_map[k] >= threshhold}

    new_intersection_to_streets_map = {}

    # update the `intersection_to_streets_map` to delete the dropped street.
    for k, v in intersection_to_streets_map.items():
        new_streets = {s for s in v if s in new_street_to_traffic_map}
        if len(new_streets) == 0: 
            continue
        new_intersection_to_streets_map[k] = new_streets
    return new_intersection_to_streets_map, new_street_to_traffic_map

if __name__ == "__main__":
    for f in ['a', 'b', 'c', 'd', 'e', 'f']:
        D, I, S, V, F, intersection_to_streets_map, street_to_traffic_map = read_input('input/' + f + '.txt')
        intersection_to_streets_map_with_drop = drop_intersections(intersection_to_streets_map, 1)
        new_intersection_to_streets_map, new_street_to_traffic_map = drop_streets(intersection_to_streets_map_with_drop, street_to_traffic_map, 1)
        output_weighted_street_traffic(f, new_street_to_traffic_map, new_intersection_to_streets_map)
