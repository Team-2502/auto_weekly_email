import unittest

from autoweeklyemail.utils import get_captains, Captain


def fun(x):
    return x + 1


class UtilsTest(unittest.TestCase):
    def test_get_captains(self):
        captains = get_captains()
        self.assertGreater(len(captains), 0)

    def test_captains_tostr(self):
        captain = Captain("Grant", "grant@yahoo.com", "(555) 555-5555")
        self.assertEqual(str(captain), "Grant: [grant@yahoo.com](mailto:grant@yahoo.com), (555) 555-5555")


if __name__ == '__main__':
    unittest.main()
