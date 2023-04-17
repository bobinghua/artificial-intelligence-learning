import globalVar
import pygame
import matplotlib.pyplot as plt
import skimage
from aboutMap import Color, Map
import os

CELL_WIDTH = globalVar.CELL_WIDTH
CELL_HEIGHT = globalVar.CELL_HEIGHT
BORDER_WIDTH = globalVar.BORDER_WIDTH


def transform(pos):
    xnew, ynew = pos[0] * CELL_WIDTH, pos[1] * CELL_HEIGHT
    return (xnew, ynew)


def saveResultImg(mapsize, pos_sn, pos_en, blocklist, routelists, idx=0):
    # 初始化导入的Pygame模块
    pygame.init()
    # 此处要将地图投影大小转换为像素大小，此处设地图中每个单元格的大小为CELL_WIDTH*CELL_HEIGHT像素
    mymap = Map((mapsize[0] * CELL_WIDTH, mapsize[1] * CELL_HEIGHT))
    pix_sn = (pos_sn[0] * CELL_WIDTH, pos_sn[1] * CELL_HEIGHT)
    pix_en = (pos_en[0] * CELL_WIDTH, pos_en[1] * CELL_HEIGHT)

    # 对blocklist和routelist中的坐标同样要转换为像素值
    bl_pix = list(map(transform, blocklist))

    # 初始化显示的窗口并设置尺寸
    screen = pygame.display.set_mode(mymap.mapsize)
    # 设置窗口标题
    pygame.display.set_caption('A*算法路径搜索演示：')
    # 用白色填充屏幕
    screen.fill(Color.WHITE.value)  # 为什么用参数Color.WHITE不行？

    # 绘制屏幕中的所有单元格
    for (x, y) in mymap.generate_cell(CELL_WIDTH, CELL_HEIGHT):
        if (x, y) in bl_pix:
            # 绘制黑色的障碍物单元格，并留出2个像素的边框
            pygame.draw.rect(screen, Color.BLACK.value, (
                (x + BORDER_WIDTH, y + BORDER_WIDTH), (CELL_WIDTH - 2 * BORDER_WIDTH, CELL_HEIGHT - 2 * BORDER_WIDTH)))
        else:
            # 绘制绿色的可通行单元格，并留出2个像素的边框
            pygame.draw.rect(screen, Color.GREEN.value, (
                (x + BORDER_WIDTH, y + BORDER_WIDTH), (CELL_WIDTH - 2 * BORDER_WIDTH, CELL_HEIGHT - 2 * BORDER_WIDTH)))
    # 绘制起点和终点
    pygame.draw.circle(screen, Color.BLUE.value, (pix_sn[0] + CELL_WIDTH // 2, pix_sn[1] + CELL_HEIGHT // 2),
                       CELL_WIDTH // 2 - 1)
    pygame.draw.circle(screen, Color.RED.value, (pix_en[0] + CELL_WIDTH // 2, pix_en[1] + CELL_HEIGHT // 2),
                       CELL_WIDTH // 2 - 1)

    # 绘制搜索得到的最优路径
    for c, routelist in routelists:
        rl_pix = list(map(transform, routelist))
        pygame.draw.aalines(screen, c, False, rl_pix, 5)

    pygame.image.save(screen, "result" + str(idx) + ".png")
    pygame.quit()
