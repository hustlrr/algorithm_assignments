# coding=utf-8

# Created by lruoran on 17-1-20

from Datautils import loadGraph

# 使用链表实现优先队列
# 利用prior queue在dijkstra中的应用进行测试

class linkedList:
    def __init__(self, d=None, node=None):
        self.dist = d
        self.node = node
        self.next_ = None


class priorQueue:
    def __init__(self):
        self.head = linkedList()

    def insert(self, node, dist):
        p = linkedList(d=dist, node=node)
        p.next_ = self.head.next_
        self.head.next_ = p

    def extractmin(self):
        mindist, minnode = (1 << 32), 0  # 此处的初始化应该大于创建pq时的初始化，否则如果剩余的节点都是无法到达的节点会陷入死循环
        p = self.head.next_
        while p:
            if p.dist < mindist:
                mindist = p.dist
                minnode = p.node
            p = p.next_
        p = self.head
        while p and p.next_:
            if p.next_.node == minnode:
                p.next_ = p.next_.next_
                break
            p = p.next_
        return (mindist, minnode)

    def decreasekey(self, node, newdist):
        p = self.head.next_
        while p:
            if p.node == node:
                p.dist = newdist
                break
            p = p.next_

    def empty(self):
        return self.head.next_ == None


def dijkstra(G, s):
    key = {node: (1 << 31) for node in G.keys()}  # s到所有节点的距离
    key[s] = 0
    exploredSet = set()  # 已经被访问过的所有节点
    exploredSet.add(s)  # 源节点已被访问

    pq = priorQueue()
    for node in G.keys():
        pq.insert(node=node, dist=key[node])
    while not pq.empty():
        (mindist, minnode) = pq.extractmin()
        print len(exploredSet), minnode, mindist
        exploredSet.add(minnode)
        for adjweight, adjnode in G[minnode]:
            if adjnode in exploredSet:  # 已经访问过
                continue
            if mindist + adjweight < key[adjnode]:
                key[adjnode] = mindist + adjweight
                pq.decreasekey(adjnode, mindist + adjweight)
                # print 'decrease', adjnode, pq.points[adjnode].dist
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
    with open(r'data/dist_linked_list', 'w') as fw:
        for node, dist in key.items():
            fw.write('%d %d\n' % (node, dist))