import socket
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import base64
import os

HOST = '10.175.115.228'
PORT = 65432
KEY = b'8bytekey'  # harus sama dengan client

def encrypt_message(message, mode, iv=None):
    if mode == 'CBC':
        cipher = DES.new(KEY, DES.MODE_CBC, iv)
    else:
        cipher = DES.new(KEY, DES.MODE_ECB)
    padded = pad(message.encode('utf-8'), DES.block_size)
    encrypted = cipher.encrypt(padded)
    return base64.b64encode(encrypted).decode('utf-8')

def decrypt_message(encrypted_text, mode, iv=None):
    decoded = base64.b64decode(encrypted_text)
    if mode == 'CBC':
        cipher = DES.new(KEY, DES.MODE_CBC, iv)
    else:
        cipher = DES.new(KEY, DES.MODE_ECB)
    decrypted = unpad(cipher.decrypt(decoded), DES.block_size)
    return decrypted.decode('utf-8')

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("📡 Device2 menunggu koneksi...")
        conn, addr = s.accept()

        with conn:
            print(f"🔗 Terhubung dengan {addr}")
            mode = conn.recv(1024).decode().strip()
            print(f"⚙ Mode enkripsi: {mode}")

            while True:
                data = conn.recv(4096)
                if not data:
                    print("❌ Koneksi terputus.")
                    break

                msg = data.decode().split("\n")
                mode_recv, iv_recv, plain_text, encrypted_text = "", "", "", ""
                for line in msg:
                    if line.startswith("MODE:"): mode_recv = line.split(":")[1].strip()
                    elif line.startswith("IV:"): iv_recv = line.split(":")[1].strip()
                    elif line.startswith("Plain:"): plain_text = line.split(":", 1)[1].strip()
                    elif line.startswith("Encrypted:"): encrypted_text = line.split(":", 1)[1].strip()

                print("\n📥 Pesan diterima dari Device1:")
                print(f"   🔓 Plain     : {plain_text}")
                print(f"   🔐 Encrypted : {encrypted_text}")
                if mode_recv == 'CBC':
                    print(f"   🧩 IV         : {iv_recv}")

                iv_bytes = base64.b64decode(iv_recv) if mode_recv == 'CBC' and iv_recv != '-' else None
                decrypted = decrypt_message(encrypted_text, mode_recv, iv_bytes)
                print(f"   ✅ Hasil Dekripsi: {decrypted}")

                # Balasan dari server
                reply = input("\n💬 Balasan dari Device2: ")
                if reply.lower() == 'exit':
                    print("🔒 Koneksi ditutup oleh Device2.")
                    break

                iv_send = os.urandom(8) if mode == 'CBC' else None
                encrypted_reply = encrypt_message(reply, mode, iv_send)
                full_reply = f"MODE:{mode}\nIV:{base64.b64encode(iv_send).decode('utf-8') if iv_send else '-'}\nPlain:{reply}\nEncrypted:{encrypted_reply}"
                conn.sendall(full_reply.encode())

                print("📤 Pesan dikirim ke Device1:")
                print(f"   🔓 Plain     : {reply}")
                print(f"   🔐 Encrypted : {encrypted_reply}")
                if mode == 'CBC':
                    print(f"   🧩 IV         : {base64.b64encode(iv_send).decode('utf-8')}")

if __name__ == "__main__":

    main()
