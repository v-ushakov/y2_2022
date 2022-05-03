import re

def find_slice(seq):
    slices = []
    new = seq
    gu = seq.find("CA")
    ag = seq.find("TC")
    while gu >= 0 and ag >=0:
        print("GU is ", gu, "UC is ", ag )
        if gu < ag:
            slices.append([gu, ag+1])
            a = seq[gu: ag+2]
            print(new, a)
            #new =
            gu = seq.find("CA", ag + 1)
            ag = seq.find("TC", ag + 1)

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


# complementary pairs: A-T/U G-C

re_tata   = re.compile('TATA')                  # TATA box on 3'->5' strand
re_tatac  = re.compile('TATA|TAC')              # TATA box or start codon
re_intron = re.compile('GU.*AG')
re_stop   = re.compile('(...)*?(ATT|ATC|ACT)')  # match, don't search

def next_gene(dna, pos):
    m = re_tata.search(dna, pos)
    while m.group(0) == 'TATA':
        tata = m.start()
        m = re_tatac.search(dna, tata + 4)
    tac = m.start()

    print(tata, tac)

    introns = []
    # 0. pos is the position after TAC
    pos = tac + 3
    while True:
        # 1. find next possible intron GU...AG from 'pos'
        intron = re_intron.search(dna, pos)
        print('intron(%u):' % pos, intron)
        # 2. find an aligned stop codon from 'pos' to GU or anywhere if no GU
        stop = re_stop.match(dna, pos, intron.start() if intron else len(dna))
        print('stop(%u):' % pos, stop)
        # 3. if found: append a gene and continue the main loop
        if stop:
            return (tata, tac, stop.end(), introns)
        # 4. append [GU:AG+2] into intron list
        introns.append(intron.span())
        # 5. [GU//3*3:GU] + [AG:AG+2]: check whether it starts with a stop codon
        gu, ag = intron.span()
        rem = (gu - pos) % 3
        pos = ag + 3 - rem
        print('gu---ag=%u---%u; rem=%u, new pos=%u' % (gu, ag, rem, pos))
        # 6. if so append a gene and continue the main loop
        if re_stop.match(dna[gu-rem:gu] + dna[ag:pos]):
            return (tata, tac, pos, introns)
        # 7. align 'pos' to the next exon and repeat


def find_genes(dna):
    print('find_genes(%s)' % dna)
    genes = []
    pos = 0
    try:
        while True:
            g = next_gene(dna, pos)
            genes.append(g)
            pos = g[2]
    except AttributeError as e:
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
    dnas = [
        #'TATATACATT',
        #'TATATACAAAAATT',
        #'TATATACAAAATT'*10,
        #'CACATATAAAAAAAAAAATATATACATT',
        'ATCTATAACTTCACACTGTACCCACCCCCAGGAGUTTAGATC',
    #              111111111122222222223333333333444444444455555555556666666666
    #    0123456789012345678901234567890123456789012345678901234567890123456789
    ]
    for dna in dnas:
        print(find_genes(dna))



if __name__ == "__main__":
    #print(find_slice("ACAPATC"))
    test_genes()
    print(proteins('AAABBBCCC'))
