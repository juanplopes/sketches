import shakespeare, sys, mmh3, math, collections, random, string, hllbias, statistics, heapq

class HyperLogLog:
    def __init__(self, log2m):
        self.log2m = log2m
        self.m = 1 << log2m
        self.data = [0]*self.m
        self.alphaMM = (0.7213 / (1 + 1.079 / self.m)) * self.m * self.m
        
    def add(self, o):
        x = mmh3.hash(str(o), 0)

        a, b = 32-self.log2m, self.log2m

        i = x >> a
        v = self._bitscan(x << b, a)
        
        self.data[i] = max(self.data[i], v)

    def union(self, hb):
        hc = HyperLogLog(self.log2m)
        for i in range(self.m):
            hc.data[i] = max(self.data[i], hb.data[i])
        return hc

    def cardinality(self, method=2):
        estimate = self.alphaMM / sum([2**-v for v in self.data])
        zeros = float(self.data.count(0))
        if method == 2:
            bias = hllbias.bias(self.log2m, estimate)
            if estimate <= 5 * self.m:
                estimate -= bias
            if zeros != 0:
                h = -self.m * math.log(zeros / self.m)
            else:
                h = estimate
            if h < hllbias.threshold(self.log2m):
                return round(h)
            else:
                return round(estimate)                
        elif estimate <= 2.5 * self.m and method == 0:
            return round(-self.m * math.log(zeros / self.m))
        else:
            return round(estimate)
        
    def _bitscan(self, x, m):
        v = 1
        while v<=m and not x&0x80000000:
            v+=1
            x<<=1
        return v

class MinHash:
    def __init__(self, m):
        self.m = m
        self.data = []
        
    def add(self, o):
        h = mmh3.hash(o, 0)
        if len(self.data) < self.m:
            heapq.heappush(self.data, -h)
        else:
            heapq.heappushpop(self.data, -h)

    def jaccard(self, other):
        HX = heapq.nlargest(self.m, set(self.data).union(other.data))
        HY = set(HX).intersection(self.data).intersection(other.data)
        return len(HY)/float(self.m)

def minhash(m, A):
    mh = MinHash(m)
    for word in A:
        mh.add(word)
    return mh

def hll(p, A):
    HA = HyperLogLog(p)
    for word in A:
        HA.add(word)
    return HA

def normal_compare(A, B):
    SA = set(A)
    SB = set(B)
    return len(SA.intersection(SB))


def real(works):
    real = {}
    for i in range(len(works)):
        for j in range(i+1, len(works)):
            name1, words1 = works[i]
            name2, words2 = works[j]
            real[(name1, name2)] = normal_compare(words1, words2)
    return real

if __name__ == '__main__':
    #shakespeare.write_duplicates()
    #sys.exit(0)

    works = list(shakespeare.each_work()) + list(shakespeare.each_work('duplicates'))

    real = real(works)
    
    hashes = {name: minhash(2048, A) for name, A in works}

    sys.stderr.write('_\n')
    for p in range(7, 19):
        hlls = {name: hll(p, A) for name, A in works}

        sys.stderr.write(str(p)+'\n')
        T = []
        for i in range(len(works)):
            for j in range(i+1, len(works)):
                name1, words1 = works[i]
                name2, words2 = works[j]
                normal = real[(name1, name2)]
                jaccard = hashes[name1].jaccard(hashes[name2])
                union = hlls[name1].union(hlls[name2]).cardinality()
                
                #print(' ', abs(jaccard*union-normal)/normal, jaccard*union, normal)
                T.append(abs(jaccard*union-normal)/normal)
        print('\t'.join(map(str, (p, statistics.mean(T), statistics.mean(T)+statistics.stdev(T), max(T)))))

    

            
            
            
