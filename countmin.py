import shakespeare, sys, mmh3, math, collections, heapq, statistics

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

def percentile(N, percent, key=lambda x:x):
    """
    Find the percentile of a list of values.

    @parameter N - is a list of values. Note N MUST BE already sorted.
    @parameter percent - a float value from 0.0 to 1.0.
    @parameter key - optional key function to compute value from each element of N.

    @return - the percentile of the values
    """
    import math
    import functools

    if not N:
        return None
    k = (len(N)-1) * percent
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return key(N[int(k)])
    d0 = key(N[int(f)]) * (c-k)
    d1 = key(N[int(c)]) * (k-f)
    return d0+d1

if __name__ == '__main__':
    word_list = list(shakespeare.all_words())
    C = shakespeare.print_counter()

    for m in range(2**7, 2**12+1, 2**7):
        sys.stderr.write(str(m)+'\n')

        M = CountMin(m, 3)
        for word in word_list:
            M.add(word)

        T = []
        top100 = C.items() #heapq.nlargest(10000, C.items(), key=lambda v:v[1])
        for word, count in top100:
            T.append((M.count(word)-count)/len(word_list))

        T.sort()
        print('\t'.join(map(str, (m, statistics.mean(T), percentile(T, 0.999)))))
    
