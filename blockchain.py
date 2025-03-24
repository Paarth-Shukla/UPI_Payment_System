import hashlib
from datetime import datetime

class TransactionBlock:
    def __init__(self, uid, mid, amount, previous_hash):
        self.uid = uid
        self.mid = mid
        self.amount = amount
        self.timestamp = datetime.now().isoformat()
        self.previous_hash = previous_hash
        self.transaction_id = self.generate_txn_id()
        self.current_hash = self.generate_block_hash()

    def generate_txn_id(self):
        raw = self.uid + self.mid + str(self.amount) + self.timestamp
        return hashlib.sha256(raw.encode()).hexdigest()

    def generate_block_hash(self):
        raw = self.transaction_id + self.previous_hash + self.timestamp
        return hashlib.sha256(raw.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis = TransactionBlock("0" * 16, "0" * 16, 0.0, "0" * 64)
        self.chain.append(genesis)

    def add_transaction(self, uid, mid, amount):
        last_hash = self.chain[-1].current_hash
        block = TransactionBlock(uid, mid, amount, last_hash)
        self.chain.append(block)
        print(f"Transaction Added. Block Hash: {block.current_hash}")

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.previous_hash != previous.current_hash:
                return False
            if current.generate_block_hash() != current.current_hash:
                return False
        return True

# Sample blockchain test
if __name__ == "__main__":
    bc = Blockchain()
    bc.add_transaction("abcd1234efgh5678", "1234abcd5678efgh", 500.0)
    bc.add_transaction("abcd1234efgh5678", "abcd56781234efgh", 150.0)
    print("Blockchain Valid:", bc.is_chain_valid())
