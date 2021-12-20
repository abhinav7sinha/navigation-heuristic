#!/usr/local/bin/python3
#
# arrange_pichus.py : arrange agents on a grid, avoiding conflicts
#
# Submitted by : Abhinav Sinha (sinhabhi)
#
# Based on skeleton code in CSCI B551, Fall 2021.

import sys
import re

# Parse the map from a given filename


def parse_map(filename):
    with open(filename, "r") as f:
        return [[char for char in line] for
                line in f.read().rstrip("\n").split("\n")][3:]

# Count total # of pichus on house_map


def count_pichus(house_map):
    return sum([row.count('p') for row in house_map])

# Return a string with the house_map rendered in a human-pichuly format


def printable_house_map(house_map):
    return "\n".join(["".join(row) for row in house_map])

# Add a pichu to the house_map at the given position, and return a
# new house_map (doesn't change original)


def add_pichu(house_map, row, col):
    return house_map[0:row] +\
        [house_map[row][0:col] +
         ['p', ] + house_map[row][col+1:]] + house_map[row+1:]

# Check row to see if there are any pichus can see new pichu
# If the space between a pichu and new pichu is empty or only contains '.',
# we discard the new location


def check_row(house_map, loc):
    new_house_map = add_pichu(house_map, loc[0], loc[1])
    pichu_count = 0
    for c in range(0, len(new_house_map[0])):
        if 'p' in new_house_map[loc[0]][c]:
            pichu_count += 1
    if pichu_count > 1:
        row_str = ''.join(map(str, new_house_map[loc[0]]))
        check_space = re.findall(r'(?=p(.*?)p)', row_str)
        # Create a list of strings representing various possible empty spaces:
        # '', '.', '..', '...', '....' etc.
        maplist = \
            ['.' * n for n in range(0, len(new_house_map[loc[0]]))]
        return not any(item in maplist for item in check_space)
    else:
        return True

# Check column to see if there are any pichus can see new pichu
# If the space between a pichu and new pichu is empty or only contains '.',
# we discard the new location


def check_column(house_map, loc):
    house_map_old = add_pichu(house_map, loc[0], loc[1])
    new_house_map = list(map(list, zip(*house_map_old)))
    pichu_count = 0
    for r in range(0, len(new_house_map[0])):
        if 'p' in new_house_map[loc[1]][r]:
            pichu_count += 1
    if pichu_count > 1:
        col_str = ''.join(map(str, new_house_map[loc[1]]))
        check_space = re.findall(r'(?=p(.*?)p)', col_str)
        maplist = \
            ['.' * n for n in range(0, len(new_house_map[loc[0]]))]
        return not any(item in maplist for item in check_space)
    else:
        return True

# Check diagonal to see if there are any pichus can see new pichu
# If the space between a pichu and new pichu is empty or only contains '.',
# we discard the new location
# I build rows corresponding to each diagonal of the map and check all the rows
# to make sure no pichus can see each other on the diagonals
#  [ a b c ] => [ a b c X X X ]        [ a b c ] => [ X X X a b c ]
#  [ d e f ] => [ X d e f X X ]        [ d e f ] => [ X X d e f X ]
#  [ g h i ] => [ X X g h i X ]        [ g h i ] => [ X X X g h i ]
#                 ^ ^ ^ ^ ^ ^                         ^ ^ ^ ^ ^ ^
# The columns of the new matrix are the diagonals. I put them in a new matrix
# as follows:
#  [ a X X ]
#  [ b d X ]
#  [ c e g ]
#    . . .
#    . . .
#  [ c X i ]


def check_diagonal(house_map, loc):
    new_house_map = add_pichu(house_map, loc[0], loc[1])
    rnum = len(new_house_map)
    cnum = len(new_house_map[0])
    cnum_new = rnum+cnum-1
    diag_map1 = [['X']*cnum_new for i in range(rnum)]
    diag_map2 = [['X']*cnum_new for i in range(rnum)]
    for r in range(0, rnum):
        for c in range(0, cnum_new):
            if r > c-cnum and r <= c:
                diag_map1[r][c] = new_house_map[r][c-r]
            if r < cnum_new-c and r+c >= rnum-1:
                diag_map2[r][c] = new_house_map[r][c-rnum+r+1]
    diagonal_map = \
        list(map(list, zip(*diag_map1)))+list(map(list, zip(*diag_map2)))
    pichu_count = 0
    for k in range(0, len(diagonal_map)):
        for c in range(0, len(diagonal_map[0])):
            if 'p' in diagonal_map[k][c]:
                pichu_count += 1
        if pichu_count > 1:
            row_str = ''.join(map(str, diagonal_map[k]))
            check_space = re.findall(r'(?=p(.*?)p)', row_str)
            maplist = ['.' * n for n in range(0, len(diagonal_map[k])-1)]
            if any(item in maplist for item in check_space):
                return False
    return True

# Get list of successors of given house_map state


def successors(house_map):
    maplist = []
    for r in (range(len(house_map))):
        for c in range(len(house_map[0])):
            if house_map[r][c] == '.' and check_row(house_map, (r, c)) and\
                    check_column(house_map, (r, c)) and\
                    check_diagonal(house_map, (r, c)):
                maplist.append(add_pichu(house_map, r, c))
    return maplist

# check if house_map is a goal state


def is_goal(house_map, k):
    return count_pichus(house_map) == k


# Arrange agents on the map
#
# This function MUST take two parameters as input -- the house map and
# the value k --
# and return a tuple of the form (new_house_map, success), where:
# - new_house_map is a new version of the map with k agents,
# - success is True if a solution was found, and False otherwise.
#


def solve(initial_house_map, k):
    fringe = [initial_house_map]
    while len(fringe) > 0:
        for new_house_map in successors(fringe.pop()):
            if is_goal(new_house_map, k):
                return(new_house_map, True)
            fringe.append(new_house_map)
    return([], False)


# Main Function
if __name__ == "__main__":
    house_map = parse_map(sys.argv[1])
    # This is k, the number of agents
    k = int(sys.argv[2])
    print("Starting from initial house map:\n" +
          printable_house_map(house_map) + "\n\nLooking for solution...\n")
    solution = solve(house_map, k)
    print("Here's what we found:")
    print(printable_house_map(solution[0]) if solution[1] else "False")
