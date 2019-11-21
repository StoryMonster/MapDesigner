# 数据编码方式：
# 0 bytes: 行数 r = byte[0]
# 1 bytes: 列数 c = byte[1]
# 2 ~ (r * c / 2) + 2 - 1 bytes: 每一格的值，用半个字节表示，按行存储
# (r * c / 2) + 2 ~ bytes: 图片

import math
from copy import deepcopy
from collections import namedtuple


MapData = namedtuple("MapData", ["row", "col", "gridWeights", "imgData"])

class DataParser:
    def parse_from_file(self, filepath):
        if filepath is None or len(filepath) == 0: return None
        data = []
        with open(filepath, "rb") as fd:
            data = fd.read()
        if len(data) == 0: return MapData(0, 0, [], [])
        try:
            row = data[0]
            col = data[1]
            gridWeights = [0 for _ in range(col * row)]
            sep = int(row * col / 2 + 1 if (row * col) % 2 == 0 else (row * col + 1) / 2 + 1)
            counter = 0
            for b in data[2:sep+1]:
                if counter < col * row:
                    gridWeights[counter] = (b & 0xf0) >> 4
                    counter += 1
                if counter < col * row:
                    gridWeights[counter] = b & 0x0f
                    counter += 1
            return MapData(row, col, deepcopy(gridWeights), deepcopy(data[sep+1:]))
        except Exception as e:
            print(str(e))
            return None

    def save_to_file(self, filepath, mapdata):
        data = bytearray()
        data.append(mapdata.row & 0xff)
        data.append(mapdata.col & 0xff)
        isHalf = False
        value = 0
        for val in mapdata.gridWeights:
            if isHalf:
                value = value | (val & 0xf)
                isHalf = False
                data.append(value)
            else:
                value = (val & 0xf) << 4
                isHalf = True
        data.extend(mapdata.imgData)
        with open(filepath, "wb") as fd:
            fd.write(data)

dataParser = DataParser()