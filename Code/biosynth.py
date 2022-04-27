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


def main():
    rna = ""
    fil = "dna_sequence"
    dna = reading_letters(fil)
    if dna != False:
        print("len of the dna:",len(dna))
        b = dna.find("TATA")
        for i in dna[(b+4)::]:
            if i == "A":
                rna += "U"
            if i == "T":
                rna += "A"
            if i == "C":
                rna += "G"
            if i == "G":
                rna += "C"



    print(rna)
    print("len of rna:", len(rna))

if __name__ == "__main__":
    main()




