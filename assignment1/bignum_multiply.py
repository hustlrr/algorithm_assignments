# coding=utf-8

# Created by lruoran on 17-1-20

def bignumSum(x, y):
    '''
    :param x: str
    :param y: str
    :return: str，大数加法，假设x和y都是正数
    '''
    lenx, leny = len(x), len(y)
    res, carry = '', 0
    x, y = x[::-1], y[::-1]
    for i in range(max(lenx, leny)):
        tmp = carry
        if i < lenx:
            tmp += int(x[i])
        if i < leny:
            tmp += int(y[i])
        res += str((tmp % 10))
        carry = tmp / 10
    if carry:
        res += str(carry)
    return res[::-1]


def bignumSub(x, y):
    '''
    :param x: str
    :param y: str
    :return: str，大数减法
    '''
    flag = False  # x>=y时为False
    lenx, leny = len(x), len(y)

    if lenx < leny or (lenx == leny and x < y):
        flag = True
        x, y = y, x

    res, carry = '', 0
    x, y = x[::-1], y[::-1]

    for i in range(max(lenx, leny)):
        tmp = carry
        if i < leny:
            if int(x[i]) + tmp < int(y[i]):
                res += str(10 + int(x[i]) + tmp - int(y[i]))
                carry = -1
            else:
                res += str(int(x[i]) + tmp - int(y[i]))
                carry = 0
        else:
            if int(x[i]) + tmp < 0:
                res += str(10 + int(x[i]) + tmp)
                carry = -1
            else:
                res += str(int(x[i]) + tmp)
                carry = 0
    zeroidx = 0
    res = res[::-1]
    for idx, digit in enumerate(res):
        if digit != '0':
            zeroidx = idx
            break
    res = res[zeroidx:]
    return '-' + res if flag else res


def onedigitMultiply(x, n):
    '''
    :param x: str
    :param n: str,一位乘数
    :return: str，积
    '''
    x = x[::-1]
    res, carry = '', 0
    for digit in x:
        tmp = int(digit) * int(n) + carry
        carry = tmp / 10
        res += str(tmp % 10)
    if carry:
        res += str(carry)
    return res[::-1]


def bignumMultiplyNaive(x, y):
    '''
    :param x: str
    :param y: str
    :return: str，大数乘法（普通版本）
    '''
    res = '0'
    y = y[::-1]
    for idx, n in enumerate(y):
        tmp = onedigitMultiply(x, n) + '0' * idx
        res = bignumSum(res, tmp)
    return res


def bignumMultiplyQuick(x, y):
    '''
    :param x: str
    :param y: str
    :return: str，大数乘法(Karatsuba algorithm)
    '''
    lenx, leny = len(x), len(y)
    if lenx <= 2 and leny <= 2:
        return str(int(x) * int(y))

    mid = max(lenx, leny) / 2
    xl, xr, yl, yr = '0', '0', '0', '0'
    if mid < lenx:
        xl, xr = x[:lenx - mid], x[lenx - mid:]
    else:
        xr = x
    if mid < leny:
        yl, yr = y[:leny - mid], y[leny - mid:]
    else:
        yr = y

    xlyl = bignumMultiplyQuick(xl, yl)
    xryr = bignumMultiplyQuick(xr, yr)
    p = bignumMultiplyQuick(bignumSum(xl, xr), bignumSum(yl, yr))
    p = bignumSub(p, xlyl)
    p = bignumSub(p, xryr)

    xlyl = xlyl + '0' * (mid * 2)
    p = p + '0' * mid

    res = bignumSum(xlyl, p)
    res = bignumSum(res, xryr)
    return res


import time
import random

if __name__ == '__main__':
    x, y = random.randint(1, 10000), random.randint(1, 10000)
    x, y = str(x), str(y)
    print 'x = ', x, ' y = ', y

    start = time.clock()
    print bignumMultiplyQuick(x, y)
    end = time.clock()
    print '改进的乘法运行时间：', (end - start)

    start = time.clock()
    print bignumMultiplyNaive(x, y)
    end = time.clock()
    print '原始的乘法运算运行时间：', (end - start)