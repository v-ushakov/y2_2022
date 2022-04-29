import unittest
from biosynth import reading_letters
#from dna_paint import
from io import StringIO

class TestLetters(unittest.TestCase):


    def test_found(self):

        self.assertEqual(False, reading_letters("test_dna_error"), False)
        self.assertEqual('ACTAGTCACAC', reading_letters("unchangeble"), 'ACTAGTCACAC')

if __name__ == '__main-__':
    unittest.main()

