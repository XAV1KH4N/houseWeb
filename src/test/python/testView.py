import unittest
from src.main.python.View import View, ViewingError

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.view = View()
        self.view.reset()

    def tearDown(self):
        self.view.close()

    def testViewCount(self):
        self.assertEquals(0, self.view.viewCount())

    def testAddViewing(self):
        self.view.addViewing("2022-02-07", "14:30")
        self.assertEqual(1, self.view.viewCount())

    def testAddViewingInts(self):
        self.view.addViewing("2022-2-8", "11:25")
        self.assertEqual(1, self.view.viewCount())

    def testViewFuture(self):
        self.view.addViewing("2021-01-29", "14:25")
        self.view.addViewing("2022-02-18", "11:25")
        self.view.addViewing("2022-02-19", "12:45")
        self.assertEqual(3, self.view.viewCount())
        self.assertEqual([(2, '2022-02-18', '11:25'), (3, '2022-02-19', '12:45')], self.view.getViewings())

if __name__ == '__main__':
    unittest.main()
