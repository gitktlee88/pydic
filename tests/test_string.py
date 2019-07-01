import unittest

# (v36) c:\virtualenv\v36\pydic>python tests\test_string.py

# or

# (v36) c:\virtualenv\v36\pydic>pip install nose2
# (v36) c:\virtualenv\v36\pydic>python -m nose2

# nose2 will try to discover all test scripts named test*.py
# and test cases inheriting from unittest.TestCase in your current directory:
# including subdirectory.

class TestStringMethods(unittest.TestCase):
      def test_lstrip(self):
              self.assertEqual('   hello '.lstrip(),'hello ')
      def test_isupper(self):
              self.assertTrue('HELLO'.isupper())
              self.assertFalse('HELlO'.isupper())
      def test_split(self):
              self.assertEqual('Hello World'.split(),['Hello','World'])
              with self.assertRaises(TypeError):
                      s.split(2)

if __name__=='__main__':
      unittest.main()
