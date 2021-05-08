PLIK = 'plik.txt'
PLIK_ZAKODOWANY = 'zakodowany.txt'
PLIK_Z_DRZEWEM = 'drzewo.json'
# kodowanie
import HuffmanTree as HT
import json

node = HT.getTree(PLIK)



huffman_codes = {}
HT.buildDict(huffman_codes, node)
print(huffman_codes)
with open(PLIK_Z_DRZEWEM, 'w') as file:
    file.write(json.dumps(huffman_codes))


# zapis do pliku
HT.encodeFile(PLIK, PLIK_ZAKODOWANY, huffman_codes)

# odczyt pliku
file = open(PLIK_ZAKODOWANY, "rb")
bytes = file.read()
file.close()

# przesylanie pliku do clienta
import socket

# create the socket
# AF_INET == ipv4
# SOCK_STREAM == TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((socket.gethostname(), 1234))

s.listen(5) # queue for incoming connections

while True:
    # now our endpoint knows about the OTHER endpoint.
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")

    clientsocket.send(bytes)
    print(bytes)
    clientsocket.close()
