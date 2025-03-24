import socket
import json
from bank_registration import banks
from Crypto.Cipher import AES
import base64

HOST = '0.0.0.0'  # Accept connections on all interfaces
PORT = 65432      # Arbitrary non-privileged port

LWC_KEY = b'ThisIsASecretKey'  # Same as UPI Machine

def unpad(text):
    return text.rstrip()

def decrypt_vm_id(vm_id_encrypted_b64):
    cipher = AES.new(LWC_KEY, AES.MODE_ECB)
    decrypted = cipher.decrypt(base64.b64decode(vm_id_encrypted_b64)).decode()
    return unpad(decrypted)

def handle_client(conn):
    try:
        data = conn.recv(1024).decode()
        if not data:
            return

        txn = json.loads(data)
        mmid = txn['mmid'].strip()
        pin = txn['pin'].strip()
        amount = float(txn['amount'])
        mid = decrypt_vm_id(txn['mid'])
        bank_name = txn['bank_name']
        ifsc = txn['ifsc']

        print(f"[DEBUG] Received MMID: {mmid}, PIN: {pin}, MID: {mid}")

        bank = banks.get(bank_name)
        if not bank:
            conn.send("Invalid bank name".encode())
            return

        branch = bank.get_branch(ifsc)
        if not branch:
            conn.send("Invalid IFSC code".encode())
            return

        # Debug: show all registered users
        for u in branch.users:
            print(f"[DEBUG] Registered User -> MMID: {u.mmid}, PIN: {u.pin}")

        success = branch.verify_and_process_transaction(mmid, pin, amount, mid)
        result = "Transaction Successful" if success else "Transaction Failed"
        conn.send(result.encode())

    except Exception as e:
        print(f"Error handling transaction: {e}")
        conn.send(f"Error: {e}".encode())
    finally:
        conn.close()

def start_server():
    print(f"Starting Bank Server on {HOST}:{PORT}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            print(f"Connection from {addr}")
            handle_client(conn)

if __name__ == '__main__':
    start_server()
