# a0
> B551 Assignment 0: Searching and Python by Abhinav Sinha (sinhabhi)

## Part 1: Navigation
## Program 1
- This program is designed to find an optimum path between Pichu and the observer.
- Set of valid states: It contains all the coordinates where Pichu can travel. According to the problem it is the location of all the '.'
- Successor function: It returns all the states that Pichu can go to from it's current location. Here, it can go either one row up, or one row down, or one column right or one column left. Additionally it can only go to a location which is empty i.e '.'. There are walls in the map 'X', where Pichu cannot go.
- Cost function: It is uniform for all valid moves.
- Goal state definition: It is defined as the state where Pichu and observer meet. Here, the goal state is when 'p' reaches '@'
- Initial state: The initial state is given in the files map1.txt and map2.txt. In both these maps 'p' is placed at an arbitrary distance from '@'. There are '.' and 'X' surrounding them.
- The existing program uses Depth First Search to find the optimum path between the observer and Pichu. This is characterized by the Stack implementation of fringe. The last node to go to the fringe is the first one to come out.
- Why does the program often fail tofind a solution? The program goes inside an infinite loop and gets stuck there. It adds and then removes the same set of nodes from the fringe repeatedly.

## Solution 1
- The solution to the problem is A* search. By defining a consistent heuristic - Manhattan distance, and using Search Algorithm #3, I have overcome the problem of the program going into infinite loops. The solution to the problem is optimal.
- The fringe is implemented as a stack. We use append function to append new node to it and pop function to remove a node.
- The fringe has 4 parameters: 1. Current position of Pichu, 2. Distance travelled by Pichu, 3. Path covered by Pichu to reach current position, 4.Heuristic function of current position
- A dictionary 'visited' is used to store all the visited nodes and the distance travelled to reach it.

## Part 2: Hide-and-seek
## Program 2
- This program is designed to arrange the given number of pichus in a map so that they cannot see each other. Unlike the first program where pichus could only travel vertically and horizontally, in this program the pichus can see vertically, horizontally AND DIAGONALLY.
- The existing program uses the Depth First Search algorithm to place pichus in the desired locations. But it fails to do so, because it doesn't clearly define the goal state, or the successor function to include conditions where pichus can see each other.

## Solution 2
- To fix the program, I defined the goal state to have all the pichus placed such that no two pichus were in the same row, column or diagonal.
- To make the porgram faster, instead of defining the checks in the goal state, I added the checks in the Successor function itself.
- In the Successor function, I only return new states, where the new pichu cannot see another pichu in the same row, column or diagonal.
- I've used Depth First Search technique to find the goal state in this program.
- State Space: It contains all the maps containing 1 to k number of pichus in the given MXN grid.
- Initial State: It is a map containing just one Pichu at a given location in the grid.
- Goal state: The goal state is the map containing the given 'k' number of 'p' such that no two 'p' in the same row, column or diagonal have ONLY empty spaces ('.') between them.
- Successor function: It takes a map as an input and returns a list containing all the maps with a new pichu such that no two pichus in the same row, column or diagonal have ONLY empty spaces ('.') between them.
- Cost function: Cost function is irrelevant. It is uniform.
