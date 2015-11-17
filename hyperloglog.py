import shakespeare, sys, mmh3, math, collections, random, string, hllbias

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
        
    def cardinality(self, method):
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

if __name__ == '__main__':
    words = set(shakespeare.all_words())
    expected = len(words)
    print expected
    for p in range(7, 19):
        H = HyperLogLog(p)
        for word in words:
            H.add(word)
        print p, H.cardinality(method=0), H.cardinality(method=1), H.cardinality(method=2)      
    

            
            
            
