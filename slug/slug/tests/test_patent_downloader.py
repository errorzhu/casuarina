import unittest
import slug.patent_downloader as downloader


class PatentDownloadTest(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_parse_patent_number(self):
        ret = downloader.parse_patent_number("BE677033A")
        expect = ("BE", "677033", "A")
        self.assertEqual(ret, expect)

        ret2 = downloader.parse_patent_number("DE2023447A1")
        expect2 = ("DE", "2023447", "A1")
        self.assertEqual(ret2, expect2)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(PatentDownloadTest('test_add'))
    suite.addTest(PatentDownloadTest('test_sub'))

    runner = unittest.TextTestRunner()
    runner.run(suite)
