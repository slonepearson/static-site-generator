from htmlnode import HTMLNode
from leafnode import LeafNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("HTML parent nodes need a tag")
        if self.children is None:
            raise ValueError("HTML parent nodes need to have children")
        
        child_html = ""
        for child in self.children:
            child_html += child.to_html()
        
        props = self.props_to_html()
        
        return f"<{self.tag}{props if props is not None else ''}>{child_html}</{self.tag}>"




