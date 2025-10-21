import socket, threading
from utils.config import SERVER_HOST, SERVER_PORT, ENCODING
from utils.encryption import encrypt_message, decrypt_message

def receive_messages(client_socket):
    while True:
        try:
            encrypted_msg = client_socket.recv(1024)
            if encrypted_msg:
                msg = decrypt_message(encrypted_msg)
                print(f"\n[Chat] {msg}")
        except:
            print("[!] Connection lost.")
            break

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((SERVER_HOST, SERVER_PORT))
    except:
        print("[!] Could not connect.")
        return

    name = input("Enter your name: ")

    threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

    while True:
        try:
            msg = input()
            full_msg = f"{name}: {msg}"
            encrypted = encrypt_message(full_msg)
            client.send(encrypted)
        except KeyboardInterrupt:
            print("\n[!] Exiting chat.")
            break

if __name__ == "__main__":
    main()
