# coding=utf-8

# Created by lruoran on 17-1-20

import math


def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1]))


def findClosestPair(pX, pY):
    '''
    :param pX: 按照x坐标将所有的节点排序
    :param pY: 按照y坐标将所有的节点排序
    :return:距离最小的节点对的距离
    '''
    num = len(pX)
    minDist = (1 << 31)
    if num <= 4:  # 节点数目不多于5个的时候用暴力方法求解
        for i in range(num):
            for j in range(i + 1, num):
                d = distance(pX[i], pX[j])
                if d < minDist:
                    minDist = d
        return minDist

    xm = (pX[0][0] + pX[-1][0])/2
    pXLeft, pXRight, pYLeft, pYRight = [], [], [], []
    # 小于xm的节点加入pXLeft, pYLeft；大于xm的节点加入pXRight，pYRight
    for p in pX:
        if p[0] <= xm:
            pXLeft.append(p)
        else:
            pXRight.append(p)
    for p in pY:
        if p[0] <= xm:
            pYLeft.append(p)
        else:
            pYRight.append(p)
    if len(pXLeft) == 0:   # 如果一侧没有点，说明x的值都相同
        return min([pYRight[i][1] - pYRight[i - 1][1] for i in range(1, len(pYRight))])
    if len(pXRight) == 0:
        return min([pYLeft[i][1] - pYLeft[i - 1][1] for i in range(1, len(pYLeft))])

    # 分别对左右区域的节点对最小距离进行计算
    leftMinDist = findClosestPair(pXLeft, pYLeft)
    rightMinDist = findClosestPair(pXRight, pYRight)
    minDist = leftMinDist
    if rightMinDist < minDist:
        minDist = rightMinDist

    # 得到条带区域的节点
    strips = []
    for py in pY:
        if math.fabs(py[0] - xm) < minDist:
            strips.append(py)
    # 计算条带区域内的节点对之间的距离
    len_ = len(strips)
    for i in range(len_):
        for j in range(i + 1, len_):
            if strips[j][1] - strips[i][1] >= minDist:  # 单方向大于minDist的距离不可能比minDist小
                break
            d = distance(strips[i], strips[j])
            if d < minDist:
                minDist = d
    return minDist

def findClosestPairStripNaive(pX, pY):
    '''
    :param pX: 按照x坐标将所有的节点排序
    :param pY: 按照y坐标将所有的节点排序
    :return:距离最小的节点对的距离
    '''
    num = len(pX)
    minDist = (1 << 31)
    if num <= 4:  # 节点数目不多于5个的时候用暴力方法求解
        for i in range(num):
            for j in range(i + 1, num):
                d = distance(pX[i], pX[j])
                if d < minDist:
                    minDist = d
        return minDist

    xm = (pX[0][0] + pX[-1][0])/2
    pXLeft, pXRight, pYLeft, pYRight = [], [], [], []
    # 小于xm的节点加入pXLeft, pYLeft；大于xm的节点加入pXRight，pYRight
    for p in pX:
        if p[0] <= xm:
            pXLeft.append(p)
        else:
            pXRight.append(p)
    for p in pY:
        if p[0] <= xm:
            pYLeft.append(p)
        else:
            pYRight.append(p)
    if len(pXLeft) == 0:   # 如果一侧没有点，说明x的值都相同
        return min([pYRight[i][1] - pYRight[i - 1][1] for i in range(1, len(pYRight))])
    if len(pXRight) == 0:
        return min([pYLeft[i][1] - pYLeft[i - 1][1] for i in range(1, len(pYLeft))])

    # 分别对左右区域的节点对最小距离进行计算
    leftMinDist = findClosestPair(pXLeft, pYLeft)
    rightMinDist = findClosestPair(pXRight, pYRight)
    minDist = leftMinDist
    if rightMinDist < minDist:
        minDist = rightMinDist

    # 得到条带区域的节点
    strips = []
    for py in pY:
        if math.fabs(py[0] - xm) < minDist:
            strips.append(py)
    # 计算条带区域内的节点对之间的距离
    tmp = naive(strips, strips)
    if tmp < minDist:
        minDist = tmp
    return minDist

def naive(pX, pY):	# 暴力求解
    len_ = len(pX)
    minDist = (1 << 31)
    for i in range(len_):
        for j in range(i + 1, len_):
            d = distance(pX[i], pX[j])
            if d < minDist:
                minDist = d
    return minDist

import time

if __name__ == '__main__':
    import random

    points = []
    for i in range(1000):
        points.append((random.randint(-100, 100), random.randint(-100, 100)))
    points = list(set(points))
    print '样本点个数：', len(points)

    # points = [(-91, -11), (-90, -75), (-89, 98), (-89, 82), (-89, -75)]

    start = time.clock()
    pX = sorted(points, key=lambda p: p[0])
    pY = sorted(points, key=lambda p: p[1])
    print findClosestPair(pX, pY)
    end = time.clock()
    print '分治法耗时(strip中y方向差大于theta则break)：', (end - start)

    start = time.clock()
    pX = sorted(points, key=lambda p: p[0])
    pY = sorted(points, key=lambda p: p[1])
    print findClosestPairStripNaive(pX, pY)
    end = time.clock()
    print '分治法耗时(strip中用暴力搜索)：', (end - start)

    start = time.clock()
    print naive(pX, pY)
    end = time.clock()
    print '普通方法耗时：', (end -  start)