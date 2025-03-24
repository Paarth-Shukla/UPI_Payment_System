import hashlib
from datetime import datetime
from blockchain import Blockchain

class Merchant:
    def __init__(self, name, password, balance, ifsc):
        self.name = name
        self.password = password
        self.balance = balance
        self.ifsc = ifsc
        self.timestamp = datetime.now().isoformat()
        self.mid = self.generate_mid()

    def generate_mid(self):
        raw = self.name + self.timestamp + self.password
        hash_hex = hashlib.sha256(raw.encode()).hexdigest()
        return hash_hex[:16]  # 16 hex chars = 64 bits


class User:
    def __init__(self, name, password, balance, ifsc, mobile, pin):
        self.name = name
        self.password = password
        self.balance = balance
        self.ifsc = ifsc
        self.mobile = mobile
        self.pin = pin
        self.timestamp = datetime.now().isoformat()
        self.uid = self.generate_uid()
        self.mmid = self.generate_mmid()

    def generate_uid(self):
        raw = self.name + self.timestamp + self.password
        hash_hex = hashlib.sha256(raw.encode()).hexdigest()
        return hash_hex[:16]

    def generate_mmid(self):
        raw = self.uid + self.mobile
        hash_hex = hashlib.sha256(raw.encode()).hexdigest()
        return hash_hex[:16]


class BankBranch:
    def __init__(self, ifsc):
        self.ifsc = ifsc
        self.users = []
        self.merchants = []
        self.blockchain = Blockchain()

    def register_user(self, name, password, balance, mobile, pin):
        user = User(name, password, balance, self.ifsc, mobile, pin)
        self.users.append(user)
        print(f"User Registered with UID: {user.uid}, MMID: {user.mmid}")

    def register_merchant(self, name, password, balance):
        merchant = Merchant(name, password, balance, self.ifsc)
        self.merchants.append(merchant)
        print(f"Merchant Registered with MID: {merchant.mid}")

    def verify_and_process_transaction(self, mmid, pin, amount, mid):
        user = next((u for u in self.users if u.mmid == mmid and u.pin == pin), None)
        merchant = next((m for m in self.merchants if m.mid == mid), None)

        if not user:
            print("Transaction Failed: Invalid MMID or PIN")
            return False
        if not merchant:
            print("Transaction Failed: Merchant Not Found")
            return False
        if user.balance < amount:
            print("Transaction Failed: Insufficient Balance")
            return False

        # Process transaction
        user.balance -= amount
        merchant.balance += amount
        self.blockchain.add_transaction(user.uid, merchant.mid, amount)
        print("Transaction Successful")
        return True


class Bank:
    def __init__(self, name, ifsc_codes):
        self.name = name
        self.branches = {code: BankBranch(code) for code in ifsc_codes}

    def get_branch(self, ifsc):
        return self.branches.get(ifsc, None)


# Initialize 3 banks each with 3 IFSC codes
banks = {
    "HDFC": Bank("HDFC", ["HDFC001", "HDFC002", "HDFC003"]),
    "ICICI": Bank("ICICI", ["ICICI001", "ICICI002", "ICICI003"]),
    "SBI": Bank("SBI", ["SBI001", "SBI002", "SBI003"]),
}

def main_menu():
    while True:
        print("\n===== BANK REGISTRATION SYSTEM =====")
        print("1. Register Merchant")
        print("2. Register User")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            bank_name = input("Enter Bank Name (HDFC/ICICI/SBI): ").upper()
            ifsc = input("Enter IFSC Code: ")
            branch = banks.get(bank_name, None).get_branch(ifsc) if bank_name in banks else None
            if not branch:
                print("Invalid Bank or IFSC")
                continue
            name = input("Merchant Name: ")
            password = input("Password: ")
            balance = float(input("Initial Balance: "))
            branch.register_merchant(name, password, balance)

        elif choice == '2':
            bank_name = input("Enter Bank Name (HDFC/ICICI/SBI): ").upper()
            ifsc = input("Enter IFSC Code: ")
            branch = banks.get(bank_name, None).get_branch(ifsc) if bank_name in banks else None
            if not branch:
                print("Invalid Bank or IFSC")
                continue
            name = input("User Name: ")
            password = input("Password: ")
            balance = float(input("Initial Balance: "))
            mobile = input("Mobile Number: ")
            pin = input("4-digit PIN: ")
            branch.register_user(name, password, balance, mobile, pin)

        elif choice == '3':
            break
        else:
            print("Invalid Choice")

if __name__ == "__main__":
    main_menu()
