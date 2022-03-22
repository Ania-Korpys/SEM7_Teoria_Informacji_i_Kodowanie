import collections
import pickle
import time


def read_text(file_name):
    with open('Pliki\\' + file_name + ".txt", encoding='UTF-8') as input_file:
        text = input_file.read()
    return text


def count_char(text):
    length = len(text)
    print("Laczna ilosc znakow: " + str(length))
    dict = {}
    i = 0
    while i < length:
        char = text[i]
        keys = dict.keys()
        if keys.__contains__(char):
            value = dict.get(char) + 1
            dict[char] = value
        else:
            dict[char] = 1
        i = i + 1
    ordered_dict = collections.OrderedDict(
        sorted(dict.items(), key=lambda d: (d[1], d[0])))  # posortowane według wartości
    print("Wszystkie znaki wraz z liczba wystapien: ")
    print(ordered_dict)
    chars = []
    values = []
    nodes = []
    for key in ordered_dict.keys():
        chars.append(key)
    for value in ordered_dict.values():
        values.append(value)
    for x in range(len(chars)):
        nodes.append(Node(values[x], chars[x]))
    return nodes


# A Huffman Tree Node
class Node:
    def __init__(self, freq, symbol, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right
        self.huff = ''


# Python program for implementation of MergeSort
def merge_sort(arr):
    if len(arr) > 1:

        mid = len(arr) // 2  # znalezienie środka
        L = arr[:mid]        # podział na dwa zbiory
        R = arr[mid:]
        merge_sort(L)        # sortowanie pierwszej części
        merge_sort(R)
        i = j = k = 0

        while i < len(L) and j < len(R):  # skopiowanie do temp arrays L[] i R[]
            if L[i].freq < R[j].freq:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

            while i < len(L):  # sprawdzenie czy został jakiś element
                arr[k] = L[i]
                i += 1
                k += 1

            while j < len(R):
                arr[k] = R[j]
                j += 1
                k += 1


def make_huffman_tree(nodes):
    while len(nodes) > 1:
        left = nodes[0]
        right = nodes[1]
        left.huff = 0
        right.huff = 1
        new_node = Node(left.freq + right.freq, left.symbol + right.symbol, left, right)
        nodes.remove(left)
        nodes.remove(right)
        nodes.append(new_node)
        merge_sort(nodes)

    print_nodes(nodes[0])


dict_codes = {}


def print_nodes(node, val=''):
    new_val = val + str(node.huff)
    if node.left:
        print_nodes(node.left, new_val)
    if node.right:
        print_nodes(node.right, new_val)
    if not node.left and not node.right:
        #print(f"{node.symbol} -> {new_val}")
        dict_codes[node.symbol] = new_val


def huffman_encode(text):
    print("Słownik: ")
    print(dict_codes)
    length = len(text)
    i = 0
    encoded_text = ""
    while i < length:
        char = text[i]
        value = dict_codes.get(char)
        encoded_text = encoded_text + value
        i = i + 1
    print("\nWczytany tekst: " + text)
    print("Tekst przy użyciu kodów: " + encoded_text)
    return encoded_text


def pad_encoded_text(encoded_text):
    extra_padding = 8 - len(encoded_text) % 8
    for i in range(extra_padding):
        encoded_text += "0"
    padded_info = "{0:08b}".format(extra_padding)  # int to binary
    encoded_text = padded_info + encoded_text
    print("\nTekst: " + encoded_text)
    return encoded_text


def get_byte_array(padded_encoded_text):
    if len(padded_encoded_text) % 8 != 0:
        print("Encoded text not padded properly")
        exit(0)

    b = bytearray()
    for i in range(0, len(padded_encoded_text), 8):
        byte = padded_encoded_text[i:i + 8]
        b.append(int(byte, 2))
    return b


def compress(encoded_text, file_name):
    output_path = "Pliki\\" + file_name + "_compressed" + ".bin"
    with open(output_path, 'wb') as output:
        padded_encoded_text = pad_encoded_text(encoded_text)
        b = get_byte_array(padded_encoded_text)
        output.write(bytes(b))

    output_path_codes = "Pliki\\" + file_name + "_codes" + ".bin"
    with open(output_path_codes, 'wb') as f:
        pickle.dump(dict_codes, f)  # , pickle.HIGHEST_PROTOCOL
    print("\nPlik został skompresowany. Skompresowany plik nazywa się: " + file_name + "_compressed.bin")
    print("Kody liter zostały zapisane do pliku o nazwie: " + file_name + "_codes.bin")


def remove_padding(padded_encoded_text):
    padded_info = padded_encoded_text[:8]
    extra_padding = int(padded_info, 2)

    padded_encoded_text = padded_encoded_text[8:]
    encoded_text = padded_encoded_text[:-1 * extra_padding]

    return encoded_text


def decode_text(encoded_text, dict_codes):
    current_code = ""
    decoded_text = ""
    keys = list(dict_codes.keys())
    vals = list(dict_codes.values())

    for bit in encoded_text:
        current_code += bit
        if current_code in dict_codes.values():
            character = keys[vals.index(current_code)]
            decoded_text += character
            current_code = ""

    return decoded_text


def decompress(file_name):
    input_path = "Pliki\\" + file_name + "_compressed.bin"
    input_path_codes = "Pliki\\" + file_name + "_codes" + ".bin"
    output_path = "Pliki\\" + file_name + "_decompressed" + ".txt"

    with open(input_path_codes, 'rb') as f:  # load all internal data
        dict_codes = pickle.load(f)

    with open(input_path, 'rb') as file, open(output_path, 'w', encoding='utf8') as output:
        bit_string = ""
        byte = file.read(1)
        while len(byte) > 0:
            byte = ord(byte)
            bits = bin(byte)[2:].rjust(8, '0')
            bit_string += bits
            byte = file.read(1)

        # print(bit_string)
        encoded_text = remove_padding(bit_string)
        # print(encoded_text)
        # print(str(dict_codes))
        decompressed_text = decode_text(encoded_text, dict_codes)
        output.write(decompressed_text)
    print("\nPlik został zdekompresowany i zapisany do pliku o nazwie: " + file_name + "_decompressed.txt")
    # print("Decompressed")


if __name__ == '__main__':
    file_name = input("Podaj nazwę pliku:")  # "new"
    start_time = time.time()
    text = read_text(file_name)
    #print(text)
    length = len(text)
    nodes = count_char(text)
    make_huffman_tree(nodes)
    # print(dict_codes)
    encoded_text = huffman_encode(text)
    compress(encoded_text, file_name)
    print("--- Compress time: %s seconds ---" % (time.time() - start_time))
    decompress_start = time.time()
    decompress(file_name)
    print("--- Decompress time:  %s seconds ---" % (time.time() - decompress_start))
    print("--- All time:  %s seconds ---" % (time.time() - start_time))
