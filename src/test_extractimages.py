import unittest
from utils import extract_markdown_images

def validate_images_and_expected_result(images, expected_result):
    if len(images) != len(expected_result):
        return False
    
    for i in range(0, len(images)):
        image_alt, image_url = images[i]
        expected_alt, expected_url = expected_result[i]
        if image_alt != expected_alt or image_url != expected_url:
            return False

    return True

class TestExtractImages(unittest.TestCase):
    def test_bootdev_example(self):
        images = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        expected_result = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertTrue(validate_images_and_expected_result(images, expected_result))

    def test_no_images(self):
        images = extract_markdown_images("This text has no image")
        expected_result = []
        self.assertTrue(validate_images_and_expected_result(images, expected_result))

    def test_link_but_no_image(self):
        images = extract_markdown_images("This text has no image [rick roll](https://i.imgur.com/aKaOqIh.gif)")
        expected_result = []
        self.assertTrue(validate_images_and_expected_result(images, expected_result))

if __name__ == "__main__":
    unittest.main()