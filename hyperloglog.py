import shakespeare, sys, mmh3, math, collections, random, string, hllbias, statistics

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
    works = list(shakespeare.each_work())
    for p in range(7, 19):
        T0 = []
        T2 = []
        for name, words in works:
            H = HyperLogLog(p)
            for word in words:
                H.add(word)
            T0.append(abs(len(words) - H.cardinality(method=0))/len(words))
            T2.append(abs(len(words) - H.cardinality(method=2))/len(words))
        print('\t'.join(map(str, (p, statistics.mean(T2), statistics.mean(T2)+statistics.stdev(T2), max(T2)))))
    

            
            
            
