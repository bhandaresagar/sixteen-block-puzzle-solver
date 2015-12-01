# !/usr/bin/python

__author__ = 'sagar'

'''
A brief report on the program:

Run Command: python solver16.py <input-board-filename.txt>
Input parameters: name of file having input 15 puzzle board configuration
Expected sample output:

if logging=DEBUG
current path being considered

if logging=INFO

Execution time : 0.08 minutes. explored nodes 8154 data:[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
L4 U3 R1 D3 R2 D2 L2 R3 U2 U4 L3 L2 D3 R2 D4 R1 U4 L1

Algorithm: A-Star
Heuristic Function: Variant of Manhattan considering shift of column and row
Total Cost : Cost of path from intial node to current node + Heuristic Cost from current node to goal node

Algo Solver16(input-borad-config-file)

    Board = load board from input-borad-config-file
    goalNotReached = TRUE
    frienge = priority queue based on total cost(path cost + heuristic cost)
    explored = set of expanded nodes

    iNode = create intial state from board

    if(iNode is GoalNode)
        return success
    add iNode to frienge
    while goalNotReached
        if(frienge empty)
            return error
        node = first node in frienge

        if(node is GoalNode)
            print moves
            return success

        children = All 16 children states of node

        for child in children
            if(child not in explored)
            put child in frienge

        add node to explored


Time Analysis:

Average Time required for configuration:
5 7 8 1
10 2 4 3
6 9 11 12
15 13 14 16

>> 15 seconds

Average Time required for configuration:
1 2 3 4
5 6 7 8
9 10 11 12
13 14 16 15

>> 5 seconds

'''

import sys, os
import logging
import time
from copy import deepcopy

# set debug level
logging.basicConfig(level=logging.INFO)

try:
    import queue
except ImportError:
    import Queue as queue


class Node:
    # represent state of board

    def __init__(self, data, moves):  # initialize a new node
        self.data = deepcopy(data)
        self.moves = deepcopy(moves)
        self.totalCost = 0
        self.heuristicCost = 0
        self.costSoFar = len(moves)
        self.updateTotalCost()

    def __lt__(self, other):  # for priority queue comparison
        return self.totalCost < other.totalCost

    def __eq__(self, other):
        return self.getUID() == other.getUID()

    def calcHeuristicCost(self):

        data = list(self.data)

        # manhattan heuristic
        manhattanDist = 0
        for i in range(0, 4):
            for j in range(0, 4):
                val = data[i][j]
                targetRow = (val - 1) / 4
                targetColumn = (val - 1) % 4
                if (targetColumn == j or targetRow == i) and (
                            (targetRow == 0 and i == 3 or targetRow == 3 and i == 0) or (
                                            targetColumn == 0 and j == 3 or targetColumn == 3 and j == 0)):  # specific to moves of problem
                    manhattanDist += 1
                else:
                    manhattanDist += abs(targetRow - i) + abs(targetColumn - j)

        self.heuristicCost = manhattanDist

    def updateTotalCost(self): # f(N) = g(N) + h(N)
        self.calcHeuristicCost()
        self.costSoFar = len(self.moves)
        self.totalCost = self.costSoFar + self.heuristicCost

    def rotateColumn(self, index, direction):
        if direction == 'U':
            # rotate column with number index up
            logging.debug('Rotating column no: ' + str(index) + ' UP')
            temp = []

            for i in range(0, 4):
                temp.append(self.data[i][index])

            first = temp.pop(0)
            temp.append(first)

            for i in range(0, 4):
                self.data[i][index] = temp[i]

            move = 'U' + str(index + 1)
            self.moves.append(move)
        else:
            # rotate column with number index down
            logging.debug('Rotating column no: ' + str(index) + ' DOWN')
            temp = []

            for i in range(0, 4):
                temp.append(self.data[i][index])

            last = temp.pop(3)
            temp.insert(0, last)

            for i in range(0, 4):
                self.data[i][index] = temp[i]

            move = 'D' + str(index + 1)
            self.moves.append(move)

    def rotateRow(self, index, direction):
        if direction == 'L':
            # rotate column with number index up
            logging.debug('Rotating row no: ' + str(index) + ' Left')
            temp = self.data[index]
            first = temp.pop(0)
            temp.append(first)
            move = 'L' + str(index + 1)
            self.moves.append(move)
        else:
            # rotate column with number index down
            logging.debug('Rotating row no: ' + str(index) + ' Right')
            temp = self.data[index]
            last = temp.pop(3)
            temp.insert(0, last)
            move = 'R' + str(index + 1)
            self.moves.append(move)

    def getUID(self): # unique state of node
        uid = ''
        for i in range(0, 4):
            for j in range(0, 4):
                uid += str(self.data[i][j])
        return uid

    def printData(self):
        logging.info(self.data)

    def isGoalNode(self): # check if goal is reached

        data = list(self.data)

        for i in range(0, 4):
            for j in range(0, 4):
                if int(data[i][j]) != int(i * 4 + j + 1):
                    return False;

        return True


class Solution:
    'Solves 16 block puzzle'

    def __init__(self):
        self.frienge = queue.PriorityQueue()  # frienge to hold nodes
        self.explored = {}                    # set of expanded nodes
        self.start = time.time()

    def printmoves(self, node):

        moves = node.moves;
        path = ''

        for move in moves:
            path += move + ' '

        end = time.time() - self.start
        print(
            "Execution time : " + str(round(end,2)) + ' seconds. Final state of data:' + str(
                node.data))
        print(path)

    def getChildNodes(self, node):  # returns all 16 possible combinations

        data = node.data[:]
        moves = node.moves[:]

        children = []

        for i in range(0, 4):
            # rotate all columns upside and downside
            childNode = Node(data, moves)
            childNode.rotateColumn(i, 'U')
            childNode.updateTotalCost()
            children.append(childNode)

            childNodeTwo = Node(data, moves)
            childNodeTwo.rotateColumn(i, 'D')
            childNodeTwo.updateTotalCost()
            children.append(childNodeTwo)

            # rotate all rows left and right
            childNodeThree = Node(data, moves)
            childNodeThree.rotateRow(i, 'L')
            childNodeThree.updateTotalCost()
            children.append(childNodeThree)

            childNodeFour = Node(data, moves)
            childNodeFour.rotateRow(i, 'R')
            childNodeFour.updateTotalCost()
            children.append(childNodeFour)

        return children

    def solve(self, iNode):

        if (iNode.isGoalNode()):
            self.printmoves(iNode)
            return

        # add to frienge
        self.frienge.put(iNode)

        goalFound = False

        while True:

            if self.frienge.empty():
                logging.error("Frienge empty")
                return

            node = self.frienge.get()

            if (node.isGoalNode()):
                self.printmoves(node)
                goalFound = True
                break
            else:
                # get all children of node
                children = self.getChildNodes(node)

                for child in children:
                    if (self.explored.get(child.getUID(), 'none') == 'none'): # check if node is already expanded
                        self.frienge.put(child)

                self.explored[node.getUID()] = "1"  # mark node as expanded


def main():
    solution = Solution()

    # 4x4 data matrix
    data = []

    # read matrix from the file
    with open(sys.argv[1], 'r') as file:
        for line in file:
            data.append([int(x) for x in line.split()]);

    logging.info('Creating initial node')
    iNode = Node(data, [])
    iNode.printData()

    solution.solve(iNode)


if __name__ == '__main__':
    main()
