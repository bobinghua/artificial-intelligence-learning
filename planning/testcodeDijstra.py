import math
from random import randint

import numpy as np
import pygame
from enum import Enum
import skimage
from skimage import io
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号 #有中文出现的情况，需要u'内容'

from planning.DijstraAlgorithm import Dijstra
from planning.AstarAlgorithm import AStar
from planning.aboutMap import gen_blocks, Color
from planning.aboutResults import saveResultImg


def runPathPlanning(algorithm_class, mapsize, pos_snode, pos_enode, blocklist):
    myAstar = algorithm_class(mapsize, pos_snode, pos_enode)
    myAstar.setBlock(blocklist)

    if myAstar.run() == 1:
        return myAstar.get_minroute()
    else:
        return -1


def runPathPlanningBasedDijstra(mapsize, pos_snode, pos_enode, blocklist):
    return runPathPlanning(Dijstra, mapsize, pos_snode, pos_enode, blocklist)


def runPathPlanningBasedAstar(mapsize, pos_snode, pos_enode, blocklist):
    return runPathPlanning(AStar, mapsize, pos_snode, pos_enode, blocklist)


def main():
    mapsize = tuple(map(int, (20, 20)))
    pos_snode = tuple(map(int, (0, 0)))
    pos_enode = tuple(map(int, (12, 19)))

    testNum = 1
    testNumList = []
    resultRoutes = []
    blocklists = []
    score = 0
    for testIdx in range(testNum):
        blocklist = gen_blocks(mapsize[0], mapsize[1])

        result = runPathPlanningBasedDijstra(mapsize, pos_snode, pos_enode, blocklist)

        if isinstance(result, list):
            resultRoutes.append(result)
            blocklists.append(blocklist)
            testNumList.append(testIdx + 1)
            score += 1
        else:
            score += -1

    successNum = len(resultRoutes)
    print('在' + str(testNum) + '次测试中，共有' + str(successNum) + '次成功规划出路径，其中：\n')
    for idx in range(successNum):
        blocklist = blocklists[idx]
        routelist = resultRoutes[idx]
        saveResultImg(mapsize, pos_snode, pos_enode, blocklist, routelist, testNumList[idx])

        print('第' + str(testNumList[idx]) + '次测试找到的路径为：')
        print(routelist)

        plt.figure(figsize=(5, 5))
        img = skimage.io.imread('result' + str(testNumList[idx]) + '.png')
        plt.imshow(img)
        plt.axis('off')
        plt.show()

    print('-------------------------\n')
    print('本次报告成果成绩得分为：' + str(score))


def compareDijstraAndAstar():
    '''
    为了证明两种算法的路径不同，这里使用同一张地图分别使用两种算法规划路径
    然后把两种算法的路径分别绘制在地图上进行展示
    '''
    mapsize = tuple(map(int, (20, 20)))
    pos_snode = tuple(map(int, (0, 0)))
    # 随机生成目标点
    pos_enode_x = randint(int((mapsize[0] - 1) / 2), mapsize[0] - 1)
    pos_enode_y = randint(int((mapsize[1] - 1) / 2), mapsize[1] - 1)
    pos_enode = tuple(map(int, (pos_enode_x, pos_enode_y)))

    # 生成障碍
    blocklist = gen_blocks(mapsize[0], mapsize[1], [pos_enode_x, pos_enode_y])

    # 分别使用两种算法计算路径
    dijstraResult = runPathPlanningBasedDijstra(mapsize, pos_snode, pos_enode, blocklist)
    if not isinstance(dijstraResult, list):
        print('路径规划失败！请重新规划!')
        exit(0)
    print('Dijstra算法找到的路径为：')
    print(dijstraResult)
    astarResult = runPathPlanningBasedAstar(mapsize, pos_snode, pos_enode, blocklist)
    print('A*算法找到的路径为：')
    print(astarResult)

    # 随机生成路径颜色
    DijstraColor = Color.random_color()
    AStarColor = (255 - DijstraColor[0], 255 - DijstraColor[1], 255 - DijstraColor[2])  # 高对比度颜色
    routelists = [(DijstraColor, dijstraResult), (AStarColor, astarResult)]

    saveResultImg(mapsize, pos_snode, pos_enode, blocklist, routelists, 1)

    plt.figure(figsize=(5, 5))
    img = skimage.io.imread('result' + str(1) + '.png')

    # 任意位置一个图像，目的是为了使用plt绘制出图例
    x = np.arange(0, 2.1, 0.1)
    y1 = np.power(x, 3)
    y2 = np.power(x, 2)

    Dijstra_hex_color = "#{:02x}{:02x}{:02x}".format(DijstraColor[0], DijstraColor[1], DijstraColor[2])
    AStar_hex_color = "#{:02x}{:02x}{:02x}".format(AStarColor[0], AStarColor[1], AStarColor[2])

    Dijstra_line, = plt.plot(x, y1, color=Dijstra_hex_color, ls='-')
    AStar_line, = plt.plot(x, y2, color=AStar_hex_color, ls='-')

    num1 = 0.3
    num2 = -0.06
    num3 = 3
    num4 = 0
    plt.legend([Dijstra_line, AStar_line], labels=['Dijstra', 'A*'], ncol=2, bbox_to_anchor=(num1, num2), loc=num3,
               borderaxespad=num4)

    plt.imshow(img)
    plt.title('Dijstra算法和A*算法规划路径对比')
    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    # main()
    compareDijstraAndAstar()
