
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props:
            attributes = "".join([f' {key}="{self.props[key]}"' for key in self.props if self.props])
            return attributes
        return None 
    
    def __repr__(self):
        return (
                f"""
            HTMLNode(
                TAG = {self.tag}, 
                ATTRIBUTES = {self.props_to_html()}, 
                VALUE = {self.value}, 
                CHILDREN = {self.children}
            )
            """
        )


