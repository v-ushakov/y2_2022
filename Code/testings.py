import unittest
from biosynth import reading_letters, find_genes
#from dna_paint import
from io import StringIO

class TestLetters(unittest.TestCase):


    def test_found(self):

        self.assertEqual(False, reading_letters("test_dna_error"), False)
        self.assertEqual('ACTAGTCACAC', reading_letters("unchangeble"), 'ACTAGTCACAC')

    def test_gene_parsing(self):

        self.assertEqual(find_genes(''),               [], "No jeans case 1")
        self.assertEqual(find_genes('TAA'),            [], "No jeans case 2")
        self.assertEqual(find_genes('TATATAG'),        [], "No jeans case 3")
        self.assertEqual(find_genes('TATATAC'),        [], "No jeans case 4")
        self.assertEqual(find_genes('TATAATGAAAATAA'), [], "Unaligned stop")

        self.assertEqual(find_genes('TATAATGAAATAA'),  [(0, 4, 13, [])], "Gene")
        self.assertEqual(find_genes('TATAATGAAATGTUUUUAGAA'), [(0, 4, 21, [[11, 19]])], "Gene with an exon")



if __name__ == '__main__':
    unittest.main()

