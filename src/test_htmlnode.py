import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_prop(self):
        test_prop = ' href="http://random.com"'
        html_node = HTMLNode(tag="a", value="Some link text here", children=None, props={"href": "http://random.com"})
        
        node_prop = html_node.props_to_html()

        self.assertEqual(node_prop, test_prop)
    
    def test_multiple_props(self):
        test_prop = ' href="http://random.com" target="_blank"'

        html_node = HTMLNode(
            tag="a", 
            value="Some link text here", 
            children=None, 
            props={"href": "http://random.com", "target": "_blank"}
        )

        node_prop = html_node.props_to_html()

        self.assertEqual(node_prop, test_prop)

    def test_parent_child_props(self):
        test_prop = ' target="_blank"'

        child_node = HTMLNode(tag="a", value="Some link text here", children=None, props={"target": "_blank"})
        parent_node = HTMLNode(tag="div", value=None, children=[child_node], props=None)
        
        child_prop = parent_node.children[0].props_to_html()
        parent_prop = parent_node.props_to_html()

        self.assertEqual(child_prop, test_prop)
        self.assertEqual(parent_prop, None)












