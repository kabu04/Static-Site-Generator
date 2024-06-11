block_type_paragraph = "paragraph"
block_type_heading= "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"

import re

from htmlnode import (
    ParentNode, 
)

from inline_markdown import (
    text_to_textnodes
)

from textnode import (
    text_node_to_html_node
)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    root_children = []
    for block in blocks:
        block_node = block_to_html_node(block)
        root_children.append(block_node)

    root = ParentNode("div", root_children)
    return root

def block_to_html_node(block):
    block_type = block_to_block_type(block)

    if block_type == block_type_quote:
        return blockquote_to_html(block)
    if block_type == block_type_unordered_list:
        return unordered_list_to_html(block)
    if block_type == block_type_ordered_list:
        return ordered_list_to_html(block)
    if block_type == block_type_code:
        return code_to_html(block)
    if block_type == block_type_heading:
        return heading_to_html(block)
    if block_type == block_type_paragraph:
        return paragraph_to_html(block)

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    trimmed_blocks = []
    for block in blocks:
        if block != '':
            trimmed_blocks.append(block.strip())
    return trimmed_blocks

def block_to_block_type(block):
    # heading : 1-6 # followed by space then text
    match = re.match(r"^#{1,6} \w+", block)
    if match != None:
        return block_type_heading
    # code : ``` 3 backticks ends with 3 backticks
    match = re.match(r"^```", block[0:3])
    matches_end = re.match(r"```$", block[-3:len(block)])
    if match != None and matches_end != None:
        return block_type_code

    # quote :every line starts with >
    block_lines = block.split("\n")
    all_lines_match = True
    for line in block_lines:
        if re.match(r"^>", line) == None:
            all_lines_match = False
    if all_lines_match:
        return block_type_quote

    # unordered list: every line starts with * or - followed by space 
    block_lines = block.split("\n")
    all_lines_match = True
    for line in block_lines:
        if re.match(r"^(\*|-) ", line) == None:
            all_lines_match = False
    if all_lines_match:
        return block_type_unordered_list
    
    # every line starts with a number followed by . then a space
    # increment by 1 at each line
    block_lines = block.split("\n")
    all_lines_match = True
    prev = None
    for line in block_lines:
        match = re.match(r"^([0-9]+)\. ", line)
        # if no match found or list is not incrementing by one at each line 
        # then not ordered list.
        if match == None or (prev != None and int(match.group(1)) != prev + 1):
            all_lines_match = False
        if match != None:
            prev = int(match.group(1))
    if all_lines_match:
        return block_type_ordered_list

    return block_type_paragraph

def heading_num(block):
    if block.startswith("######"):
        return "h6"
    if block.startswith("#####"):
        return "h5"
    if block.startswith("####"):
        return "h4"
    if block.startswith("###"):
        return "h3"
    if block.startswith("##"):
        return "h2"
    if block.startswith("#"):
        return "h1"
    
def text_nodes_to_html_nodes(text_nodes):
    children = []
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children

def blockquote_to_html(block):
    block_lines = block.split("\n")
    # get rid of > at the start of every line
    # and whitespaces
    filtered_lines = []
    for line in block_lines:
        filtered_lines.append(line.lstrip(">").strip())
    text_nodes = text_to_textnodes(" ".join(filtered_lines))
    children = text_nodes_to_html_nodes(text_nodes)
    return ParentNode("blockquote", children)

def unordered_list_to_html(block):
    block_lines = block.split("\n")
    # get rid of * or - followed by space at the start of every line
    # and whitespaces
    filtered_lines = []
    for line in block_lines:
        filtered_lines.append(line[2:].strip())
    children = []   
    for line in filtered_lines:
        filtered_text_nodes = text_to_textnodes(line)
        filtered_html_nodes = map(lambda x: text_node_to_html_node(x), filtered_text_nodes)
        children.append(ParentNode("li", filtered_html_nodes))
    return ParentNode("ul", children)

def ordered_list_to_html(block):
    block_lines = block.split("\n")
    # get rid of #. followed by space at the start of every line
    # and whitespaces
    filtered_lines = []
    for line in block_lines:
        filtered_lines.append(line[3:].strip())
    children = []   
    for line in filtered_lines:
        filtered_text_nodes = text_to_textnodes(line)
        filtered_html_nodes = map(lambda x: text_node_to_html_node(x), filtered_text_nodes)
        children.append(ParentNode("li", filtered_html_nodes))
    return ParentNode("ol", children)

def code_to_html(block):
    block_no_backticks = block[3:-3]
    filtered_lines = block_no_backticks.split("\n")
    text_nodes = text_to_textnodes(" ".join(filtered_lines))
    children = text_nodes_to_html_nodes(text_nodes)
    return ParentNode("pre", [ParentNode("code", children)])

def heading_to_html(block):
    # get rid of leading # and space that follows
    block_no_hash = block.lstrip("#")[1:]
    filtered_lines = block_no_hash.split("\n")
    text_nodes = text_to_textnodes(" ".join(filtered_lines))
    children = text_nodes_to_html_nodes(text_nodes)
    return ParentNode(heading_num(block), children)

def paragraph_to_html(block):
    filtered_lines = block.split("\n")
    text_nodes = text_to_textnodes(" ".join(filtered_lines))
    children = text_nodes_to_html_nodes(text_nodes)
    return ParentNode("p", children)
