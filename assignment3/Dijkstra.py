# coding=utf-8

from Datautils import loadGraph


class fibNode:
    def __init__(self, d=None, node=None):
        self.dist = d
        self.node = node
        self.parent = None
        self.left = self
        self.right = self
        self.child = None
        self.degree = 0
        self.mark = False


class priorQueue:
    def __init__(self):
        self.head = fibNode()
        self.min = None
        self.n = 0
        # self.dn = 0  # 最大的根结点度数
        self.points = {}

    def merge(self, p):  # 将结点p合入self.head
        p.right = self.head.right
        p.left = self.head
        self.head.right.left = p
        self.head.right = p

    def insert(self, node, dist):
        p = fibNode(d=dist, node=node)
        self.points[node] = p
        self.merge(p)
        if self.min is None or self.min.dist > p.dist:
            self.min = p
        self.n = self.n + 1

    def link(self, y, x):  # 把y从根结点删除，成为x的子节点
        y.left.right = y.right  # 把y从根结点链表删除
        y.right.left = y.left

        if x.child is not None:
            y.right = x.child  # 使y成为x的孩子节点
            y.left = x.child.left
            x.child.left.right = y
            x.child.left = y
        else:
            y.left, y.right = y, y
        x.child = y
        y.parent = x
        x.degree += 1

        y.mark = False

    def consolidate(self):
        a = [None for _ in range(self.n)]
        w = self.head.right
        while w != self.head:
            # print 'w', w.dist
            tmp = w.right
            x = w
            d = x.degree
            while a[d] is not None:
                y = a[d]
                if x.dist > y.dist:
                    x, y = y, x
                self.link(y, x)
                a[d] = None
                d = d + 1
            a[d] = x
            w = tmp  # 调试,遍历根结点链表不能使用w=w.right，因为w可能已经成为另一个根结点的子节点，所以w.right也不再是根结点
        self.min = None
        for i in range(self.n):
            if a[i] is not None:
                # self.merge(a[i])
                self.min = a[i] if (self.min is None or self.min.dist > a[i].dist) else self.min

    def extractmin(self):
        z = self.min
        if z is not None:
            x = z.child
            for _ in range(z.degree):
                x.parent = None
                tmp = x.right
                self.merge(x)
                x = tmp
            z.right.left = z.left  # 将z从根链表删除
            z.left.right = z.right
            if z == z.right:
                self.min = None
            else:
                self.min = z.right
                self.consolidate()
            self.n = self.n - 1
        return (z.dist, z.node)

    def cut(self, x, y):  # 把x从y的孩子链表删除，加入根链表
        x.right.left = x.left
        x.left.right = x.right
        if x == x.right:
            y.child = None
        else:           # 在算法导论的伪代码中没有处理else的情况，但是显然如果不处理会丢掉子节点
            y.child = x.right
        y.degree = y.degree - 1

        self.merge(x)
        x.parent = None
        x.mark = False

    def cascadingCut(self, y):
        z = y.parent
        if z is not None:
            if y.mark == False:
                y.mark = True
            else:
                self.cut(y, z)
                self.cascadingCut(z)

    def decreasekey(self, node, newdist):
        x = self.points[node]
        x.dist = newdist
        y = x.parent
        if y is not None and x.dist < y.dist:
            # print 'cut'
            self.cut(x, y)
            self.cascadingCut(y)
        if x.dist < self.min.dist:
            self.min = x

    def empty(self):
        return self.head.right == self.head


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

    with open(r'data/dist_fib_heap', 'w') as fw:
        for node, dist in key.items():
            fw.write('%s %d\n' % (node, dist))
