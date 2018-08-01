import unittest
import app

class appUnitTest(unittest.TestCase):

    '''
    <summary>Basic unit test for index function within app.py</summary>
    <asserts>assertEqual; String comparison<asserts>
    <returns>Success if return string is: Hello World!</returns>
    '''
    def testIndex(self):
        self.assertEqual(app.index(),'Hello World!')

'''
<summary>Main Function that runs unit tests</summary>
'''
if __name__ == '__main__':
    unittest.main()