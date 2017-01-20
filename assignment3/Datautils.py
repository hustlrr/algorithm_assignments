# coding=utf-8

def loadGraph(graph_path):
    with open(graph_path) as fr:
        lines = fr.readlines()
    G = {}
    for line in lines:
        if line.startswith('#'):
            continue  # 注释行
        if len(line.strip()) == 0:
            continue
        line = line.strip().split(' ')
        s, v, w = line[0], line[1], int(line[2])
        try:
            G[s].append((w, v,))
        except KeyError:
            G[s] = [(w, v,)]
        try:
            G[v]
        except KeyError:
            G[v] = []
            # try:
            #     G[v].append((w, s,))
            # except KeyError:
            #     G[v] = [(w, s,)]
    return G
