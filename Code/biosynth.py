import re


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
    m = re.match(("(...)*?A(TT|TC|CT)"), dna)
    if m == None:
        return -1
    #print("m is in", m.span()[1])
    return m.span()[1]

def find_genes(dna):
    genes = []
    s = 0
    while True:
        a = dna.find("TATA", s)
        if a < 0:
            break
        b = dna.find("TATA", a + 3)
        c = dna.find("TAC", a + 3)
        if c < 0:
            break
        #print('c1', a, b, c)
        while c >= b and b != -1:
            a = b
            b = dna.find("TATA", a + 3)
            c = dna.find("TAC", a + 3)
            #print('c2', a, b, c)
        e = find_gene(dna[c:]) + len (dna[:c])
        if e == len (dna[:c]) - 1:
            #print("There is no gene found")
            break
        genes.append((a, c, e))
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
    tata = []
    for a, b, c in find_genes('TATATACAAAATT'*10):
        tata.append(a)
    print("tata is", tata)
    print(find_genes('TATATACAAAAATT'))
    print(find_genes('TATATACAAAATT'*10))



if __name__ == "__main__":
    test_genes()




