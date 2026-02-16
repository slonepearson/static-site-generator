import unittest

from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_types_not_eq(self):
        node = TextNode("I am alt text", TextType.IMAGE, "someimgurl.com")
        node2 = TextNode("I am a link", TextType.LINK, "http://somerandomelink.com")
        self.assertNotEqual(node, node2)
    
    def test_missing_url(self):
        node = TextNode("I have a url link", TextType.LINK, "https://bootdotdev.com")
        node2 = TextNode("I don't have a url link", TextType.LINK)
        self.assertNotEqual(node, node2)
    
    def test_content_not_eq(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_types_default(self):
        node = TextNode("I was meant to be an img node but ended up a text node")
        node2 = TextNode("I was meant to be an img node but ended up a text node")
        self.assertEqual(node, node2)

    def test_text_to_html(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), "This is a text node")

    def test_type_image_to_html(self):
        node = TextNode("Google.com logo", TextType.IMAGE, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props_to_html(), ' src="https://www.google.com" alt="Google.com logo"')
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.to_html(), '<img src="https://www.google.com" alt="Google.com logo"></img>')

if __name__ == "__main__":
    unittest.main()
