import mmh3, math, collections, random, string, hllbias, statistics, heapq

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
        h = mmh3.hash64(o)[0]
        if len(self.data) < self.m:
            heapq.heappush(self.data, -h)
        else:
            heapq.heappushpop(self.data, -h)

    def jaccard(self, other):
        HX = heapq.nlargest(self.m, set(self.data).union(other.data))
        HY = set(HX).intersection(self.data).intersection(other.data)
        print(len(HY))
        return len(HY)/self.m

class IntersectionSketch:
    def __init__(self):
        self.mh = MinHash(2048)
        self.hll = HyperLogLog(10)
        
    def add(self, o):
        self.mh.add(str(o))
        self.hll.add(str(o))
        
    def intersection(self, other):
        union = self.hll.union(other.hll).cardinality()
        jaccard = self.mh.jaccard(other.mh)
        print(union, jaccard)
        return union*jaccard
        
if __name__ == '__main__':
    a = IntersectionSketch()
    b = IntersectionSketch()
    
    for i in range(1000000):
        a.add(i)
    for i in range(1000000-1, 2000000):
        b.add(i)

    answer = a.intersection(b)
    print(answer)

    

