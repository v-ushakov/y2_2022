import re

def find_slice(seq):
    slices = []
    new = ''
    gu = seq.find("GT")
    ag = seq.find("AG")
    while gu >= 0 and ag >=0:
        print("GU is ", gu, "UC is ", ag )
        if gu < ag:
            slices.append([gu, ag+1])
            a = seq[gu: ag+2]
            print(new, a)
            gu = seq.find("GT", ag + 1)
            ag = seq.find("AG", ag + 1)

    for a in range(len(slices)):
        if a == 0:
            new += seq[:slices[a][0]]
        else:
            new += seq[slices[a-1][1]:slices[a][0]]

    return new, slices, seq

def proteins(seq):
    prot = []
    start = 0
    for a in range(3, len(seq)+1,3):
        prot.append(seq[start:a])
        start = a
    return prot

        #if a%3 == 0:






def reading_letters(fil):
    dna = ''
    with open(fil) as f:
        a = f.readline().strip().upper()
        while a != "":
            dna += a
            a = f.readline().strip().upper()
    for i in dna:
        if not i in ["A", "T", "C", "G"]:
            print("There is a unacceptable letter")
            return False
    #print("dna is :", dna)
    return dna

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
        while e == 0:
            new = ''
            gu = dna.find("GT", pos)
            ag = dna.find("AG", gu + 2)
            if gu < ag and gu != -1 and ag != -1 :
                stop = find_gene(dna[pos:gu])
                if stop == -1:
                    slices.append([gu, ag + 2])
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
        for (s, f) in slices:
            new += dna[pos:s]
            pos = f
        new += dna[pos:e]

        genes.append((a, c, e, slices, new))
        s = e
    return genes

def main():
    rna = ""
    fil = "test_dna_error"#"dna_sequence"
    dna = reading_letters(fil)
    if dna != False:
        DNA = find_genes(dna)
        print(DNA)
        for i in DNA:
            print(dna[(i[0]): (i[2])])
            print(dna[(i[1]): (i[2])])

        print(rna)
    else:
        print("Error in reading file")



def test_genes():
    #print(find_genes(''))
    #print(find_genes('TATAATGAAAATAA')) #should not work
    #print(find_genes('TATAATGAAATAA'))
    print(find_genes('TATAATGAAATAA'*10))
    #print(find_genes('TATAATGAAAGTUUUUAGTAA'*3))
    #print(find_genes('TATAATGAAATGTUUUUAGAA'))
    #print(find_genes('TATAATGAAATGTUUUUAGAATATAATGAAAGTUUUUAGTAATATAATGAAATAA'))

if __name__ == "__main__":
    #print(find_slice("AAGTUUUAGAA"))
    #test_genes()
    print(proteins('AAABBBCCC'))





