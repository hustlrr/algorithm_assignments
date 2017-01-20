# coding=utf-8

# Created by lruoran on 17-1-20


def longestIncreasingSequence(a):
    '''
    :param a: list
    :return: int
    '''
    n = len(a)
    dp = [1 for _ in range(n)]
    for i in range(1,n):
        for j in range(i):
            if a[i] > a[j]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)

if __name__ == '__main__':
    a = range(10, 1, -1)
    print longestIncreasingSequence(a)