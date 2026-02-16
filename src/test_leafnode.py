import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_anchor_with_prop(self):
        node = LeafNode("a", "Click me!", {"href":"https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_self_closing(self):
        node = LeafNode("img","",{"src":"https://google.com","alt":"google.com logo"})
        self.assertEqual(node.to_html(), '<img src="https://google.com" alt="google.com logo"></img>')
