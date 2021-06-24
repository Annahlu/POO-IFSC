import sys
import numpy as np

def string_to_dict(S):
    S = np.array(list(S))
    d = {}
    for s in np.unique(S):
        d[s] = np.sum(S == s)
    return d

def isanagrama(p1, p2):
    return string_to_dict(p1) == string_to_dict(p2)
        
def anagrama(P):
    sizes = np.array(list(map(lambda x : len(x), P)))
    ascii_sums = np.array(list(map(lambda x : np.sum(list(map(ord,list(x)))), P)))
    ascii_prods = np.array(list(map(lambda x : np.prod(list(map(ord,list(x)))), P)))
    passed = np.zeros(len(P))
    i = 0
    palavras = []
    for p1 in P:
        if(passed[i] == 0):
            anagramas = [p1]
            passed[i] = 1
            pos = np.where((sizes == sizes[i]) & (passed == 0) & (ascii_sums == ascii_sums[i]) & (ascii_prods == ascii_prods[i]))[0]
            for j in pos:
                if(isanagrama(p1, P[j])):
                    anagramas.append(P[j])
                    passed[j] = 1
            palavras.append(anagramas)
        i += 1
    return palavras

def save(v, filename):
    f = open(filename, "w", encoding='utf-8')
    
    for l in v:
        f.write(', '.join(l))
        f.write('\n')
    
    f.close()

filename = sys.argv[1]

f = open(filename, encoding='utf-8')
x = list(map(lambda x : x.replace('\n','').lower(), f.readlines()))
v = anagrama(x)
save(v,filename+".ana")
