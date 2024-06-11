from textnode import TextNode
import os
import shutil

from copystatic import copy_dir
from generate_page import generate_pages_recursive

# Copy static
dir_path_static = "./static"
dir_path_public = "./public"

# Generate Page
dir_from_path = "./content"
dir_template_path = "./template.html"
dir_dest_path = "./public"

def main():
    print("Deleting public")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying from static into public")
    copy_dir(dir_path_static, dir_path_public)

    generate_pages_recursive(dir_from_path, dir_template_path, dir_dest_path)

main()
