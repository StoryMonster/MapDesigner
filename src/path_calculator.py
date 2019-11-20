from constances import EMPTY_NUMBER
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
        return self.G[int(row * self.maxCol + col)]

    def _is_pos_closeat(self, row1, col1, row2, col2):
        return (row1 == row2 and math.fabs(col1 - col2) <= 1) or (col1 == col2 and math.fabs(row1-row2) <= 1)

    def _is_pos_can_walk(self, row, col):
        return not (row < 0 or row >= self.maxRow or col < 0 or col >= self.maxCol or self._get_weight(row, col) == EMPTY_NUMBER or ((row, col) in self.tempPaths.nodes))

    def _calc_shortest_path(self, row1, col1, row2, col2):
        if self._is_pos_closeat(row1, col1, row2, col2):
            w = self._get_weight(row2, col2)
            self.tempPaths.add_node(row2, col2, w)
            if (self.shortestPath is None) or \
               (self.shortestPath is not None and self.tempPaths.distance < self.shortestPath.distance) or \
               (self.shortestPath is not None and len(self.tempPaths.nodes) < len(self.shortestPath.nodes)):
                self.shortestPath = deepcopy(self.tempPaths)
            self.tempPaths.del_last_node(w)
            return
        if self._is_pos_can_walk(row1-1, col1): # 上行
            w = self._get_weight(row1-1, col1)
            self.tempPaths.add_node(row1-1, col1, w)
            self._calc_shortest_path(row1-1, col1, row2, col2)
            self.tempPaths.del_last_node(w)
        if self._is_pos_can_walk(row1+1, col1): #下行
            w = self._get_weight(row1+1, col1)
            self.tempPaths.add_node(row1+1, col1, w)
            self._calc_shortest_path(row1+1, col1, row2, col2)
            self.tempPaths.del_last_node(w)
        if self._is_pos_can_walk(row1, col1-1): # 左行
            w = self._get_weight(row1, col1-1)
            self.tempPaths.add_node(row1, col1-1, w)
            self._calc_shortest_path(row1, col1-1, row2, col2)
            self.tempPaths.del_last_node(w)
        if self._is_pos_can_walk(row1, col1+1): # 右行
            w = self._get_weight(row1, col1+1)
            self.tempPaths.add_node(row1, col1+1, w)
            self._calc_shortest_path(row1, col1+1, row2, col2)
            self.tempPaths.del_last_node(w)
    
    def get_the_shortest_path(self, row1, col1, row2, col2):
        if row1 == row2 and col1 == col2:
            res = MapPath()
            res.add_node(row1, col1, 0)
            return res
        self.tempPaths.add_node(row1, col1, 0)
        self._calc_shortest_path(row1, col1, row2, col2)
        return self.shortestPath

