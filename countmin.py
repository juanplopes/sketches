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

if __name__ == '__main__':
    M = CountMin(2**16, 5)
    for word in shakespeare.all_words():
        M.add(word)

    C = shakespeare.print_counter()

    print 'Estimated cardinality:', M.cardinality()
    for test in iter(sys.stdin.readline, ''):
        test = test.strip().lower()
        
        print 'Count-Min: ', M.count(test)
        print 'Counter: ', C[test]
            
            
