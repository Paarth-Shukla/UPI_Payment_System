import socket
import json

BANK_HOST = '0.0.0.0'  # Replace with actual bank laptop IP
BANK_PORT = 65432


def send_transaction():
    print("\n===== UPI CLIENT (USER LAPTOP) =====")
    encrypted_mid = input("Enter scanned VMID (Encrypted MID from QR): ")
    mmid = input("Enter your MMID: ")
    pin = input("Enter your 4-digit PIN: ")
    amount = float(input("Enter transaction amount: "))
    bank_name = input("Enter bank name (HDFC/ICICI/SBI): ").upper()
    ifsc = input("Enter IFSC code of bank branch: ")

    txn_packet = {
        "mmid": mmid,
        "pin": pin,
        "amount": amount,
        "mid": encrypted_mid,
        "bank_name": bank_name,
        "ifsc": ifsc
    }

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((BANK_HOST, BANK_PORT))
            s.send(json.dumps(txn_packet).encode())
            result = s.recv(1024).decode()
            print("\n===== TRANSACTION RESULT =====")
            print(result)
    except Exception as e:
        print(f"Error sending transaction: {e}")


if __name__ == '__main__':
    send_transaction()
