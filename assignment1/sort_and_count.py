# coding=utf-8

# Created by lruoran on 17-1-20

def sortAndCount(A, left, right):
    '''
    :param A: 数组A
    :return: 查找数组A中的逆序对个数
    '''
    if left >= right:
        return 0
    mid = left + (right - left) / 2
    res = 0
    res += sortAndCount(A, left, mid)
    res += sortAndCount(A, mid + 1, right)
    partLeft = A[left:mid + 1]
    partRight = A[mid + 1: right + 1]
    pl, pr, lenLeft, lenRight = 0, 0, len(partLeft), len(partRight)
    for k in range(left, right + 1):
        if pl <= mid - left and pr <= right - mid - 1:
            if partLeft[pl] < partRight[pr]:
                A[k] = partLeft[pl]
                pl += 1
            else:
                A[k] = partRight[pr]
                res += (lenLeft - pl)
                pr += 1
        elif pl <= mid - left:
            A[k] = partLeft[pl]
            pl += 1
        else:
            A[k] = partRight[pr]
            pr += 1
    return res


def naive(A):
    len_ = len(A)
    res = 0
    for i in range(len_):
        for j in range(i + 1, len_):
            if A[i] > A[j]:
                res += 1
    return res

'''
归并排序是一种稳定的排序方式，但是快速排序是一种不稳定的排序方式，不稳定性发生在pivot和最终的位置交换的时候。
for example:
[1,3,4,5,2]	当3作为主元的时候，2会被置换到前面，此时5,2的顺序改变。
BTW，附上快排的两种实现方式
'''
def partition(A, left, right):
    x = A[left]  # 将第一个元素作为主元
    i, j = left, right
    while i <= j:
        while i <= j and A[i] <= x:  # 从左向右扫描
            i += 1
        while i <= j and A[j] >= x:  # 从右向左扫描
            j -= 1
        if i < j:  # A[i] > x > A[j]
            A[i], A[j] = A[j], A[i]
    A[left], A[j] = A[j], A[left]	# 排序不稳定性来源
    return j

def partition_(A, left, right):
    x = A[left]  # 将第一个元素作为主元
    i, j = left, left + 1
    while j <= right:
        if x > A[j]:    # 将所有大于主元的数字放在主元的左边
            i += 1
            A[i], A[j] = A[j], A[i]
        j += 1
    A[left], A[i] = A[i], A[left]
    return i  # 主元位置

def quickSort(A, left, right):
    '''
    :param A: 数组A
    :return:
    '''
    if left >= right:
        return 0
    mid = partition(A, left, right)
    quickSort(A, left, mid - 1)
    quickSort(A, mid + 1, right)