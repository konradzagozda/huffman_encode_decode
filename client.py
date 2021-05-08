import socket
import json
import bitarray
import bitarray.util
import HuffmanTree as HT

PLIK_Z_DRZEWEM = 'drzewo.json'

# zaladuj drzewo

huffman_codes = {}
with open(PLIK_Z_DRZEWEM, 'r') as file:
    d = json.load(file)
    for key in d:
        huffman_codes[key] = bitarray.bitarray(d[key])

# odebranie wiadomosci
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))

bytes = s.recv(1024)

# bytes -> bitarray

# odkodowanie
barr = bitarray.util.deserialize(bytes)
decoded_message = HT.decode(barr, huffman_codes)

# zapisanie
f = open("odkodowany.txt", "w")
f.write("".join(decoded_message))
f.close()