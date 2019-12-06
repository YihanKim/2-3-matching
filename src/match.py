import networkx as nx
import random
import sys


class GenderException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class FileReader(object):
    
    def read_file(fname):
        vertices = []
        edges = []
        return vertices, edges

class MatchingTwo(FileReader, object):
    def read_file(fname):
        vertices = []
        genders = []
        edges = []
        with open(fname, 'r') as f:
            # first line - readline and strip
            n = int(f.readline().strip())
            for i in range(n):
                args = f.readline().strip().split()
                src, gender, *dests = args
                assert len(dests) <= 1, "Multiple directed edges were given"
                vertices.append(src)
                genders.append(gender)
                edges.extend([(src, dest) for dest in dests])
        G = nx.DiGraph()
        for (v, g) in zip(vertices, genders):
            G.add_node(v, gender=g)
        G.add_edges_from(edges)
        return G
    
    def __init__(self, fname):
        G = MatchingTwo.read_file(fname)
        self.G = G
    
    def check_constraint(p, q):
        pass

    def match(self):
        M = []
        unmatched = list(self.G.nodes)
        assert len(unmatched) % 2 == 0, "The number of nodes should be even"
        
        # finding 2-cycles
        for u, v in self.G.edges:
            if self.G.has_edge(v, u) and v in unmatched:
                M.append((u, v))
                unmatched.remove(u)
                unmatched.remove(v)
        
        full_matched = len(M)

        # use greedy search for single directed edges
        _G = self.G.subgraph(unmatched)
        for u, v in random.sample(_G.edges, len(_G.edges)):
            if u in unmatched and v in unmatched:
                M.append((u, v))
                unmatched.remove(u)
                unmatched.remove(v)

        partially_matched = len(M) - full_matched
        
        # and then randomly match the others
        random.shuffle(unmatched)
        while len(unmatched) > 0:
            u = unmatched.pop()
            v = unmatched.pop()
            M.append((u, v))

        acceptance_rate = (full_matched * 2 + partially_matched) / len(self.G.edges)
        print('Acceptance rate: {}'.format(acceptance_rate))
        return M

