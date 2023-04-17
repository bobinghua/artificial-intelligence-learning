# 定义全局变量：地图中节点的像素大小
CELL_WIDTH = 16  # 单元格宽度
CELL_HEIGHT = 16  # 单元格长度
BORDER_WIDTH = 1  # 边框宽度
BLOCK_NUM = 50  # 地图中的障碍物数量


def _init():
    global _globalDict
    _globalDict = {}


def set_value(key, value):
    _globalDict[key] = value


def get_value(key, defValue=None):
    try:
        return _globalDict[key]
    except KeyError:
        return defValue
