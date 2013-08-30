import shakespeare, sys, mmh3, math, collections

class CountMin:
    def __init__(self, m, k):
        self.data = [[0] * m for i in range(k)]
        self.m = m
        self.k = k
        
    def add(self, word, count=1):
        for i in range(self.k):
            h = mmh3.hash(word, i) 
            self.data[i][h % self.m] += count

    def count(self, word):
        m = 2**30
        for i in range(self.k):
            h = mmh3.hash(word, i) 
            m = min(m, self.data[i][h % self.m])
        return m

    def falsep(self, n):
        return (1 - (1 - 1.0/self.m)**(self.k*n))**self.k  

    def cardinality(self):
        zeros = sum(float(d.count(0)) for d in self.data)
        return round(-self.m * math.log(zeros / self.m / self.k))

class CountMinRange:
    def __init__(self, m, k, n):
        self.cmin = CountMin(m, k)
        self.n = n

    def add(self, value, count=1):
        while value < self.n:
            self.cmin.add(str(value), count)
            value += value & -value
            
    def count_upto(self, value):
        s = 0
        while value:
            s += self.cmin.count(str(value))
            value -= value & -value
        return s

if __name__ == '__main__':
    M = CountMinRange(2**16, 5, 2**31) 
    for i in range(1, 10000):
        M.add(i, i-100)

    s = 0
    for i in range(1,10000):
        s += i-100
        print s, M.count_upto(i)
