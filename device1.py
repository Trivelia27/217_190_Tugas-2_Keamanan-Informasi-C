import socket
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import base64
import os

HOST = '10.175.115.228' 
PORT = 65432
KEY = b'8bytekey'  # kunci DES harus 8 byte

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
    mode = input("Pilih mode enkripsi (ECB/CBC): ").strip().upper()
    if mode not in ['ECB', 'CBC']:
        print("❌ Mode tidak valid. Gunakan ECB atau CBC.")
        return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(mode.encode())  # kirim mode ke server
        print(f"🔒 Device1 terhubung ke Device2 (Mode: {mode})")

        while True:
            msg = input("\n💬 Pesan dari Device1: ")
            if msg.lower() == 'exit':
                print("🔚 Koneksi ditutup oleh Device1.")
                break

            iv = os.urandom(8) if mode == 'CBC' else None
            encrypted_msg = encrypt_message(msg, mode, iv)

            full_msg = f"MODE:{mode}\nIV:{base64.b64encode(iv).decode('utf-8') if iv else '-'}\nPlain:{msg}\nEncrypted:{encrypted_msg}"
            s.sendall(full_msg.encode())

            print("\n📤 Pesan dikirim ke Device2:")
            print(f"   🔓 Plain     : {msg}")
            print(f"   🔐 Encrypted : {encrypted_msg}")
            if mode == 'CBC':
                print(f"   🧩 IV         : {base64.b64encode(iv).decode('utf-8')}")

            # Terima balasan
            data = s.recv(4096)
            if not data:
                print("❌ Koneksi terputus.")
                break

            reply = data.decode().split("\n")
            mode_recv, iv_recv, plain_reply, encrypted_reply = "", "", "", ""
            for line in reply:
                if line.startswith("MODE:"): mode_recv = line.split(":")[1].strip()
                elif line.startswith("IV:"): iv_recv = line.split(":")[1].strip()
                elif line.startswith("Plain:"): plain_reply = line.split(":", 1)[1].strip()
                elif line.startswith("Encrypted:"): encrypted_reply = line.split(":", 1)[1].strip()

            print("\n📩 Balasan dari Device2:")
            print(f"   🔓 Plain     : {plain_reply}")
            print(f"   🔐 Encrypted : {encrypted_reply}")
            if mode_recv == 'CBC':
                print(f"   🧩 IV         : {iv_recv}")

            iv_bytes = base64.b64decode(iv_recv) if mode_recv == 'CBC' else None
            decrypted_reply = decrypt_message(encrypted_reply, mode_recv, iv_bytes)
            print(f"   ✅ Hasil Dekripsi: {decrypted_reply}")

if __name__ == "__main__":
    main()