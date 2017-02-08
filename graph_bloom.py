import random, mmh3, collections

class Bloom:
    def __init__(self, m, k):
        m = max(m, 1)
        self.data = [0] * m
        self.m = m
        self.k = k
        
    def add(self, word):
        for i in range(self.k):
            h = mmh3.hash(str(word), i) 
            self.data[h % self.m] = 1

    def contains(self, word):
        for i in range(self.k):
            h = mmh3.hash(str(word), i) 
            if not self.data[h % self.m]:
                return False
        return True

    def cardinality(self):
        try:
            zeros = float(self.data.count(0))
            return round(-self.m / self.k * math.log(zeros / self.m))
        except:
            return -1

def random_graph(n, m):
    S = set()
    while len(S) < m:
        a = random.randint(0, n-1)
        b = random.randint(0, n-1)
        a, b = min(a, b), max(a, b)

        if a!=b and (a, b) not in S:
            S.add((a, b))
    return S
            
def test_bloom1(n, m):
    G = random_graph(n, m)
    P = Bloom(10*m, 7)
    
    for e in G:
        P.add(e)
        
    answer = 0
    for i in range(n):
        for j in range(i+1, n):
            if P.contains((i, j)) != ((i, j) in G):
                answer+=1
    return answer

def test_bloom2(n, m):
    G = random_graph(n, m)
    D = collections.Counter(x for x, _ in G)
    P = [Bloom(10*D[i], 7) for i in range(n)]

    for a, b in G:
        P[a].add(b)

    answer = 0
    for i in range(n):
        for j in range(i+1, n):
            if P[i].contains(j) != ((i, j) in G):
                answer+=1
    return answer

def test(n, m, fn):
    s = 0
    for i in xrange(100):
        s += fn(n, m)
    return s/100.0

N = 100
for m in xrange(0, 21):
    M = int(round(N*(N-1)/2*(m/20.0)))

    print M, test(N, M, test_bloom1), test(N, M, test_bloom2), 0.008193722*(N*(N-1)/2-M)

    
