from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type = TextType.TEXT, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        if (
            self.text == other.text 
            and self.text_type == other.text_type
            and self.url == other.url
            ):
            return True
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
    
    value = text_node.text
    text_type = text_node.text_type

    match text_type.value:
        case "text":
            return LeafNode(None, value)
        case "bold":
            return LeafNode("b", value)
        case "italic":
            return LeafNode("i", value)
        case "code":
            return LeafNode("code", value)
        case "link":
            return LeafNode("a", value, {"href":text_node.url})
        case "image":
            return LeafNode("img", "", {"src":text_node.url, "alt":value})
        case _:
            raise Exception("Not a supported inline element")
