# A Huffman Tree Node
from bitarray.util import serialize
import bitarray
import json

class node:
    def __init__(self, freq, symbol, left=None, right=None):
        # frequency of symbol
        self.freq = freq

        # symbol name (charecter)
        self.symbol = symbol

        # node left of current node
        self.left = left

        # node right of current node
        self.right = right

        # tree direction (0/1)
        self.huff = ''


# utility function to print huffman
# codes for all symbols in the newly
# created Huffman tree


def printNodes(node, val=''):
    # huffman code for current node
    newVal = val + str(node.huff)

    # if node is not an edge node
    # then traverse inside it
    if (node.left):
        printNodes(node.left, newVal)
    if (node.right):
        printNodes(node.right, newVal)

        # if node is edge node then
        # display its huffman code
    if (not node.left and not node.right):
        print(f"{node.symbol} -> {newVal}")



# funkcja przyjmie nazwe pliku i zwroci jej drzewo oraz zakodowany plik
def getTree(filename):
    '''
        create a priority queue Q consisting of each unique character.
        sort then in ascending order of their frequencies.
        for all the unique characters:
            create a newNode
            extract minimum value from Q and assign it to leftChild of newNode
            extract minimum value from Q and assign it to rightChild of newNode
            calculate the sum of these two minimum values and assign it to the value of newNode
            insert this newNode into the tree
    :param filename:
    :return: rootNode
    '''

    frequency_dict = {}
    f = open(filename, "r")
    for line in f:
        for character in line:
            if character in frequency_dict:
                frequency_dict[character] += 1
            else:
                frequency_dict[character] = 1
    f.close()

    # list containing unused nodes
    nodes = [node(frequency_dict[k], k) for k in frequency_dict]

    while len(nodes) > 1:
        # sort all the nodes in ascending order
        # based on their frequency
        nodes = sorted(nodes, key=lambda x: x.freq)

        # pick 2 smallest nodes
        left = nodes[0]
        right = nodes[1]

        # assign directional value to these nodes
        left.huff = 0
        right.huff = 1

        # combine the 2 smallest nodes to create
        # new node as their parent
        newNode = node(left.freq + right.freq, left.symbol + right.symbol, left, right)

        # remove the 2 nodes and add their
        # parent as new node among others
        nodes.remove(left)
        nodes.remove(right)
        nodes.append(newNode)

    # Huffman Tree is ready!
    printNodes(nodes[0])

    return nodes[0]


def encodeFile(inFile, outFile, dic):
    import bitarray

    # read file as characters
    characters = []
    f = open(inFile, "r")
    for line in f:
        for character in line:
            characters.append(character)
    f.close()

    # characters -> encoded characters ( using tree )
    encodedbits = ""
    for char in characters:
        encodedbits += dic[char]

    encodedbits = bitarray.bitarray(encodedbits)
    print(encodedbits)
    # bits -> bytes
    bytes = serialize(encodedbits)

    # save file

    f = open(outFile, 'wb')
    f.write(bytes)
    f.close()


def findNode(node1, char):
    if node1.symbol == char:
        return node1
    if node1.left:
        n = findNode(node1.left, char)
        if n:
            return n
    if node1.right:
        n = findNode(node1.right, char)
        if n:
            return n


def buildDict(dict, node, val=''):
    # huffman code for current node
    newVal = val + str(node.huff)

    # if node is not an edge node
    # then traverse inside it
    if (node.left):
        buildDict(dict, node.left, newVal)
    if (node.right):
        buildDict(dict, node.right, newVal)

        # if node is edge node then
        # display its huffman code
    if (not node.left and not node.right):
        dict[node.symbol] = newVal


def decode(barr, huffman_dict):
    '''
    :param huffman_dict: dict z kodami do dla znaków
    :param barr: bitarray zawiera bity zakodowanej wiadomosci
    :return: string odkodowany
    '''

    cos = barr.decode(huffman_dict)
    return cos