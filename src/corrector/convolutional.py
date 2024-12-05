class Trellis:
    """ A class to represent a Trellis diagram
    
    Sources: 
        http://www.irisa.fr/cosi/MOCAT/Travaux/Viterbi/contenu.html
    """

    def __init__(self, msg: str, initial_state: str = "00", polynome: str = ["111", "101"]) -> None:
        self.msg = msg
        
        if(not "0" in msg or not "1" in msg):
            self.msg_bits = ''.join(format(i, '08b') for i in bytearray(msg, encoding ='utf-8'))
        else:
            self.msg_bits = msg
        
        self.generator_polynomial = polynome
        self.initial_state = initial_state
            
    def convo_encode(self) -> list:
        """ Encode the message using the convolutional code
        
        Sources:
            https://www.youtube.com/watch?v=79kEDie6nAg
            
        Returns:
            list: The encoded message
        """
        (g1, g2) = self.generator_polynomial
        input = "00" + self.msg_bits
        register = []
        
        for i in range(len(self.msg_bits)):
            register.append(input[-3:])
            input = input[:-1]
            
        output = ""
        for j in range(len(register)):
            u1, u2 = 0, 0
            for k in range(3):
                u1 ^= int(register[j][k]) & int(g1[k])
                u2 ^= int(register[j][k]) & int(g2[k])
                    
            output = str(u1) + str(u2) + output
            
        # output = output[::-1]
        return output
    
    class BinaryTree:
        """ A binary tree class
        
            Sources:
                https://www.geeksforgeeks.org/binary-tree-set-1-introduction/
                https://stackoverflow.com/questions/34012886/print-binary-tree-level-by-level-in-python
                
            Attributes:
                LEFT (int): The left branch of the binary tree
                RIGHT (int): The right branch of the binary tree
                left (BinaryTree): The left node of the binary tree
                right (BinaryTree): The right node of the binary tree
                val (dict): The value of the binary tree represented as a dictionary
                
            Methods:
                get_left(self) -> self: Get the left node of the binary tree
                insert_left(self, val): Insert a node to the left of the binary tree
                get_right(self) -> self: Get the right node of the binary tree
                insert_right(self, val): Insert a node to the right of the binary tree
                get_val(self) -> dict: Get the value of the binary tree
                compute_branchs_metrics(self, input_bits): Compute the metrics of the binary tree branches
                compute_all_metrics(self, dist: int, message: str, path: list): Compute all the metrics of the binary tree
                display(self): Display the binary tree
                _display_aux(self) -> tuple: Display the binary tree auxiliary
                to_string(self) -> str: Convert the binary tree to a string
                
            Example:
                b = BinaryTree({"state": "start", "dist": -1, "input": None, "message": ""})
                for _ in range(50):
                    b.insert_left({"state": "start", "dist": -1, "input": None, "message": ""})
                b.display()
                
            Returns:
                BinaryTree: A binary tree
            
        """
        
        LEFT = 0
        RIGHT = 1

        def __init__(self, key: dict) -> None:
            self.left = None
            self.right = None
            
            if(key is not None and type(key) is not dict):
                raise ValueError("The key must be a dictionary")
            
            self.val = key


        def get_left(self):
            """ Get the left node of the binary tree

            Returns:
                self: The left node of the binary tree
            """
            return self.left
        
        
        def insert_left(self, val: dict):
            """ Insert a node to the left of the binary tree

            Args:
                node (self): The node to be inserted to the left of the binary tree
            """
            node = Trellis.BinaryTree(val)
            
            if self.left is None:
                self.left = node
            else:
                node.left = self.left
                self.left = node
        
        
        def get_right(self):
            """ Get the right node of the binary tree
            
            Returns:
                self: The right node of the binary tree
            """
            return self.right


        def insert_right(self, val: dict):
            """ Insert a node to the right of the binary tree

            Args:
                node (self): The node to be inserted to the right of the binary tree
            """
            node = Trellis.BinaryTree(val)
            
            if self.right is None:
                self.right = node
            else:
                node.right = self.right
                self.right = node
        
        
        def get_val(self):
            """ Get the value of the binary tree
            
            Returns:
                dict: The value of the binary tree represented as a dictionary
            """
            return self.val
        
        
        @staticmethod
        def hamming_dist(s1: str, s2: str) -> int:
            """
                Return the Hamming distance between equal-length sequences.
                Sources:
                    https://en.wikipedia.org/wiki/Hamming_distance
                    https://claresloggett.github.io/python_workshops/improved_hammingdist.html#Hamming-distance

                Parameters:
                    s1 (str): The first string to compare with the second one
                    s2 (str): The second string to compare with the first one

                Return:
                    (int) The sum of differents for each bit between two strings, also known as Hamming distance.
            """
            if len(s1) != len(s2):
                raise ValueError("Undefined for sequences of unequal length.")
            
            dist = 0
            for i in range(len(s1)):
                if str(s1[i]) != str(s2[i]):
                    dist += 1
            return dist
        
        
        @staticmethod
        def viterbi_circuit(base, input_bit) -> tuple:
            """ Viterbi circuit operation

            Args:
                base (str): Current state
                input_bit (str): Bit to be input

            Returns:
                tuple: The output bit and the new state
            """
            
            if base is not None and (isinstance(base, list) or isinstance(base, tuple)):
                fmt_base = "".join(map(str, base))
            else:
                fmt_base = base
            
            circuit = {
                # "state": {"input_bit (0)": ("output_bit", "new_state"), "input_bit (1)": ("output_bit", "new_state")}
                "00": {"0": ("00", "00"), "1": ("11", "10")},
                "10": {"0": ("10", "01"), "1": ("01", "11")},
                "01": {"0": ("11", "00"), "1": ("00", "10")},
                "11": {"0": ("01", "01"), "1": ("10", "11")}
            }

            return circuit[fmt_base][str(input_bit)]
        
        
        def compute_branchs_metrics(self, input_bits):
            """ Compute the metrics of the binary tree branches

            Args:
                input_bits (str): The input bits to be computed
            """
            if input_bits is None or input_bits == [] or input_bits == "":
                return
            
            pair = input_bits[:2]
            
            # Left branch
            out, state = self.viterbi_circuit(self.get_val()["state"], self.LEFT)
            dist = self.hamming_dist(out, pair)
            self.insert_left({"state": state, "output": out, "dist": dist, "message": str(self.LEFT)})
            self.get_left().compute_branchs_metrics(input_bits[2:])
            
            # Right branch
            out, state = self.viterbi_circuit(self.get_val()["state"], self.RIGHT)
            dist = self.hamming_dist(out, pair)
            self.insert_right({"state": state, "output": out, "dist": dist, "message": str(self.RIGHT)})
            self.get_right().compute_branchs_metrics(input_bits[2:])
            
            
        def compute_all_metrics(self, dist: int, message: str, path: list):
            """ Compute all the metrics of the binary tree

            Args:
                dist (int): Hamming distance
                message (str): The message
                path (list): The path to be computed

            Returns:
                list: The path computed
            """
            if self.get_val()["dist"] != -1:
                dist += self.get_val()["dist"]
                message += self.get_val()["message"]
                
            if self.get_left() is None and self.get_right() is None:
                path.append((dist, message))
                return path
            
            if self.get_left() is not None:
                self.get_left().compute_all_metrics(dist, message, path)
                
            if self.get_right() is not None:
                self.get_right().compute_all_metrics(dist, message, path)
                
            return path

        def display(self):
            """ Display the binary tree
            """
            print("-----------------------BIN TREE INFORMATIONS-----------------------------------")        
            lines, *_ = self._display_aux()
            print("[DIST, OUTPUT]")
            for line in lines:
                print(line)
            print("-------------------------------------------------------------------------------")
            return

        def _display_aux(self):
            """Returns list of strings, width, height, and horizontal coordinate of the root."""
            # No child.
            if self.right is None and self.left is None:
                line = '[%s' % str(self.get_val()["dist"]) + "," + str(self.get_val()["output"]) + "]"
                width = len(line)
                height = 1
                middle = width // 2
                return [line], width, height, middle

            # Only left child.
            if self.right is None:
                lines, n, p, x = self.left._display_aux()
                s = '[%s' % str(self.get_val()["dist"]) + "," + str(self.get_val()["output"]) + "]"
                u = len(s)
                first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
                second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
                shifted_lines = [line + u * ' ' for line in lines]
                return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

            # Only right child.
            if self.left is None:
                lines, n, p, x = self.right._display_aux()
                s = '[%s' % str(self.get_val()["dist"]) + "," + str(self.get_val()["output"]) + "]"
                u = len(s)
                first_line = s + x * '_' + (n - x) * ' '
                second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
                shifted_lines = [u * ' ' + line for line in lines]
                return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

            # Two children.
            left, n, p, x = self.left._display_aux()
            right, m, q, y = self.right._display_aux()
            s = '[%s' % str(self.get_val()["dist"]) + "," + str(self.get_val()["output"]) + "]"
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
            second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
            if p < q:
                left += [n * ' '] * (q - p)
            elif q < p:
                right += [m * ' '] * (p - q)
            zipped_lines = zip(left, right)
            lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
            return lines, n + m + u, max(p, q) + 2, n + u // 2
        
        
        def to_string(self) -> str:
            """ Convert the binary tree to a string

            Returns:
                str: The string representation of the binary tree
            """
            if(self is not None and self.left is not None and self.right is not None):
                return f"Node {self.val}, left: {self.left.to_string()}, right: {self.right.to_string()}"
            return

    def viterbi_decode(self, encoded_message) -> str:
        """ Decode the message using the Viterbi algorithm

        Returns:
            str: The message to be decoded
        """
        tree = Trellis.BinaryTree({"state": self.initial_state, "output": self.initial_state, "dist": -1, "message": ""})
        
        tree.compute_branchs_metrics(encoded_message)
        path = tree.compute_all_metrics(-1, "", [])
        
        min = path[0][0]
        most_probable_message = path[0][1]
        
        for i in range(1, len(path)):
            if path[i][0] < min:
                min = path[i][0]
                most_probable_message = path[i][1]
        
        tree.display()
        return most_probable_message
    
    def to_string(self) -> str:
        print("-----------------------BASIC INFORMATIONS -----------------------------------")
        print("Base message:", self.msg)
        print("Base message bits:", self.msg_bits)
        print("Generator polynomial:", self.generator_polynomial)
        print("Initial state:", self.initial_state)
        print("-----------------------------------------------------------------------------")
        return
    

if __name__ == "__main__":
    msg = "1010"
    trellis = Trellis(msg, "00")

    trellis.to_string()
    encode = trellis.convo_encode()
    decode = trellis.viterbi_decode(encoded_message=encode)

    print("-----------------------RESULT INFORMATIONS ----------------------------------")
    print("Encoded message:", encode)
    print("Decoded message bits:", decode)
    if "0" not in trellis.msg or "1" not in trellis.msg: print("Decoded message:", ''.join(chr(int(decode[i:i+8], 2)) for i in range(0, len(decode), 8)))
    print("-----------------------------------------------------------------------------")