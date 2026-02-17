from textnode import TextNode, TextType, text_node_to_html_node

def split_nodes_delimiter(current_nodes, delimiter, text_type):
    new_nodes = []
    
    for node in current_nodes:
        current_text_type = node.text_type
        text = node.text

        if current_text_type.value != "text":
            new_nodes.append(node)
       
        elif delimiter not in text:
            new_nodes.append(node)

        elif text.count(delimiter) % 2 != 0:
            raise ValueError("invalid markdown: missing delimiter")
        
        else:
            text1, extracted_type_text, text2  = text.split(delimiter)

            new_nodes.extend([
                TextNode(text1, current_text_type), 
                TextNode(extracted_type_text, text_type), 
                TextNode(text2, current_text_type)
                ])

    return new_nodes


