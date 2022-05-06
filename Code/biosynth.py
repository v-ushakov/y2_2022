import re


def read_dna(fil):
    dna = ''
    with open(fil) as f:
        for a in f:
            a = a.strip().upper()
            if re.search('[^ATCG]', a):
                raise RuntimeError('Bad file contents')
            dna += a
    return dna


def proteins(seq):
    prot = []
    start = 0
    for a in range(3, len(seq)+1,3):
        prot.append(seq[start:a])
        start = a
    return prot


def find_gene(dna):
    # stops: ATT, ATC, ACT
    m = re.match(("(...)*?T(AA|AG|GA)"), dna)
    if m == None:
        return -1
    #print("m is in", m.span()[1])
    return m.span()[1]


def find_genes(dna):
    stops = ['TAA', 'TAG', 'TGA']
    genes = []

    s = 0
    while True:
        a = dna.find("TATA", s)
        if a < 0:
            break
        b = dna.find("TATA", a + 4)
        c = dna.find("ATG",  a + 4)
        if c < 0:
            break
        #print('c1', a, b, c)
        while c >= b and b != -1:
            a = b
            b = dna.find("TATA", a + 4)
            c = dna.find("ATG",  a + 4)
        pos = c+3
        e = 0
        slices = []
        total = 0
        while e == 0:
            new = ''
            gu = dna.find("GT", pos)
            ag = dna.find("AG", gu + 2)
            if gu < ag and gu != -1 and ag != -1 :
                stop = find_gene(dna[pos:gu])
                if stop == -1:
                    total += ag + 2 - gu
                    slices.append((gu, ag + 2, total))
                    rem = (gu-pos)%3
                    if dna[gu-rem:gu] + dna[ag + 2:ag + 5 - rem]  in stops:
                        e = ag+5-rem
                    else:
                        pos = ag + 2
                else:
                    e = stop + len(dna[:pos])
            else:
                e = find_gene(dna[pos:]) + len(dna[:pos])
                if e == len(dna[:pos]) - 1:
                    return []

        pos = c
        for s, f, _ in slices:
            new += dna[pos:s]
            pos = f
        new += dna[pos:e]

        genes.append((a, c, e, slices, new))
        s = e
    return genes


def test_genes():
    #print(find_genes(''))
    #print(find_genes('TATAATGAAAATAA')) #should not work
    #print(find_genes('TATAATGAAATAA'))
    print(find_genes('TATAATGAAATAA'*10))
    #print(find_genes('TATAATGAAAGTUUUUAGTAA'*3))
    #print(find_genes('TATAATGAAATGTUUUUAGAA'))
    #print(find_genes('TATAATGAAATGTUUUUAGAATATAATGAAAGTUUUUAGTAATATAATGAAATAA'))

if __name__ == "__main__":
    #test_genes()
    print(proteins('AAABBBCCC'))
