"""
Authoer: hzwdachui
Date: 2020/08/02
Reference: https://blog.csdn.net/yaoyefengchen/article/details/80195231#21-%E6%A0%87%E5%87%86%E5%BA%93pathlib%E4%BB%8B%E7%BB%8D

Generate a dir tree and save it to a markdown file
"""
from pathlib import Path

tree_str = ""
BASE_DIR = Path(__file__).resolve().parent  # get root dir of the current file
BASE_URL = "https://github.com/hzwdachui/Notes"
BASE_FILE_URL = BASE_URL + "/blob/master/"
BASE_DIR_URL = BASE_URL + "/tree/master/"
IGNORE = [".git", "__pycache__", ".gitignore", ".pytest_cache", "电脑修复", "梯子", ".vscode"]


def generate_tree(path, ignore_path=None, n=0):
    global tree_str
    
    if path.is_file():
        # ignore all file in the ignore_path
        if ignore_path and path.name in ignore_path:
            return

        url = BASE_FILE_URL + fix_name(str(path.relative_to(BASE_DIR)))
        tree_str += '........|' * n + '-' * 4 + '[' + path.name + ']' + '(' + url + ')' + '  \n'
    elif path.is_dir():
        # ignore all file in the ignore_path
        if ignore_path and path.name in ignore_path:
            return
        
        url = BASE_DIR_URL + fix_name(str(path.relative_to(BASE_DIR)))
        tree_str += '........|' * n + '-' * 4 + '[' + path.name + ']' + '(' + url + ')' + '\\' + '  \n'
        for subpath_it in path.iterdir():
            generate_tree(subpath_it, ignore_path, n+1)


def save_file(tree_str, filename="README.md"):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(tree_str)

def fix_name(name):
    """
    If the file name conatains space, github can't render it properly
    Replace space with '-'
    """
    new_name = name.replace(' ', '%20')
    return new_name


if __name__ == "__main__":
    generate_tree(BASE_DIR, ignore_path=IGNORE, n=0)
    # print(tree_str)
    save_file(tree_str)








