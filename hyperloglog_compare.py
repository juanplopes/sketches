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
                h = round(-self.m * math.log(zeros / self.m))
            else:
                h = estimate
            if h < hllbias.threshold(self.log2m):
                return h
            else:
                return estimate                
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
    rounds = 64
    total = [set() for i in range(rounds)]

    H0 = [HyperLogLog(12) for i in range(rounds)]
   
    for i in xrange(30001):
        err0 = []
        err1 = []
        err2 = []
        for j in xrange(rounds):
            word = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
            total[j].add(word)
            H0[j].add(word)
            
            expected = len(total[j])

            if i%200==0:
                actual0 = H0[j].cardinality(method = 0)
                err0.append(abs(actual0/expected-1))

                actual1 = H0[j].cardinality(method = 1)
                err1.append(abs(actual1/expected-1))

                actual2 = H0[j].cardinality(method = 2)
                err2.append(abs(actual2/expected-1))
        if i%200==0:
            sys.stderr.write(str(i)+'\n')
            print i, sum(err0)/len(err0), sum(err1)/len(err1), sum(err2)/len(err2)

            
            
            
