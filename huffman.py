import heapq
import os

class HuffmanCoding:
    def __init__(self, path):
        self.path = path
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}

    def make_frequency_dict(self, text):
        """Create a frequency dictionary for characters in the text."""
        frequency = {}
        for character in text:
            if character not in frequency:
                frequency[character] = 0
            frequency[character] += 1
        return frequency

    def make_heap(self, frequency):
        """Create a heap using the frequency dictionary (tuples of frequency and character)."""
        for key in frequency:
            heapq.heappush(self.heap, (frequency[key], key))  # Insert as a tuple
        print("Heap:", self.heap)  # Debugging

    def build_tree(self):
        """Build the Huffman Tree."""
        while len(self.heap) > 1:
            # Pop two smallest nodes (tuples of (frequency, character or tree))
            freq1, left = heapq.heappop(self.heap)
            freq2, right = heapq.heappop(self.heap)

            # Merge nodes into a new node with combined frequency and push back into heap
            merged = (freq1 + freq2, (left, right))
            heapq.heappush(self.heap, merged)

        print("Final Heap (Root of Tree):", self.heap)  # Debugging

    def build_codes_helper(self, node, current_code):
        """Helper function to recursively build the Huffman codes."""
        if isinstance(node, str):  # Leaf node (character)
            self.codes[node] = current_code
            self.reverse_mapping[current_code] = node
            return

        # Traverse left (0) and right (1) children
        self.build_codes_helper(node[0], current_code + "0")
        self.build_codes_helper(node[1], current_code + "1")

    def build_codes(self):
        """Build Huffman codes for each character."""
        if len(self.heap) == 0:
            raise ValueError("Heap is empty; cannot build codes.")

        # Get the root of the Huffman Tree
        root = heapq.heappop(self.heap)[1]
        self.build_codes_helper(root, "")

    def compress(self):
        """Compress the file and return the compressed output file path."""
        filename, _ = os.path.splitext(self.path)
        output_path = filename + ".txt"

        with open(self.path, 'r') as file, open(output_path, 'wb') as output:
            text = file.read().strip()  # Read input file and strip leading/trailing whitespace
            print("Input Text:", text)  # Debugging

            # Generate frequency dictionary, heap, and codes
            frequency = self.make_frequency_dict(text)
            self.make_heap(frequency)
            self.build_tree()
            self.build_codes()

            # Encode the text using the Huffman codes
            encoded_text = ''.join([self.codes[char] for char in text])
            print("Encoded Text:", encoded_text)  # Debugging

            # Add padding to make the length of encoded text a multiple of 8
            padding = 8 - len(encoded_text) % 8
            encoded_text += "0" * padding

            # Convert encoded text to byte array and write to file
            byte_array = bytearray(int(encoded_text[i:i+8], 2) for i in range(0, len(encoded_text), 8))
            output.write(bytes(byte_array))

        return output_path

    def decompress(self):
        """Decompress the binary file and reconstruct the original text."""
        filename, _ = os.path.splitext(self.path)
        output_path = filename + "_decompressed.txt"

        with open(self.path, 'rb') as file, open(output_path, 'w') as output:
            # Read the binary file and convert to bit string
            byte_array = file.read()
            bit_string = ''.join(format(byte, '08b') for byte in byte_array)
            print("Bit String:", bit_string)  # Debugging

            # Decode the bit string using Huffman codes
            current_code = ""
            decoded_text = ""

            for bit in bit_string:
                current_code += bit
                if current_code in self.reverse_mapping:
                    character = self.reverse_mapping[current_code]
                    decoded_text += character
                    current_code = ""

            output.write(decoded_text)

        return output_path