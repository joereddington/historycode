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


    def test_why_is_this_not_working(self):
        row="('2025-05-26 08:40:50', 'https://www.theguardian.com/business/2025/may/26/taxpayer-loss-natwest-disgraced-ex-boss-pension', 'Taxpayers set for £10bn loss on NatWest as disgraced ex-boss takes £600k-a-year pension | Fred Goodwin | The Guardian', 1748248850912335)"
        import ast 
        row=ast.literal_eval(row)
        print(row)
        print("XXX")
        whitelist=export_history.get_whitelist_domains()
        print(export_history.process_row(row, whitelist,False, {}, True))


if __name__=="__main__":
    unittest.main()
