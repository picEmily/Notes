"""
File Name: generate_content2.py
Authoer: hzwdachui
Date: 2020/08/02

Generate a dir tree and save it to a markdown file
The dir tree will show in a dropdown tree

==========================================

The nested dropdown tree syntax can be:

<details>
    <summary>dir1</summary>
    <details style="margin-left:5%">
        <summary>dir2_1</summary>
        This is a dropdown with text!
    </details>
    <details style="margin-left:5%">
        <summary>dir2_2</summary>
        This is a dropdown with text!
    </details>
</details>
"""

from pathlib import Path
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).resolve().parent  # get root dir of the current file
BASE_URL = "https://github.com/hzwdachui/Notes"
BASE_FILE_URL = BASE_URL + "/blob/master/"
BASE_DIR_URL = BASE_URL + "/tree/master/"
IGNORE = [".git", "__pycache__", ".gitignore",
          ".pytest_cache", "电脑修复", "梯子", ".vscode"]
MARGIN = 3

soup = BeautifulSoup("", features="html.parser")


class TreeNode(object):

    def __init__(self, name, level, children, node_type, parent=None):
        self.name = name            # name {"name":xxx, "url": xxx}
        self.level = level          # to compute margin 好像没用到，我对css不是很熟
        self.parent = parent        # parent node
        self.node_type = node_type  # 0 is file, 1 is dir
        self.children = children    # a list

    def __str__(self):
        return "-"*self.level + self.name


def generate_tree(path, root, ignore_path=None, n=0):
    if path.is_file():
        if ignore_path and path.name in ignore_path:
            # ignore all file in the ignore_path
            return

        url = BASE_FILE_URL + fix_name(str(path.relative_to(BASE_DIR)))
        name = {"name": path.name, "url": url}
        node = TreeNode(name, root.level+1, [], 0, root)
        root.children.append(node)
    elif path.is_dir():
        if ignore_path and path.name in ignore_path:
            return

        url = BASE_DIR_URL + fix_name(str(path.relative_to(BASE_DIR)))
        name = {"name": path.name, "url": url}
        node = TreeNode(name, root.level+1, [], 1, root)
        root.children.append(node)
        for subpath_it in path.iterdir():
            generate_tree(subpath_it, node, ignore_path, n+1)


def tree_to_html(root):
    """
    according to the tree
    generate the html page
    """

    global soup
    if root.node_type == 0:
        """
        node is file
        <p style="margin-left:{}%"> 
            <a href="xxx"></a> 
        </p>
        """

        # create tag
        new_tag_p = soup.new_tag(
            "p", style="margin-left:{}%".format(str(MARGIN)), id=root.name["url"])
        new_tag_a = soup.new_tag("a", href=root.name["url"])
        new_tag_a.string = root.name["name"]

        # generate nested tags
        parent_tag = soup.find(id=root.parent.name["url"])
        new_tag_p.append(new_tag_a)
        parent_tag.append(new_tag_p)
    else:
        """
        node is dir
        <details style="margin-left:{}%">
            <summary> <a href="xxx"></a> </summary>
        <details>
        """

        # create tag
        new_tag_details = soup.new_tag(
            "details", style="margin-left:{}%".format(str(MARGIN)), id=root.name["url"])
        new_tag_summary = soup.new_tag("summary")
        new_tag_a = soup.new_tag("a", href=root.name["url"])
        new_tag_a.string = root.name["name"]

        # generate nested tags
        parent_tag = soup.find(id=root.parent.name["url"])
        new_tag_summary.append(new_tag_a)
        new_tag_details.append(new_tag_summary)
        parent_tag.append(new_tag_details)

        for n in root.children:
            tree_to_html(n)


def save_file(tree_str, filename="README.md"):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(tree_str)


def fix_name(name):
    """
    If the file name conatains space, github can't render it properly
    Replace space with '%20'
    """
    new_name = name.replace(' ', '%20')     # %20 is space
    return new_name


if __name__ == "__main__":
    """
    generate the default div
    
    <div id="content_tree">
    </div>
    """
    dummy = TreeNode({"name": "", "url": "content_tree"}, -1, [], 1)
    new_tag_div = soup.new_tag("div", id=dummy.name["url"])
    new_tag_div.string = dummy.name["name"]
    soup.append(new_tag_div)

    generate_tree(BASE_DIR, dummy, ignore_path=IGNORE, n=0)
    tree_to_html(dummy.children[0])     # dummy.children[0] is the root node

    save_file(str(soup))
