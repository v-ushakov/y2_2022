import unittest
from biosynth import reading_letters
from io import StringIO

class TestLetters(unittest.TestCase):


    def test_found(self):

        self.assertEqual(False, reading_letters("test_dna_error"), False)
        self.assertEqual('ACTAGTC', reading_letters("test_dna"), 'ACTAGTC')



