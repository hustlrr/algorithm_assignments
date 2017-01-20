# coding=utf-8

# Created by lruoran on 17-1-20

# 利用二项堆实现优先队列

from Datautils import loadGraph

class binomialNode:
    def __init__(self, node=None, dist=None):
        self.node = node
        self.dist = dist
        self.parent = None
        self.child = None
        self.sibling = None
        self.degree = 0


class priorQueue:
    def __init__(self):
        self.head = binomialNode()
        self.points = {}

    def merge(self, h2):
        p1 = self.head.sibling if self.head else None  # merge
        p2 = h2.head.sibling if h2.head else None
        self.head.sibling = None
        p = self.head

        def move2anotherlist(p, p1):
            tmp = p1.sibling
            p1.sibling = p.sibling
            p.sibling = p1
            p1 = tmp
            return p1

        while p1 and p2:
            if p1.degree < p2.degree:
                p1 = move2anotherlist(p, p1)
            elif p1.degree > p2.degree:
                p2 = move2anotherlist(p, p2)
            else:
                p1 = move2anotherlist(p, p1)
                p = p.sibling
                p2 = move2anotherlist(p, p2)
            p = p.sibling
        while p1:
            p1 = move2anotherlist(p, p1)
            p = p.sibling
        while p2:
            p2 = move2anotherlist(p, p2)
            p = p.sibling

    def union(self, h2):
        def link(y, z):  # z成为y的父节点
            y.parent = z
            y.sibling = z.child
            z.child = y
            z.degree += 1

        self.merge(h2)
        if self.empty():
            return
        prev_p, p, next_p = self.head, self.head.sibling, self.head.sibling.sibling
        while next_p:
            if (p.degree != next_p.degree) or \
                    (next_p.sibling and p.degree == next_p.sibling.degree):
                prev_p = p
                p = next_p
            elif p.dist <= next_p.dist:
                p.sibling = next_p.sibling
                link(next_p, p)
            else:
                prev_p.sibling = next_p
                link(p, next_p)
                p = next_p
            next_p = p.sibling
        return self.head

    def insert(self, node, dist):
        '''
        :param node:节点编号
        :param dist:源节点到该节点的距离
        :return:
        '''
        h2 = priorQueue()
        h2.head.sibling = binomialNode(node=node, dist=dist)
        self.union(h2)
        self.points[node] = h2.head.sibling
        return self.head

    def extractmin(self):
        '''
        :return:
        '''
        pmin, distmin = None, (1 << 32)
        p = self.head.sibling
        while p:
            pmin, distmin = (p, p.dist) if (pmin is None or distmin > p.dist) else (pmin, distmin)
            p = p.sibling
        p = self.head
        while p and p.sibling:
            if p.sibling == pmin:
                p.sibling = p.sibling.sibling
                break
            p = p.sibling
        if pmin:
            h2 = priorQueue()
            h2.head.sibling = pmin.child
            self.union(h2)
            self.points.pop(pmin.node)
        return (pmin.dist, pmin.node)

    def decreasekey(self, node, newdist):
        '''
        :param node:
        :param newdist:
        :return:
        '''

        def swap(y, z):
            z.dist, y.dist = y.dist, z.dist
            self.points[z.node], self.points[y.node] = self.points[y.node], self.points[z.node]
            z.node, y.node = y.node, z.node

        p = self.points[node]
        p.dist = newdist
        y = p
        z = p.parent
        while z and z.dist > y.dist:
            # z.dist, y.dist = y.dist, z.dist
            swap(y, z)
            y = z
            z = y.parent

    def empty(self):
        '''
        :return:
        '''
        return self.head.sibling is None


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
    with open(r'data/dist_binomial_heap', 'w') as fw:
        for node, dist in key.items():
            fw.write('%s %d\n' % (node, dist))