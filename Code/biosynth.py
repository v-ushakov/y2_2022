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
    return dna

def gene(dna):
    #stops = ["ATT", "ATC", "ACT"]
    m = re.search(("(...)*ATT|(...)*ATC|(...)*ACT"),dna)
    #print("m is in ",m.span()[1])
    return m.span()[1]




#def finding_genes(dna):











def main():
    rna = ""
    fil = "test_dna"#"dna_sequence"
    dna = reading_letters(fil)
    a = dna.find("TATA")
    b = dna.find("TATA", a + 3)
    c = dna.find("TAC", a+ 3)
    #print(a, b, c)
    while c >= b and b != -1:
        a = b
        b = dna.find("TATA", a + 3)
        c = dna.find("TAC", a + 3)
        #print(b, c)

    print("the gene starts here ",a, ",", c) # a is the TATA place, C is the start codone place

    e = gene(dna[c:]) + len (dna[:c])
    #print(dna)
    print(dna[c:e])


    #if dna != False:
     #   print("len of the dna:",len(dna))
    #    b = dna.find("TATA")
    #    for i in dna[(b+4)::]:
    #        if i == "A":
    #            rna += "U"
    #        if i == "T":
    #            rna += "A"
    #        if i == "C":
    #            rna += "G"
    #        if i == "G":
    #            rna += "C"



    print(rna) 
    #print(b)
    #print("len of rna:", len(rna))


if __name__ == "__main__":
    main()




