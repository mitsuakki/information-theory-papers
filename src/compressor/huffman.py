from collections import Counter
import sys
import time
import matplotlib.pyplot as plt
import networkx as nx

FILE = "words.txt"

class Node:
    def __init__(self, value: int, name: str) -> None:
        self.name: str = name
        self.value: int = value
        self.left: Node = None
        self.right: Node = None
        self.parent: Node = None
    
    def __str__(self):
        right = ""
        left = ""
        parent = ""
        
        if self.right == None: right = "None"
        else: right = self.right.name
        
        if self.left == None: left = "None"
        else: left = self.left.name
        
        if self.parent == None: parent = "None"
        else: parent = self.parent.name
        
        return("'" + self.name + "' : " + str(self.value) + " --- left : '" + left + "', right : '" + right + "', parent : '" + parent + "'")

class Tree:
    def __init__(self) -> None:
        self.root: Node = None
        self.node_liste: list = None
        
    def creation_tree(self, node_liste: list):
        liste: list = node_liste.copy()
        final_liste: list = []
        while len(liste) > 2:
            left: Node = liste.pop(0)
            right: Node = liste.pop(0)
            final_liste.append(right)
            final_liste.append(left)
            new_node: Node = Node(left.value + right.value, str(left.value + right.value))
            new_node.left = left
            new_node.right = right
            left.parent = new_node
            right.parent = new_node
            liste.append(new_node)
            liste = sorted(liste, key=lambda x: x.value)
        
        self.root = Node(liste[0].value + liste[1].value, "root")
        
        self.root.left = liste[0]
        self.root.right = liste[1]
        liste[0].parent = self.root
        liste[1].parent = self.root
        
        final_liste.append(liste[1])
        final_liste.append(liste[0])
        final_liste.append(self.root)
        
        final_liste = sorted(final_liste, key=lambda x: x.value)
        self.node_liste = final_liste
    
    def get_node(self, name) -> Node: 
        for i in self.node_liste:
            if i.name == name:
                return i
        return None
    

def build_binary_from_str(tree: Tree, string: str, verif : bool) -> str:
    final_string: str = ""
    if verif : print("start building binary string")
    for i in string:
        node: Node = tree.get_node(i)
        if verif : print(node.name + " : ", end="")
        tmp_str: str = ""
        while node.name != "root":
            if node.parent.left == node:
               tmp_str =tmp_str + "0"
            else:
               tmp_str =tmp_str + "1"
            node = node.parent
        if verif : print(tmp_str + " -> ", end="")
        inverse = ''.join(reversed(tmp_str))
        if verif : print(inverse)
        final_string = final_string + inverse
    return final_string

def build_string_from_binary(tree: Tree, string: str) -> str:
    final_string: str = ""
    node : Node = tree.get_node("root")
    
    for i in string:
        if i == "0":
            node = node.left
        else:
            node = node.right
        
        if node.right == None and node.left == None:
            final_string = final_string + node.name
            node = tree.get_node("root")
    return final_string

def get_frequency(chaine: str):
    letter_frequency: dict = Counter()
    for i in chaine:
        letter_frequency[i] += 1
    return letter_frequency

def creationArbre(chaine: str, affichage: bool, return_bin = False) -> tuple:
    letter_frequency: dict = get_frequency(chaine)
    sorted_frequency: list = sorted(letter_frequency.items(), key=lambda x: x[1])
    node_liste: list = []
    for i in sorted_frequency:
        node_liste.append(Node(i[1], i[0]))
    
    tree: Tree = Tree()
    tree.creation_tree(node_liste)
    
    
    for i in tree.node_liste:
        if affichage : print(i)
        
    if affichage : print("initial string : " + chaine + ", avec : " + str(len(chaine)) + " characteres")
    binary_compressed_string: str = build_binary_from_str(tree, chaine, affichage)
    if affichage : print("Compression binaire : " + binary_compressed_string)
    initial_string: str = build_string_from_binary(tree, binary_compressed_string)
    if affichage : print("Conversion en str : " + initial_string + ", avec : " + str(len(initial_string)) + " characteres")
    if return_bin : return (binary_compressed_string, tree)
    return initial_string
    
    
def test_huffman():
    print("Starting test . . . ")
    start = time.time()
    words = []
    with open("../wordgame/words.txt", "r") as file:
            for line in file:
                words.append(line.rstrip("\n"))
    
    for word in words:
        new_words: str = creationArbre(word, False)
        if word == new_words:
            print("\033[32m[1]\033[0m" + " successed for : " + word)
        else:
            print("\033[31m[0]\033[0m" + " Failed for : " + word)
            break
    end = time.time()
    print("Tests finished in " + str(end - start) + " seconds")
        

def file_huffman_binary(string: str) -> str:
    
    file_content: str = ""
    
    with open(string, 'r') as file:
        
        for ligne in file:
            file_content = file_content + ligne
    
    file_compressed, tree = creationArbre(file_content, False, True)
    
    new_file: str = string[:-4] + "_compressed.txt"
    
    with open(new_file, 'w') as file:
        file.write(file_compressed)
        
    return new_file, tree

def file_huffman_string(file: str, tree: Tree):
    file_content: str = ""
    
    with open(file, 'r') as f:
        
        for ligne in f:
            file_content = file_content + ligne
    print(file_content)
    initial_content = build_string_from_binary(tree, file_content)
    new_file = file[:-14] + "initial.txt"
    with open(new_file, 'w') as f:
        f.write(initial_content)

def display_binary_tree(arbre, pos=None, ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(8,6))
    if pos is None:
        fig = nx.spring_layout(arbre)
    
    nx.draw(arbre, pos, ax=ax, with_labels=True, node_size=2000, node_color="skyblue", font_size=10, font_weight="bold")
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        creationArbre("J'adore monsieur Fosse ainsi que les mathematiques", True)
    else:
        arg = sys.argv[1]
        if arg[:4] == "test" and arg[5:] == "true":
            test_huffman()
        elif arg[:4] == "file":
            if arg[-4:] == '.txt':
                new_file, tree = file_huffman_binary(arg[5:])
                file_huffman_string(new_file, tree)
            else :
                print("given extention : " + arg[-4:])
                sys.exit("\033[31mErreure : mauvaise extention dans votre fichier, veuillez nous donner un fichier en .txt\033[0m")
        else:
            new_file, tree = creationArbre(sys.argv[1], True)