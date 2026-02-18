import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from split_text_nodes import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link

class TestSplitNodes(unittest.TestCase):
    def test_split_code_block(self):
        node = TextNode("This is text with a `code block` inside", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertListEqual([
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" inside", TextType.TEXT)
        ], new_nodes)

        html_node_one = text_node_to_html_node(new_nodes[0])
        html_node_two = text_node_to_html_node(new_nodes[1])
        html_node_three = text_node_to_html_node(new_nodes[2])
        
    def test_missing_delimiter(self):
        node = TextNode("This was suppose to be text with a **bolded word", TextType.TEXT)
        
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_split_with_no_postceding_text(self):
        node = TextNode("This is a text with a `code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual([
            TextNode("This is a text with a ", TextType.TEXT, None),
            TextNode("code block", TextType.CODE, None)
        ], new_nodes)

    def test_splitting_text_objs(self):
        node = TextNode("**I am a bolded sentence**", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(new_nodes[0], node)

    def test_multiple_delimiters(self):
        node = TextNode("I am text with a `code_block` an _italic_ word and a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)

        self.assertEqual(len(new_nodes), 7)
        
        self.assertListEqual([
            TextNode("I am text with a ",TextType.TEXT),
            TextNode("code_block",TextType.CODE),
            TextNode(" an ",TextType.TEXT),
            TextNode("italic",TextType.ITALIC),
            TextNode(" word and a ",TextType.TEXT),
            TextNode("bold",TextType.BOLD),
            TextNode(" word",TextType.TEXT)

        ],new_nodes)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
                "This is a text with a link [to youtube](https://www.youtube.com) and [to google](https://www.google.com)"
        )
        self.assertListEqual([("to youtube", "https://www.youtube.com"),("to google", "https://www.google.com")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual([
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
        ], new_nodes)

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [go to youtube](https://www.youtube.com) and another link [go to google](https://www.google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("go to youtube", TextType.LINK, "https://www.youtube.com"),
            TextNode(" and another link ", TextType.TEXT),
            TextNode("go to google", TextType.LINK, "https://www.google.com")
        ], new_nodes)

    def test_split_link_with_postceding_text(self):
        node = TextNode("This is a text with a link [go to google](https://www.google.com) and more text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
            TextNode("This is a text with a link ", TextType.TEXT),
            TextNode("go to google", TextType.LINK, "https://www.google.com"),
            TextNode(" and more text", TextType.TEXT)
        ], new_nodes)

    def test_split_link_and_image(self):
        node = TextNode(
                "This is a text with a link [go to google](https://www.google.com) and an image ![image](https://i.imgur.com/zjjcJKZ.png)",
                TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        new_nodes = split_nodes_link(new_nodes)

        self.assertListEqual([
            TextNode("This is a text with a link ", TextType.TEXT),
            TextNode("go to google", TextType.LINK, "https://www.google.com"),
            TextNode(" and an image ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ], new_nodes)

    def test_split_image_with_no_text(self):
        node = TextNode("![image](https://some_random_image.jpg)")
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("image",TextType.IMAGE, "https://some_random_image.jpg")], new_nodes)

