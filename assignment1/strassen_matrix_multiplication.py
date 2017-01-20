# coding=utf-8

# Created by lruoran on 17-1-20

import numpy as np
import time


def strassen(A, B):
    '''
    :param A: numpy.array
    :param B: numpy.array
    :return: numpy.array
    '''
    if A.shape != B.shape:
        raise TypeError
    row, col = A.shape
    if row != col:
        raise TypeError

    C = np.zeros(shape=(row, col), dtype=float)
    if row <= 10:    # 小于4时按普通矩阵乘法处理
        for i in range(row):
            for j in range(col):
                C[i][j] = np.sum(A[i][k] * B[k][j] for k in range(row))
        return C

    flag = False
    if row % 2:  # 奇数，则增加一行一列
        C = np.zeros(shape=(row + 1, col + 1), dtype=float)
        _ = C[-1, :col]
        A = np.row_stack((A, _))
        B = np.row_stack((B, _))
        _ = C[:, -1]
        A = np.column_stack((A, _))
        B = np.column_stack((B, _))
        flag = True
        row, col = row + 1, col + 1
    else:
        C = np.zeros(shape=(row, col), dtype=float)

    mid = row / 2
    s = time.clock()
    A11, A12, A21, A22 = A[:mid, :mid], A[:mid, mid:], A[mid:, :mid], A[mid:, mid:]
    B11, B12, B21, B22 = B[:mid, :mid], B[:mid, mid:], B[mid:, :mid], B[mid:, mid:]
    e = time.clock()
    print 'stage1:', e - s

    s = time.clock()
    m1 = strassen(A11 + A22, B11 + B22)
    m2 = strassen(A21 + A22, B11)
    m3 = strassen(A11, B12 - B22)
    m4 = strassen(A22, B21 - B11)
    m5 = strassen(A11 + A12, B22)
    m6 = strassen(A21 - A11, B11 + B12)
    m7 = strassen(A12 - A22, B21 + B22)
    e = time.clock()
    print 'stage2:', e - s

    s = time.clock()
    C[:mid, :mid] = m1 + m4 - m5 + m7  # C11
    C[:mid, mid:] = m3 + m5  # C12
    C[mid:, :mid] = m2 + m4  # C21
    C[mid:, mid:] = m1 - m2 + m3 + m6  # C22
    e = time.clock()
    print 'stage3:', e - s

    if flag:
        C = C[:row - 1, :col - 1]
    return C

def naiveMultiply(A, B):
    '''
    :param A: numpy.array
    :param B: numpy.array
    :return: numpy.array,result
    '''
    C = np.zeros(A.shape, dtype=float)
    for i in range(C.shape[0]):
        for j in range(C.shape[1]):
            C[i][j] = np.sum([A[i][k] * B[k][j] for k in range(C.shape[0])])
    return C

if __name__ == '__main__':
    size = 100

    print 'shape:%d * %d'% (size, size)
    A = np.reshape(np.array(range(1, size * size + 1), dtype=float), (size, size))
    B = A = np.reshape(np.array(range(1, size * size + 1), dtype=float), (size, size))

    start = time.clock()
    C1 = strassen(A, B)
    end = time.clock()
    print 'strassen time:', (end - start)

    start = time.clock()
    C2 = naiveMultiply(A, B)
    end = time.clock()
    print 'naive time:', (end - start)
    print (C1 == C2).all()