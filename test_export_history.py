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


    def test_is_domain_whitelisted_with_date(self):
        whitelist_domains = {"example.com": "2023-01-01"}
        self.assertTrue(export_history.is_domain_whitelisted("example.com", whitelist_domains,"2023-02-02"))

        self.assertFalse(export_history.is_domain_whitelisted("example.com", whitelist_domains,"2020-02-02"))


    def test_is_domain_whitelisted_with__future_date(self):
        whitelist_domains = {"example.com": "2024-01-01"}
        self.assertFalse(export_history.is_domain_whitelisted("example.com", whitelist_domains,"2023-02-02"))

    def test_is_domain_whitelisted_without_date(self):
        whitelist_domains = {"example.com": None}
        self.assertTrue(export_history.is_domain_whitelisted("example.com", whitelist_domains,"2023-02-02"))



if __name__=="__main__":
    unittest.main()
