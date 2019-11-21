from .constances import EMPTY_NUMBER
import math
from copy import deepcopy
import sys

sys.setrecursionlimit(5000000)

class MapPath:
    def __init__(self):
        self.distance = 0
        self.nodes = []
    
    def add_node(self, row, col, weight):
        self.distance += weight
        self.nodes.append((row, col))

    def del_last_node(self, weight):
        self.distance -= weight
        self.nodes.pop()

class PathCalculator:
    def __init__(self, G, maxRow, maxCol):
        self.G = G
        self.maxRow = maxRow
        self.maxCol = maxCol
        self.shortestPath = None
        self.tempPaths = MapPath()
    
    def _get_weight(self, row, col):
        offset = int(row * self.maxCol + col)
        if offset >= len(self.G): return EMPTY_NUMBER
        return self.G[offset]

    def _is_pos_closeat(self, row1, col1, row2, col2):
        return (row1 == row2 and math.fabs(col1 - col2) <= 1) or (col1 == col2 and math.fabs(row1-row2) <= 1)

    def _is_pos_can_walk(self, row, col):
        if row < 0 or row >= self.maxRow or col < 0 or col >= self.maxCol or \
           self._get_weight(row, col) == EMPTY_NUMBER or ((row, col) in self.tempPaths.nodes) or \
           (self.shortestPath is not None and self.tempPaths.distance >= self.shortestPath.distance):
           return False
        return True

    ## maybe best
    def _calc_maybe_shortest_path(self, row1, col1, row2, col2):
        if self._is_pos_closeat(row1, col1, row2, col2):
            w = self._get_weight(row2, col2)
            self.tempPaths.add_node(row2, col2, w)
            self.shortestPath = deepcopy(self.tempPaths)
            return True
        nextNodes = [[row1-1, col1, self._get_weight(row1-1, col1), 0],
                     [row1+1, col1, self._get_weight(row1+1, col1), 0],
                     [row1, col1-1, self._get_weight(row1, col1-1), 0],
                     [row1, col1+1, self._get_weight(row1, col1+1), 0]]
        yOffset = row2 - row1
        xOffset = col2 - col1
        if xOffset > 0: nextNodes[3][3] += 100
        if xOffset < 0: nextNodes[2][3] += 100
        if yOffset > 0: nextNodes[1][3] += 100
        if yOffset < 0: nextNodes[0][3] += 100
        for node in nextNodes:
            node[3] += (100 - node[2])
        nextNodes.sort(key=lambda a: a[3], reverse=True)

        for node in nextNodes:
            if self._is_pos_can_walk(node[0], node[1]):
                self.tempPaths.add_node(node[0], node[1], node[2])
                if self._calc_maybe_shortest_path(node[0], node[1], row2, col2): return True
                self.tempPaths.del_last_node(node[2])
        return False

    ## global best
    def _calc_shortest_path(self, row1, col1, row2, col2):
        if self._is_pos_closeat(row1, col1, row2, col2):
            w = self._get_weight(row2, col2)
            self.tempPaths.add_node(row2, col2, w)
            if (self.shortestPath is None) or \
               (self.shortestPath is not None and self.tempPaths.distance < self.shortestPath.distance):
                self.shortestPath = deepcopy(self.tempPaths)
            self.tempPaths.del_last_node(w)
            return
        nextNodes = [(row1-1, col1), (row1+1, col1), (row1, col1-1), (row1, col1+1)]
        for node in nextNodes:
            if self._is_pos_can_walk(node[0], node[1]):
                w = self._get_weight(node[0], node[1])
                self.tempPaths.add_node(node[0], node[1], w)
                self._calc_shortest_path(node[0], node[1], row2, col2)
                self.tempPaths.del_last_node(w)
    
    def get_maybe_shortest_path(self, row1, col1, row2, col2):
        if row1 == row2 and col1 == col2:
            res = MapPath()
            res.add_node(row1, col1, 0)
            return res
        if self._get_weight(row2, col2) == EMPTY_NUMBER: return None
        self.tempPaths.add_node(row1, col1, 0)
        self._calc_maybe_shortest_path(row1, col1, row2, col2)
        return self.shortestPath

    def get_the_shortest_path(self, row1, col1, row2, col2):
        if row1 == row2 and col1 == col2:
            res = MapPath()
            res.add_node(row1, col1, 0)
            return res
        if self._get_weight(row2, col2) == EMPTY_NUMBER: return None
        self.tempPaths.add_node(row1, col1, 0)
        self._calc_shortest_path(row1, col1, row2, col2)
        return self.shortestPath
