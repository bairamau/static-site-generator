import unittest
from main import extract_title

class MainTest(unittest.TestCase):
    def test_extract_title(self):
        md = '''# What is up my peeps

It's a beautiful day, ain't it?
'''
        self.assertEqual(extract_title(md), 'What is up my peeps')

        md = 'Irrelevant'
        self.assertRaises(Exception, extract_title, md)
