from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,
    block_type_heading
)

import os

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)

    if block_to_block_type(blocks[0]) != block_type_heading:
        raise Exception("Markdown doesn't contain a header at the beginning")
    
    header_block = blocks[0].split("\n")
    if header_block[0].startswith("# "):
        return header_block[0][2]
    else:
        raise Exception("First header is not h1 header")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using template {template_path}")
    
    # Gets contents of markdown and template
    markdown_file = open(from_path, "r")
    template_file = open(template_path, "r")
    markdown = markdown_file.read()
    template = template_file.read()
    markdown_file.close()
    template_file.close()
    # Builds html for web page
    html_text = markdown_to_html_node(markdown).to_html()
    page_title = extract_title(markdown)

    updated_template = template.replace("{{ Title }}", page_title)
    updated_template = updated_template.replace("{{ Content }}", html_text)
    # create all directories leading to file destination
    dest_dir_path = os.path.dirname(dest_path)
    os.makedirs(dest_dir_path, exist_ok=True)
    # write to file 
    dest_file = open(dest_path, "w")
    dest_file.write(updated_template)
    dest_file.close

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dir_path_content):
        raise Exception(f"{dir_path_content} doesn't exist")
    if not os.path.isdir(dir_path_content):
        raise Exception(f"{dir_path_content} is not a directory")
    
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for item in os.listdir(dir_path_content):
        __generate_pages_recursive_helper(dir_path_content, template_path, dest_dir_path, item)


def __generate_pages_recursive_helper(dir_path_content, template_path, dest_dir_path, content):
    content_source = os.path.join(dir_path_content, content)
    content_dest = os.path.join(dest_dir_path, content)

    if os.path.isfile(content_source) and content.endswith('.md'):
        # converted file should end in html
        content = content.split(".")[0]
        content = f"{content}.html"
        content_dest = os.path.join(dest_dir_path, content)
        generate_page(content_source, template_path, content_dest)
    else:
        if not os.path.exists(content_dest):
            os.mkdir(content_dest)
        for item in os.listdir(content_source):
            __generate_pages_recursive_helper(content_source, template_path, content_dest, item)

    

        

