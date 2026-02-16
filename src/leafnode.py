from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value

        props = self.props_to_html() 

        return f"<{self.tag}{props if props is not None else ''}>{self.value}</{self.tag}>"

    def __repr__(self):
        return ( 
            f"""
            LeafNode(
                TAG = {self.tag}, 
                ATTRIBUTES = {self.props_to_html()}, 
                VALUE = {self.value}, 
            )
            """
        )

