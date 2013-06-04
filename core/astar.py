from math import sqrt

TOO_HIGH_COST = 1000

class AStar(object):
    def __init__(self, graph):
        self.graph = graph
        
    def heuristic(self, node, start, end):
        raise NotImplementedError
        
    def search(self, start, end):
        g = {}
        h = {}
        parent = {}
        openset = set()
        closedset = set()
        current = start
        openset.add(current)
        def gg(n):
            if n not in g:
                g[n] = 0
                return 0
            return g[n]
        def gh(n):
            if n not in h:
                h[n] = 0
                return 0
            return h[n]
        def gp(n):
            if n not in parent:
                parent[n] = None
                return None
            return parent[n]
        while openset:
            current = min(openset, key=lambda o:gg(o) + gh(o))
            if current == end:
                path = []
                while gp(current):
                    path.append(current)
                    current = gp(current)
                path.append(current)
                return path[::-1]
            openset.remove(current)
            closedset.add(current)
            for node in self.graph[current]:
                if node in closedset:
                    continue
                if current.move_cost(node)>=TOO_HIGH_COST:
                    continue
                if node in openset:
                    new_g = gg(current) + current.move_cost(node)
                    if gg(node) > new_g:
                        g[node] = new_g
                        parent[node] = current
                else:
                    g[node] = gg(current) + current.move_cost(node)
                    h[node] = self.heuristic(node, start, end)
                    parent[node] = current
                    openset.add(node)
        return None

class AStarNode(object):
    def __init__(self):
        self.g = 0
        self.h = 0
        self.blocked = False
        self.parent = None
        
    def move_cost(self, other):
        raise NotImplementedError

class AStarGrid(AStar):
    def heuristic(self, node, start, end):
        return sqrt((end.x - node.x)**2 + (end.y - node.y)**2)

class AStarGridNode(AStarNode):
    def __init__(self, x, y):
        self.x, self.y = x, y
        super(AStarGridNode, self).__init__()

    def move_cost(self, other):
        diagonal = abs(self.x - other.x) == 1 and abs(self.y - other.y) == 1
        #~ if diagonal:
            #~ return TOO_HIGH_COST
        if self.blocked:
            return TOO_HIGH_COST
        return 10

if __name__=="__main__":
    from itertools import product

    def make_graph(mapinfo):
        nodes = [[AStarGridNode(x, y) for y in range(mapinfo["height"])] for x in range(mapinfo["width"])]
        graph = {}
        for x, y in product(list(range(mapinfo["width"])), list(range(mapinfo["height"]))):
            node = nodes[x][y]
            graph[node] = []
            for i, j in product([-1, 0, 1], [-1, 0, 1]):
                if not (0 <= x + i < mapinfo["width"]): continue
                if not (0 <= y + j < mapinfo["height"]): continue
                graph[nodes[x][y]].append(nodes[x+i][y+j])
        return graph, nodes

    graph, nodes = make_graph({"width": 8, "height": 8})
    paths = AStarGrid(graph)
    start, end = nodes[1][1], nodes[5][7]
    path = paths.search(start, end)
    if path is None:
        print("No path found")
    else:
        print("Path found:", path)