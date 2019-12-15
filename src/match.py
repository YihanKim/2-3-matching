import networkx as nx
import random

class TwoThreeMatching(object):
 
    def __init__(self, fname, seed = None):
        
        # use this flag for deterministic result
        if seed: 
            random.seed(seed)

        with open(fname, 'r') as f:
            vertices = []
            edges = []
            parseline = lambda: f.readline().strip()
            n = int(parseline())
            for _ in range(n):
                s, *ds = parseline().split() # source, dest
                vertices.append(s)
                for d in ds: edges.append((s, d))    
            G = nx.DiGraph()
            G.add_nodes_from(vertices)
            G.add_edges_from(edges)
        self.G = G
        return

    def match(self):
        G = self.G
        solid_matched = []
        flex_matched = []
        unmatched = list(G.nodes)

        assert 120 >= len(G), \
                "the total number of members under 80"

        assert 120 >= len(G), \
                "the total number of members exceed 120"

        THREE_GROUPS = len(G) - 80
        TWO_GROUPS = 40 - THREE_GROUPS
        
        print("2인조: {}팀, 3인조: {}팀".format(TWO_GROUPS, THREE_GROUPS))

        # priority matching (2-cycles)
        for u in unmatched:
            vs = G.neighbors(u)
            for v in vs:
                if G.has_edge(v, u):
                    solid_matched.append((u, v))
                    unmatched.remove(u)
                    unmatched.remove(v)
        
        # handling 2-cycles
        random.shuffle(solid_matched)
        random.shuffle(unmatched)
        while len(solid_matched) > TWO_GROUPS:
            flex_matched.append(solid_matched.pop())
            flex_matched[-1] += (unmatched.pop(),)
        
        for _ in range(TWO_GROUPS - len(solid_matched)):
            u = unmatched.pop()
            vs = G.neighbors(u)
            v = None
            for _v in vs:
                if _v in unmatched:
                    unmatched.remove(_v) 
                    v = _v
                    break
            if not v:
                v = unmatched.pop()
            flex_matched.append((u, v))


        assert len(unmatched) % 3 == 0

        while len(unmatched) > 0:
            u = unmatched.pop()
            v = unmatched.pop()
            w = unmatched.pop()
            flex_matched.append((u, v, w))

        
        for _ in range((len(flex_matched) // 2 + 40) ** 2):
            i = random.randint(0, len(flex_matched) - 1)
            j = random.randint(0, len(flex_matched) - 1)
            if i == j: continue

            g1 = flex_matched[i]
            g2 = flex_matched[j]
            merge = list(g1 + g2)
            random.shuffle(merge)
            
            split_idx = 3
            if len(merge) == 4: split_idx = 2
            g1_, g2_ = tuple(merge[:split_idx]), tuple(merge[split_idx:])

            G1 = G.subgraph(g1)
            G2 = G.subgraph(g2)

            G1_ = G.subgraph(g1_)
            G2_ = G.subgraph(g2_)
            
            # swap if the new match is not worse than original
            original_size = G1.size() + G2.size()
            new_size = G1_.size() + G2_.size()
            if original_size <= new_size:
                flex_matched[i] = g2_
                flex_matched[j] = g1_
        
        match = solid_matched + flex_matched
        return match
