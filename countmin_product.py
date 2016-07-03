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

    def product(self, other):   
        answer = 2**30
        for i in range(self.k):
            s = 0
            for j in range(self.m):
                s += self.data[i][j] * other.data[i][j]
            answer = min(answer, s)
        return answer


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

def real(works):
    real = {}
    for i in range(len(works)):
        for j in range(i+1, len(works)):
            name1, words1 = works[i]
            name2, words2 = works[j]
            
            dic1 = collections.Counter(words1)
            dic2 = collections.Counter(words2)
           
            real[(name1, name2)] = sum(v*dic2[k] for k,v in dic1.items())
    return real


if __name__ == '__main__':
    works = list(shakespeare.each_work_raw()) + list(shakespeare.each_work_raw('duplicates'))
    real = real(works)

    for m in range(2**7, 2**12+1, 2**7):
        sys.stderr.write(str(m)+'\n')

        sketches = {}
        for name, words in works:
            M = CountMin(m, 3)
            for word in words:
                M.add(word)
            sketches[name] = M

        T = []
        for i in range(len(works)):
            for j in range(i+1, len(works)):
                name1, words1 = works[i]
                name2, words2 = works[j]
                normal = real[(name1, name2)]
                hashed = sketches[name1].product(sketches[name2])
                T.append(abs(hashed-normal) / (len(words1)* len(words2)))
                #print(i, j, normal, hashed, abs(hashed-normal) / (len(words1)* len(words2)), 2.718281828/m)
        T.sort()
        print('\t'.join(map(str, (m, statistics.mean(T), percentile(T, 0.999)))))
    
