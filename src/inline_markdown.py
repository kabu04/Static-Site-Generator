from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)

import re

# turns nodes into potentionally multiple nodes split based on the delimeter
def split_nodes_delimiter(old_nodes, delimeter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        # do not split non TextNode types
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue

        # list of texts for each new node
        node_text = old_node.text.split(delimeter)

        # make sure delimiter has opening and closing delimiter
        if len(node_text) % 2 == 0:
            raise Exception("Invalid Markdown syntax: Matching closing delimiter not found")
        
        # if the old_node ends with delimiter then we have an empty "" as the last element due to split.
        # we need "" to check for valid closing delimiters. Afterwords we remove it, since it should not be a node.
        if old_node.text.endswith(delimeter):
            node_text = node_text[0:-1]

        # create one new node for each text
        for i in range(0, len(node_text)):
            if i % 2 == 0:
                new_nodes.append(TextNode(node_text[i], old_node.text_type))
            else:
                new_nodes.append(TextNode(node_text[i], text_type))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        
        image_tup = extract_markdown_images(old_node.text)

        # if no content then we leave it
        if len(image_tup) == 0:
            new_nodes.append(old_node)
            continue

        for i in range(0, len(image_tup)):
            # splits text
            if i == 0:
                text_from_image_tup = old_node.text.split(f"![{image_tup[0][0]}]({image_tup[0][1]})", 1)
            else:
                text_from_image_tup = text_from_image_tup[1].split(f"![{image_tup[i][0]}]({image_tup[i][1]})", 1)

            # only add if there was text preceding the image 
            if not (text_from_image_tup[0] == ""):
                new_nodes.append(TextNode(text_from_image_tup[0], text_type_text))

            # add the link text
            new_nodes.append(TextNode(image_tup[i][0], text_type_image, image_tup[i][1]))

            # if no text after image then on split we get ""
            if text_from_image_tup[1] == "": 
                break

        # add last remaining text
        if not (text_from_image_tup[1] == ""):
            new_nodes.append(TextNode(text_from_image_tup[1], text_type_text))
            
    
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue

        link_tup = extract_markdown_links(old_node.text)

        # if no content then we leave it
        if len(link_tup) == 0:
            new_nodes.append(old_node)
            continue

        for i in range(0, len(link_tup)):
            # splits text
            if i == 0:
                text_from_link_tup = old_node.text.split(f"[{link_tup[0][0]}]({link_tup[0][1]})", 1)
            else:
                text_from_link_tup = text_from_link_tup[1].split(f"[{link_tup[i][0]}]({link_tup[i][1]})", 1)

            # only add if there was text preceding the image 
            if not (text_from_link_tup[0] == ""):
                new_nodes.append(TextNode(text_from_link_tup[0], text_type_text))

            # add the link text
            new_nodes.append(TextNode(link_tup[i][0], text_type_link, link_tup[i][1]))

            # if no text after image then on split we get "" and were done
            if text_from_link_tup[1] == "": 
                break

        # add last remaining text
        if not (text_from_link_tup[1] == ""):
            new_nodes.append(TextNode(text_from_link_tup[1], text_type_text))

    return new_nodes


def extract_markdown_images(text):
    # captures [image](url) and places them into a tuple 
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches

def text_to_textnodes(text):
    new_nodes = split_nodes_delimiter([TextNode(text, text_type_text, None)], "**", text_type_bold)
    new_nodes = split_nodes_delimiter(new_nodes, "*", text_type_italic)
    new_nodes = split_nodes_delimiter(new_nodes, "`", text_type_code)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes