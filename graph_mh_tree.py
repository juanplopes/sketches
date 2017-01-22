import random, mmh3, collections, math, heapq

def gen_set(S, to):
    return [S[2*i+bin(i&to).count('1')%2] for i in xrange(len(S)/2)]

def unique_numbers():
    i = [0]
    def gen(n): 
        S = range(i[0], i[0]+n)
        i[0]+=n; 
        return S;
    return gen

def minhash_sig(A, k):
    return [min(mmh3.hash(str(word), i) for word in A) for i in range(k)]

def minhash(HA, HB, k):
    return sum(a==b for a, b in zip(HA, HB))/float(k)

def simhash_sig(A, k):
    n = 0
    for i in range(k):
        v = sum(1 if mmh3.hash(str(x), i)>0 else -1 for x in A)
        n = n*2+(v>=0)
    return n

def simhash(HA, HB, k):
    return (k-bin(HA^HB).count('1'))/float(k)

def random_tree(n, k, sig):
    N = unique_numbers()
    m = int(2**(math.ceil(math.log(n, 2))+1))
    G = [(None, N(m))]

    for i in range(n-1):
        j = random.randint(0, i)
        _, S = G[j]
    
        G.append((j, gen_set(S, i) if len(S) == m else S+N(m/2)))
    return [(p, sig(S, k)) for p, S in G]

def compute_error(N, k, sig, comp):
    G = random_tree(N, k, sig)

    print G

    total = 0
    E = 0
    EE = 0
    for i in range(N):
        for j in range(i+1, N):
            nei = G[i][0] == j or G[j][0] == i
            value = comp(G[i][1], G[j][1], k)
            ok = nei == (value >= 0.363198231)
            if not ok: E += 1
            if nei and not ok: EE += 1
            print nei, value
            total += 1
    print E, EE, total
    return float(E)/total
    
#print compute_error(200, 64, minhash_sig, minhash)
print compute_error(10, 64, simhash_sig, simhash)
