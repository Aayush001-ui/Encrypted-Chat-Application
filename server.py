import socket, threading
from utils.config import SERVER_HOST, SERVER_PORT, ENCODING
from utils.encryption import decrypt_message, encrypt_message

clients = []

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                clients.remove(client)

def handle_client(client_socket, address):
    print(f"[+] {address} connected.")
    while True:
        try:
            encrypted_msg = client_socket.recv(1024)
            if not encrypted_msg: break

            decrypted_msg = decrypt_message(encrypted_msg)
            print(f"[{address}] {decrypted_msg}")
            broadcast(encrypted_msg, client_socket)

        except Exception as e:
            print(f"[-] Error with {address}: {e}")
            clients.remove(client_socket)
            client_socket.close()
            break

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_HOST, SERVER_PORT))
    server.listen(5)
    print(f"[*] Server started on {SERVER_HOST}:{SERVER_PORT}")

    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()

if __name__ == "__main__":
    main()
