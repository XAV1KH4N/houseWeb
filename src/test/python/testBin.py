import unittest

from src.main.python.Bin import Bin


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.bin = Bin()

    def testCalcNext(self):
        bins = self.bin.nextBins()
        print(bins)


if __name__ == '__main__':
    unittest.main()
