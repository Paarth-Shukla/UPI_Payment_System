
# Centralized UPI Payment Gateway

A LAN-based simulation of a **Unified Payments Interface (UPI)** system that models **users, merchants, and a bank server**.  
The project integrates **cryptography** for identity protection, **blockchain** for immutable transaction history, and a **quantum attack simulator** (Shor’s algorithm) to analyze vulnerabilities.

---

## Features
- **User, Merchant, and Bank Nodes** simulated as independent modules.
- **SHA-256 hashing** for secure MMID/PIN storage and verification.
- **Speck lightweight encryption** to generate **VMID** from **MID**, embedded in QR codes.
- **Blockchain ledger** for tamper-proof, append-only transaction recording.
- **QR-based payments** linking users to merchants seamlessly.
- **Shor’s algorithm simulation** to demonstrate quantum-era risks to PIN/UID security.

---

## System Architecture
```
User (MMID) ----> [QR Scan: VMID] ----> Merchant Node (UPI Machine) ----> Bank Server
   |                                                               |
   |                        Blockchain Ledger <--------------------|
   |                                                                
   ---> Transaction Integrity Verified via Hash-Linking
```

**Identifiers**
- **MMID**: User’s Mobile Money ID (hashed).
- **MID**: Merchant ID, issued by the bank.
- **VMID**: Virtual MID (Speck-encrypted MID), stored in QR code.

---

## Security Stack
| Layer               | Technique                 | Purpose                                  |
|----------------------|---------------------------|------------------------------------------|
| User PIN / MMID     | SHA-256 Hashing           | Non-reversible secure storage            |
| Merchant ID (MID)   | Speck Lightweight Cipher  | Obfuscation into VMID for QR codes       |
| Ledger              | Blockchain (append-only)  | Tamper-proof transaction history         |
| Research Component  | Shor's Algorithm          | Quantum-era cryptography vulnerability demo |

---

## Modules
- **`bank_server.py`** → Central bank server handling registrations, PIN verification, balances, and blockchain ledger.
- **`upi_machine.py`** → Merchant node that registers with bank, generates VMID & QR, and listens for payments.
- **`user_client.py`** → User node for registration and QR-based transactions.
- **`shor_attack.py`** → Simulates Shor’s algorithm for PIN/UID factoring demonstration.

---

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/Paarth-Shukla/UPI_Payment_System.git
cd UPI_Payment_System
```

### 2. Install Dependencies
```bash
pip install qrcode[pil]
```

### 3. Run the Bank Server
```bash
python bank_server.py
```

### 4. Run a Merchant Node
```bash
python upi_machine.py
# Enter merchant details → generates QR code with VMID
```

### 5. Run User Client
```bash
python user_client.py
# Register a user
# Scan merchant QR and make payment
```

### 6. (Optional) Simulate Quantum Attack
```bash
python shor_attack.py
# Choose PIN or UID attack simulation
```

---

## Transaction Flow
1. **User registers** → gets UID + MMID.
2. **Merchant registers** → gets MID, generates VMID.
3. **QR generated** with VMID + Merchant port.
4. **User scans QR**, enters MMID + PIN + amount.
5. **Bank verifies PIN, updates balance, appends block to blockchain.**
6. **Ledger verification** ensures tamper-proof history.

---



---

## Limitations
- Blockchain stored **in-memory only** (lost on restart).
- Communication is over **plain TCP sockets** (no TLS).
- No database persistence for users/merchants.
- Replay attacks not prevented (no nonce).

---

## Future Improvements
- Add **persistent storage** (SQLite/JSON).
- Use **TLS/SSL** for secure communication.
- Introduce **transaction nonces** to prevent replay attacks.
- Scale to **distributed ledger** with multiple bank replicas.
- Dynamic QR codes with **amount + transaction ID**.

---

## Learning Outcomes
- Hands-on with **blockchain implementation** (hash linking + verification).
- Applied **lightweight cryptography** (Speck) for ID protection.
- Understood **quantum threats** to classical cryptosystems via Shor’s algorithm.
- Practical experience with **client-server networking** in Python.

---
