


def main():
    dna = ""
    rna = ""
    with open("dna_sequence") as f:
        a = f.readline().strip().upper()
        while a != "":
            dna += a
            a = f.readline().strip().upper()
    b = dna.find("TATA")
    for i in dna[(b+5)::]:
        if i == "A":
            rna += "U"
        if i == "T":
            rna += "A"
        if i == "C":
            rna += "G"
        if i == "G":
            rna += "C"

    print(rna[:10])

main()




