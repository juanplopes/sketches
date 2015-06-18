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

    def cardinality(self):
        try:
            zeros = float(self.data.count(0))
            return round(-self.m / self.k * math.log(zeros / self.m))
        except:
            return -1

def test_errors(bloom, control, words):
    count = 0
    false = 0
    for word in words:
        count+=1
        if bloom.contains(word):
            false+=1
    print '\t'.join(str(x) for x in (len(control), bloom.cardinality(), false/float(count)))

if __name__ == '__main__':
    words = shakespeare.distinct_words()
    control = set()
    bloom = Bloom(2048, 1)
    
    print '\t'.join(('n', 'cardinality', 'falsep'))
    for word in words[:20000]:
        bloom.add(word)
        control.add(word)
        if len(control) % 500 == 0:
            test_errors(bloom, control, words[20000:])            

