# coding=utf-8

# Created by lruoran on 17-1-20

# 利用二叉堆实现优先队列

from Datautils import loadGraph

def dijkstra(G, s):
    import heapq
    key = {node: 0 for node in G.keys()}  # s到所有节点的距离
    pq = [[key[s], s, ]]  # 保存未被访问的节点的距离
    exploredSet = set()  # 已经被访问过的所有节点
    exploredSet.add(s)
    heapq.heapify(pq)
    inf = 1<<31
    for node in G.keys():
        if node == s:
            continue
        key[node] = inf
        heapq.heappush(pq, [inf, node])

    while len(pq):
        v = heapq.heappop(pq)
        dist, nodev = v
        exploredSet.add(nodev)
        for adj in G[nodev]:
            w, adjnode = adj
            if adjnode in exploredSet:
                continue
            if key[nodev] + w < key[adjnode]:
                for idx, (d, n) in enumerate(pq):
                    if adjnode == n:
                        pq[idx][0] = key[nodev] + w
                        key[adjnode] = key[nodev] + w
                heapq.heapify(pq)
    return key

import time

if __name__ == '__main__':
    G = loadGraph(r'data/graph.txt')
    s = time.clock()
    sourcenode = '0'
    print 'source node:', sourcenode
    key = dijkstra(G, sourcenode)
    t = time.clock()
    print 'time = ', t - s
    with open(r'data/dist_binary_heap', 'w') as fw:
        for node, dist in key.items():
            fw.write('%s %d\n' % (node, dist))