import unittest
from utils import extract_markdown_links

def validate_links_and_expected_result(links, expected_result):
    if len(links) != len(expected_result):
        return False
    
    for i in range(0, len(links)):
        link_alt, link_url = links[i]
        expected_alt, expected_url = expected_result[i]
        if link_alt != expected_alt or link_url != expected_url:
            return False

    return True

class TestExtractLinks(unittest.TestCase):
    def test_bootdev_example(self):
        links = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        expected_result = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertTrue(validate_links_and_expected_result(links, expected_result))

    def test_no_links(self):
        links = extract_markdown_links("This text has no link")
        expected_result = []
        self.assertTrue(validate_links_and_expected_result(links, expected_result))

    def test_image_but_no_link(self):
        links = extract_markdown_links("This text has no link but does have image ![rick roll](https://i.imgur.com/aKaOqIh.gif)")
        expected_result = []
        self.assertTrue(validate_links_and_expected_result(links, expected_result))

if __name__ == "__main__":
    unittest.main()