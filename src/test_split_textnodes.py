import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from split_text_nodes import split_nodes_delimiter

class TestSplitTextNodes(unittest.TestCase):
    def test_split_code_block(self):
        node = TextNode("This is text with a `code block` inside", TextType.TEXT)
        node_one,node_two,node_three = split_nodes_delimiter([node], "`", TextType.CODE)
        
        #Test series 1
        self.assertEqual(node_one.text_type, TextType.TEXT)
        self.assertEqual(node_two.text_type, TextType.CODE)
        self.assertEqual(node_three.text_type, TextType.TEXT)
        self.assertEqual(node_one.text, "This is text with a ")
        self.assertEqual(node_two.text, "code block")
        self.assertEqual(node_three.text, " inside")

        html_node_one = text_node_to_html_node(node_one)
        html_node_two = text_node_to_html_node(node_two)
        html_node_three = text_node_to_html_node(node_three)
        
        #Test series 2
        self.assertEqual(html_node_one.to_html(), "This is text with a ")
        self.assertEqual(html_node_two.to_html(), "<code>code block</code>")
        self.assertEqual(html_node_three.to_html(), " inside")
        
    def test_missing_delimiter(self):
        node = TextNode("This was suppose to be text with a **bolded word", TextType.TEXT)
        
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_splitting_text_objs(self):
        node = TextNode("**I am a bolded sentence**", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(new_nodes[0], node)

    def test_multiple_delimiters(self):
        node = TextNode("I am text with a `code_block`, an _italic_ word and a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)

        self.assertEqual(len(new_nodes), 7)
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[5].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[6].text_type, TextType.TEXT)

        code_html_node = text_node_to_html_node(new_nodes[1])
        italic_html_node = text_node_to_html_node(new_nodes[3])
        bold_html_node = text_node_to_html_node(new_nodes[5])

        self.assertEqual(code_html_node.to_html(), "<code>code_block</code>")
        self.assertEqual(italic_html_node.to_html(), "<i>italic</i>")
        self.assertEqual(bold_html_node.to_html(), "<b>bold</b>")


