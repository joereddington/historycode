from unittest import TestCase
import unittest
import export_history



class historyTest(TestCase):


    def test_domain_finder(self):
        dom=export_history.get_domain("file:///Users/joe/Downloads/Geodesic%20Sphere.pdf")
        self.assertEqual(dom,"Local file")

    def test_domain_finder2(self):
        dom=export_history.get_domain("https://chat.openai.com/?model=text-davinci-002-render-sha")
        self.assertEqual(dom,"chat.openai.com")






if __name__=="__main__":
    unittest.main()
