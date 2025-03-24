import hashlib
import qrcode
from Crypto.Cipher import AES
import os
import base64

# --- Lightweight Cryptography (AES-based SPECK Simulation) ---
# We'll simulate LWC using AES in ECB mode with a fixed key for simplicity.
# Replace this with SPECK if implementing SPECK directly.

LWC_KEY = b'ThisIsASecretKey'  # 16 bytes for AES-128


def pad(text):
    # Pad to 16-byte block
    while len(text) % 16 != 0:
        text += ' '
    return text


def encrypt_mid(mid):
    cipher = AES.new(LWC_KEY, AES.MODE_ECB)
    padded = pad(mid)
    encrypted = cipher.encrypt(padded.encode())
    return base64.b64encode(encrypted).decode()


def generate_qr_code(data, filename='merchant_qr.png'):
    qr = qrcode.make(data)
    qr.save(filename)
    print(f"QR Code saved as {filename}")


def main():
    print("\n===== UPI MACHINE (QR Generator) =====")
    mid = input("Enter your MID: ")
    encrypted_mid = encrypt_mid(mid)
    print(f"Encrypted MID (VMID): {encrypted_mid}")
    generate_qr_code(encrypted_mid)
    print("Display this QR for scanning.")


if __name__ == '__main__':
    main()
