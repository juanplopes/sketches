import shakespeare, sys, mmh3, math, collections

class Bloom:
    def __init__(self, m, k):
        self.data = [0] * m
        self.m = m
        self.k = k
        
    def add(self, word):
        for i in range(self.k):
            h = mmh3.hash(word, i) 
            self.data[h % self.m] = 1

    def contains(self, word):
        for i in range(self.k):
            h = mmh3.hash(word, i) 
            if not self.data[h % self.m]:
                return False
        return True

    def falsep(self, n):
        return (1 - (1 - 1.0/self.m)**(self.k*n))**self.k  

    def cardinality(self):
        zeros = float(self.data.count(0))
        return round(-self.m / self.k * math.log(zeros / self.m))

if __name__ == '__main__':
    B = Bloom(2**20, 5)
    for word in shakespeare.all_words():
        B.add(word)

    C = shakespeare.print_counter()

    print 'Probability of false positive:', B.falsep(len(C))
    print 'Estimated cardinality:', B.cardinality()
    for test in iter(sys.stdin.readline, ''):
        test = test.strip().lower()
        
        print 'Bloom filter: ', B.contains(test)
        print 'Counter: ', C.has_key(test)
            
            
