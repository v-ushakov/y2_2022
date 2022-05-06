import unittest
from biosynth import read_dna, find_genes, proteins
#from dna_paint import
from io import StringIO

class TestLetters(unittest.TestCase):


    def test_found(self):

        #self.assertEqual(False, read_dna("../DNA/test_dna_error"), False)
        self.assertEqual('ACTAGTCACAC', read_dna("../DNA/unchangeble"), 'ACTAGTCACAC')

    def test_gene_parsing(self):

        self.assertEqual(find_genes(''),               [], "No jeans case 1")
        self.assertEqual(find_genes('TAA'),            [], "No jeans case 2")
        self.assertEqual(find_genes('TATATAG'),        [], "No jeans case 3")
        self.assertEqual(find_genes('TATATAC'),        [], "No jeans case 4")
        self.assertEqual(find_genes('TATAATGAAAATAA'), [], "Unaligned stop")

        self.assertEqual(find_genes('TATAATGAAATAA'),  [(0, 4, 13, [], 'ATGAAATAA')], "Gene")
        self.assertEqual(find_genes('TATAATGAAATGTUUUUAGAA'), [(0, 4, 21, [(11, 19, 8)], 'ATGAAATAA')], "Gene with an exon")

    def test_protein_tripleting(self):
        self.assertEqual(proteins('AAABBBCCC'), ['AAA', 'BBB', 'CCC'], 'Gene splitting into triplets')

if __name__ == '__main__':
    unittest.main()

