import re
from textnode import TextNode, TextType, text_node_to_html_node

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def split_nodes_delimiter(current_nodes, delimiter, text_type):
    new_nodes = []
    
    for node in current_nodes:
        current_text_type = node.text_type
        text = node.text

        if current_text_type.value != "text":
            new_nodes.append(node)
            continue

        if delimiter not in text:
            new_nodes.append(node)
            continue

        if text.count(delimiter) % 2 != 0:
            raise ValueError("invalid markdown: missing delimiter") 
        
        sections = text.split(delimiter)
        if not sections[2]:
            new_nodes.extend([
                TextNode(sections[0],current_text_type),
                TextNode(sections[1],text_type)
            ])
        else:
            new_nodes.extend([
                TextNode(sections[0], current_text_type),
                TextNode(sections[1], text_type),
                TextNode(sections[2], current_text_type)
            ])
            
    return new_nodes

def split_nodes_image(current_nodes):
    new_nodes = []

    for node in current_nodes:
        current_text_type = node.text_type
        text = node.text
        
        if current_text_type.value != "text":
            new_nodes.append(node)
            continue

        if (extracted_images := extract_markdown_images(text)):
            for alt_text, url in extracted_images:
                delimiter = f"![{alt_text}]({url})"
                sections = text.split(delimiter,1)

                if sections[0]:
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))

                new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
                text = sections[1]
 
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def split_nodes_link(current_nodes):
    new_nodes = []

    for node in current_nodes:
        current_text_type = node.text_type
        text = node.text
        
        if current_text_type.value != "text":
            new_nodes.append(node)
            continue
 
        if (extracted_links := extract_markdown_links(text)):
            for link_text, url in extracted_links:
                delimiter = f"[{link_text}]({url})"
                sections = text.split(delimiter,1)

                if sections[0]:
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))

                new_nodes.append(TextNode(link_text, TextType.LINK, url))
                text = sections[1]
            
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

