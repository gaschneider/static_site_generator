import unittest
from extracttitle import extract_title

def validate_links_and_expected_result(links, expected_result):
    if len(links) != len(expected_result):
        return False
    
    for i in range(0, len(links)):
        link_alt, link_url = links[i]
        expected_alt, expected_url = expected_result[i]
        if link_alt != expected_alt or link_url != expected_url:
            return False

    return True

class TestExtractTitle(unittest.TestCase):
    def test_title(self):
        title = extract_title(
"""# Hello, I am title   """
)
        self.assertEqual(title, "Hello, I am title")

    def test_real_title(self):
        title = extract_title(
"""## Hello, I am title   
# But I am the real title"""
)
        self.assertEqual(title, "But I am the real title")

    def test_no_title(self):
        self.assertRaises(Exception, extract_title, """####### Not a real title at all   """)

if __name__ == "__main__":
    unittest.main()