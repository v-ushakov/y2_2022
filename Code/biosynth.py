import re

def proteins(seq):
    prot = []
    start = 0
    for a in range(3, len(seq)+1,3):
        prot.append(seq[start:a])
        start = a
    return prot

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
re_tatac  = re.compile('TATA|ATG')              # TATA box or start codon
re_intron = re.compile('GT.*?AG')
re_stop   = re.compile('(...)*?(TAA|TAG|TGA)')  # match, don't search

def next_gene(dna, pos):
    m = re_tata.search(dna, pos)
    while m.group(0) == 'TATA':
        tata = m.start()
        m = re_tatac.search(dna, tata + 4)
    start = m.start()

    print(tata, start)

    introns = []
    total = 0                                           # total size of introns
    # 0. pos is the position after ATG
    pos = start + 3
    while True:
        # 1. find next possible intron GU...AG from 'pos'
        intron = re_intron.search(dna, pos)
        print('intron(%u):' % pos, intron)
        # 2. find an aligned stop codon from 'pos' to GU or anywhere if no GU
        stop = re_stop.match(dna, pos, intron.start() if intron else len(dna))
        print('stop(%u):' % pos, stop)
        # 3. if found: append a gene and continue the main loop
        if stop:
            return (tata, start, stop.end(), introns)
        # 4. append [GU:AG+2] into intron list
        gu, ag = intron.span()
        total += ag - gu
        introns.append((gu, ag, total))
        # 5. [GU//3*3:GU] + [AG:AG+2]: check whether it starts with a stop codon
        rem = (gu - pos) % 3
        pos = ag + 3 - rem
        print('gu---ag=%u---%u; rem=%u, new pos=%u' % (gu, ag, rem, pos))
        # 6. if so append a gene and continue the main loop
        if re_stop.match(dna[gu-rem:gu] + dna[ag:pos]):
            return (tata, start, pos, introns)
        # 7. align 'pos' to the next exon and repeat


def splice_gene(dna, gene):
    tata, start, end, introns = gene
    pos = start
    spliced = ''
    for s, e, _ in introns:
        spliced += dna[pos:s]
        pos = e
    spliced += dna[pos:end]
    return tata, start, end, introns, spliced


def find_genes(dna):
    print('find_genes(%s)' % dna)
    genes = []
    pos = 0
    try:
        while True:
            g = next_gene(dna, pos)
            genes.append(splice_gene(dna, g))
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
        'TATAATGTAA',
        'TATAATGAAAATAA',
        'TATAATGAAATAA'*10,
        'CACATATAAAAAAAAAAATATAATGTAA',
        'TAGTATAACTTCACACTGATGCCACCCCCAGGAGUTTAGTAG',
    #              111111111122222222223333333333444444444455555555556666666666
    #    0123456789012345678901234567890123456789012345678901234567890123456789
    ]
    for dna in dnas:
        print(find_genes(dna))



if __name__ == "__main__":
    test_genes()
    print(proteins('AAABBBCCC'))
