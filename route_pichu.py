#!/usr/local/bin/python3
#
# route_pichu.py : a maze solver
#
# Submitted by : Abhinav Sinha (sinhabhi)
#
# Based on skeleton code provided in CSCI B551, Fall 2021.

import sys

# Parse the map from a given filename


def parse_map(filename):
    with open(filename, "r") as f:
        return [[char for char in line] for
                line in f.read().rstrip("\n").split("\n")][3:]

# Check if a row,col index pair is on the map


def valid_index(pos, n, m):
    return 0 <= pos[0] < n and 0 <= pos[1] < m

# Find the possible moves from position (row, col)


def moves(map, row, col):
    moves = ((row+1, col), (row-1, col), (row, col-1), (row, col+1))

    # Return only moves that are within the house_map and legal
    # (i.e. go through open space ".")
    return [move for move in moves if valid_index(
        move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@")]

# Add direction of new node to path string


def update_path(curr_path, move, curr_move):
    if move[0]-curr_move[0] == 1:
        return curr_path+'D'
    elif move[0]-curr_move[0] == -1:
        return curr_path+'U'
    elif move[1]-curr_move[1] == 1:
        return curr_path+'R'
    elif move[1]-curr_move[1] == -1:
        return curr_path+'L'

# get heuristic function at a node - Manhattan distance from current to goal


def heuristic(initial_loc, goal_loc):
    manhattan_dist = abs(initial_loc[0]-goal_loc[0])+abs(
        initial_loc[1]-goal_loc[1])
    return manhattan_dist

# Perform search on the map
#
# This function MUST take a single parameter as input -- the house map --
# and return a tuple of the form (move_count, move_string), where:
# - move_count is the number of moves required to navigate from start to
# finish, or -1 if no such route exists
# - move_string is a string indicating the path, consisting of U, L, R,
# and D characters (for up, left, right, and down)


def search(house_map):
    # Find pichu start position
    pichu_loc = [(row_i, col_i) for col_i in range(len(house_map[0]))
                 for row_i in range(len(house_map)) if house_map[row_i][
                 col_i] == "p"][0]
    # Determine goal position
    goal_loc = [(row_i, col_i) for col_i in range(len(house_map[0]))
                for row_i in range(len(house_map)) if house_map[row_i][
                col_i] == "@"][0]
    path = ''
    # Initialize fringe - It has 4 parameters:
    # 1. Current position of Pichu
    # 2. Distance of travelled by Pichi
    # 3. Path covered by Pichu to reach current position
    # 4. Heuristic function of current position
    fringe = [(pichu_loc, 0, path, heuristic(pichu_loc, goal_loc))]
    # visited dictionary to store all visited points and the distance travelled
    # to reach it
    visited = {}
    while fringe:
        fringe.sort(reverse=True)
        (curr_move, curr_dist, curr_path, heur) = fringe.pop()
        if curr_move not in visited.keys():
            for move in moves(house_map, *curr_move):
                if house_map[move[0]][move[1]] == "@":
                    return (
                        curr_dist+1, update_path(curr_path, move, curr_move))
                else:
                    fringe.append((move, curr_dist + 1,
                                   update_path(curr_path, move, curr_move),
                                   heuristic(move, goal_loc)))
        else:
            continue
        visited.update({curr_move: curr_dist})
    curr_dist = -1
    return (curr_dist, '')


# Main Function
if __name__ == "__main__":
    house_map = parse_map(sys.argv[1])
    print("Shhhh... quiet while I navigate!")
    solution = search(house_map)
    print("Here's the solution I found:")
    print(str(solution[0]) + " " + solution[1])
