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
        self.assertTrue(export_history.is_domain_whitelisted("example.com", whitelist_domains))

    def test_is_domain_whitelisted_with__future_date(self):
        whitelist_domains = {"example.com": "2024-01-01"}
        self.assertFalse(export_history.is_domain_whitelisted("example.com", whitelist_domains))
    def test_is_domain_whitelisted_without_date(self):
        whitelist_domains = {"example.com": None}
        self.assertFalse(export_history.is_domain_whitelisted("example.com", whitelist_domains))

    def test_domain_filter(self):
        # TODO - this needs to be related to a whitelist
        matches = [("2023-11-15 10:46:50", "https://example.com/path1", "Title1"),
                   ("2023-11-15 10:46:50", "https://example.com/path2", "Title2"),
                   ("2023-11-15 10:48:50", "https://example2.com/path3", "Title3")]
        result = export_history.domain_filter(matches, use_blacklist=False, html=True)
        expected_result = [("2023-11-15 10:46:50", 'example.com'), ("2023-11-15 10:48:50", 'example2.com')]
        self.assertEqual(result, expected_result)




if __name__=="__main__":
    unittest.main()
