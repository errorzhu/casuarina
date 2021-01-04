import unittest


class MyclassTest(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_add(self):
        # ret = self.clac.add()
        # self.assertEqual(ret, 9)
        pass

    def test_sub(self):
        pass
        # ret = self.clac.sub()
        # self.assertEqual(ret, -1)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(MyclassTest('test_add'))
    suite.addTest(MyclassTest('test_sub'))

    runner = unittest.TextTestRunner()
    runner.run(suite)
