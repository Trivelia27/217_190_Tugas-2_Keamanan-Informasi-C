# DES Encryption Communication System

Sistem komunikasi client-server sederhana yang mengimplementasikan enkripsi DES (Data Encryption Standard) dengan mode ECB dan CBC.

## 📋 Deskripsi

Proyek ini mendemonstrasikan komunikasi terenkripsi antara dua perangkat menggunakan algoritma DES. Device1 berperan sebagai client dan Device2 sebagai server. Kedua perangkat dapat bertukar pesan yang dienkripsi menggunakan mode ECB atau CBC.

## ✨ Fitur

- **Enkripsi DES**: Menggunakan algoritma DES untuk mengamankan komunikasi
- **Dual Mode**: Mendukung mode enkripsi ECB dan CBC
- **Two-Way Communication**: Komunikasi dua arah antara client dan server
- **Real-time Display**: Menampilkan plaintext, ciphertext, dan IV (untuk mode CBC)
- **Base64 Encoding**: Enkoding ciphertext untuk transmisi yang aman

## 🔧 Requirements

Pastikan Python dan library berikut telah terinstall:

```bash
pip install pycryptodome
```

## 📁 Struktur File

```
.
├── device1.py    # Client (Pengirim pertama)
├── device2.py    # Server (Penerima dan pembalas)
└── README.md     # Dokumentasi
```

## ⚙️ Konfigurasi

### Network Settings

Edit konfigurasi jaringan sesuai kebutuhan:

**device1.py:**
```python
HOST = '10.175.115.228'  # IP address server
PORT = 65432             # Port server
```

**device2.py:**
```python
HOST = '10.175.115.228'  # IP address untuk binding
PORT = 65432              # Port untuk listening
```

### Encryption Key

Kedua file menggunakan kunci yang sama (8 byte untuk DES):
```python
KEY = b'8bytekey'
```

⚠️ Pastikan KEY di kedua file identik!

## 🚀 Cara Penggunaan

### 1. Jalankan Server (Device2)

Buka terminal pertama dan jalankan:

```bash
python device2.py
```

Output:
```
📡 Device2 menunggu koneksi...
```

### 2. Jalankan Client (Device1)

Buka terminal kedua dan jalankan:

```bash
python device1.py
```

Pilih mode enkripsi:
```
Pilih mode enkripsi (ECB/CBC): CBC
🔒 Device1 terhubung ke Device2 (Mode: CBC)
```

### 3. Mulai Chat

**Device1 mengirim pesan pertama:**
```
💬 Pesan dari Device1: Hello dari Device1
```

**Device2 menerima dan membalas:**
```
📥 Pesan diterima dari Device1:
   🔓 Plain     : Hello dari Device1
   🔐 Encrypted : zX9k2mP...
   🧩 IV        : q8w9e...
   ✅ Hasil Dekripsi: Hello dari Device1

💬 Balasan dari Device2: Hello juga dari Device2
```

### 4. Keluar

Ketik `exit` di salah satu device untuk mengakhiri koneksi.

## 🔐 Mode Enkripsi

### ECB (Electronic Codebook)

- **Karakteristik**: Setiap blok plaintext dienkripsi secara independen
- **Kelebihan**: Sederhana dan cepat
- **Kekurangan**: Pola pada plaintext terlihat di ciphertext
- **Penggunaan**: Tidak memerlukan IV

### CBC (Cipher Block Chaining)

- **Karakteristik**: Setiap blok di-XOR dengan blok ciphertext sebelumnya
- **Kelebihan**: Lebih aman, pola plaintext tersembunyi
- **Kekurangan**: Sedikit lebih lambat, memerlukan IV
- **Penggunaan**: Memerlukan IV (Initialization Vector) 8 byte

## 📊 Format Pesan

Pesan yang dikirim melalui socket memiliki format:

```
MODE:CBC
IV:q8w9e7r6t5y4u3i2
Plain:Hello World
Encrypted:zX9k2mP3qR5tY8...
```

## 🛠️ Troubleshooting

### Connection Refused

**Masalah**: Client tidak dapat terhubung ke server

**Solusi**:
- Pastikan Device2 dijalankan terlebih dahulu
- Periksa IP address dan port sudah benar
- Pastikan firewall tidak memblokir koneksi
- Periksa kedua device dalam satu jaringan

### Padding Error

**Masalah**: Error saat dekripsi

**Solusi**:
- Pastikan KEY sama di kedua file
- Pastikan mode enkripsi yang dipilih sesuai
- Periksa IV dikirim dengan benar (untuk mode CBC)

### Port Already in Use

**Masalah**: Port sudah digunakan

**Solusi**:
```bash
# Linux/Mac
lsof -i :65432
kill -9 <PID>

# Windows
netstat -ano | findstr :65432
taskkill /PID <PID> /F
```