class MatchingThree(FileReader, object):
    def read_file(fname):
        vertices = []
        genders = []
        edges = []
        isolated = []
        with open(fname, 'r') as f:
            n, m = map(int, f.readline().strip().split())
            for i in range(n):
                args = f.readline().strip().split()
                src, gender, *dests = args
                vertices.append(src)
                genders.append(gender)
                edges.extend([(src, dest) for dest in dests])
            for j in range(m):
                p, q = f.readline().strip().split()
                isolated.append((p, q))
                isolated.append((q, p))
        G = nx.DiGraph()
        for v, g in zip(vertices, genders):
            G.add_node(v, gender=g)
        G.add_edges_from(edges)

        return G, isolated 
     
    def __init__(self, fname):
        G, I = MatchingThree.read_file(fname)
        self.G = G
        self.I = I
    
    def check_constraint(self, p, q, r):
        # exclusive constraint
        assert (p, q) not in self.I, "Mutual-exclusive member {}, {}".format(p, q)
        assert (q, r) not in self.I, "Mutual-exclusive member {}, {}".format(q, r)
        assert (r, p) not in self.I, "Mutual-exclusive member {}, {}".format(r, p)
        # gender constraint
        gdp, gdq, gdr = self.G.nodes[p]['gender'], self.G.nodes[q]['gender'], self.G.nodes[r]['gender']
        
        if gdp == gdq == gdr == 'F':
            raise GenderException("cannot form a group with 3 females")
        return True
    
    def soft_check_constraint(self, p, q, r):
        try: 
            return self.check_constraint(p, q, r)
        except:
            return False

    def evaluate_acceptance_rate(self, p, q, r):
        acc_edges = 0
        if self.G.has_edge(p, q): acc_edges += 1
        if self.G.has_edge(q, p): acc_edges += 1
        if self.G.has_edge(p, r): acc_edges += 1
        if self.G.has_edge(r, p): acc_edges += 1
        if self.G.has_edge(q, r): acc_edges += 1
        if self.G.has_edge(r, q): acc_edges += 1
        return acc_edges

    def match(self):
        M = []
        _M = []
        unmatched = list(self.G.nodes)
        assert len(unmatched) % 3 == 0, "The number of nodes should be multiple of 3"
        
        # finding 3-cycles
        '''
        for u, v in self.G.edges:
            w = next(self.G.neighbors(v), None)
            if u != w and \
                    w is not None and \
                    self.G.has_edge(w, u) and \
                    u in unmatched and \
                    v in unmatched and \
                    w in unmatched: 
                try:
                    self.check_constraint(u, v, w)
                except AssertionError as e:
                    raise Exception("3-cycle({}, {}, {}) violates contraint: {}".format(u, v, w, e))
                except GenderException as e:
                    print(e)
                    _M.append([u, v, w])
                    unmatched.remove(u)
                    unmatched.remove(v)
                    unmatched.remove(w)
                else:
                    M.append((u, v, w))
                    unmatched.remove(u)
                    unmatched.remove(v)
                    unmatched.remove(w)
        '''
        _G = self.G.subgraph(unmatched)
        
        m_nodes = [x for x,y in _G.nodes(data=True) if y['gender'] == 'M']
        f_nodes = [x for x,y in _G.nodes(data=True) if y['gender'] == 'F']
        
        if len(f_nodes) > len(m_nodes) * 2:
            raise Exception("Cannot avoid 3 female students in a team")
        
        # group randomly and shuffle until satisfies the constraint
        __M = [[] for _ in range(len(unmatched) // 3)]
        i = 0
        for node in random.sample(f_nodes, len(f_nodes)):
            __M[i % len(__M)].append(node)
            i += 1

        for node in random.sample(m_nodes, len(m_nodes)):
            __M[i % len(__M)].append(node)
            i += 1
        
        _M.extend(__M)

        _swap_limit = 200000
        while True:
            if _swap_limit <= 0:
                raise RuntimeError('Maximum number of swaps exceeded')
            conds = [self.soft_check_constraint(*team) for team in _M]
            if not all(conds):
                first_violates = _M[conds.index(False)]
                # randomly select the other set
                other = _M[random.randint(0, len(_M) - 1)]
                i, j = random.randint(0, 2), random.randint(0, 2)
                first_violates[i], other[j] = other[j], first_violates[i]
                _swap_limit -= 1
                continue
            else:
                break
        print(_M)

        # evolutionary optimization
        for _ in range(len(_M) ** 2):
            i, j = random.sample(range(len(_M)), 2)
            group1, group2 = _M[i], _M[j]
            i, j = random.randint(0, 2), random.randint(0, 2)
            acc = self.evaluate_acceptance_rate(*group1) + \
                    self.evaluate_acceptance_rate(*group2)
            group1[i], group2[j] = group2[j], group1[i]
            if not self.soft_check_constraint(*group1) or \
                not self.soft_check_constraint(*group2) or \
                acc > self.evaluate_acceptance_rate(*group1) + \
                self.evaluate_acceptance_rate(*group2):
                group1[i], group2[j] = group2[j], group1[i]
            
        M.extend(map(tuple, _M))
        acc = [self.evaluate_acceptance_rate(*g) for g in M]
        print("Acceptance rate : {} / {} = {}".format(sum(acc), len(self.G.edges), sum(acc) / len(self.G.edges)))
        return M


        # The code below describes the old grouping method. 
        '''
        two_cycles = []
        
        # finding non-cycle paths
        for u, v in random.sample(_G.edges, len(_G.edges)):
            w = next(self.G.neighbors(v), None)
            if w is not None and \
                    u in unmatched and \
                    v in unmatched and \
                    w in unmatched:
                # case 1. u -> v -> u(2-cycle)
                if w == u:
                    try:
                        self.check_constraint(u, v, w)
                    except AssertionError:
                        continue
                    else:
                        two_cycles.append((u, v))
                        # do nothing; skip
                # case 2. u -> v -> w(!= u)
                else:
                    try:
                        self.check_constraint(u, v, w)
                    except AssertionError:
                        continue
                    else:
                        M.append((u, v, w))
                        unmatched.remove(u)
                        unmatched.remove(v)
                        unmatched.remove(w)

        two_matched = len(M) - full_matched

        # finding isolated
        _G = self.G.subgraph(unmatched)
        random.shuffle(unmatched)
        while len(unmatched) > 0:
            u = unmatched.pop()
            v = unmatched.pop()
            w = unmatched.pop()
            try:
                self.check_constraint(u, v, w)
            except AssertionError:
                unmatched.extend([u, v, w])
                random.shuffle(unmatched)
            else:
                M.append((u, v, w))
        '''

        return M


def main(*arg):
    matchType = arg[1]
    filename = arg[2]
    if matchType == '2':
        m = MatchingTwo(filename)
    elif matchType == '3':
        m = MatchingThree(filename)
    result = m.match()
    for i, g in enumerate(result):
        print("Group {}: {}".format(i + 1, ", ".join(g)))

if __name__ == "__main__":
    main(*sys.argv)

