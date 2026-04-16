import hashlib
import time

class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
    
    def __repr__(self):
        return f"{self.sender} -> {self.receiver} : {self.amount} BTC"

class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = time.time()
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        data = str(self.index) + str(self.transactions) + str(self.previous_hash) + str(self.timestamp)
        return hashlib.sha256(data.encode()).hexdigest()
    
    def __repr__(self):
        return f"\nBlock {self.index}:\nTransactions: {self.transactions}\nHash: {self.hash[:10]}..."

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
    
    def create_genesis_block(self):
        return Block(0, [], "0")
    
    def get_latest_block(self):
        return self.chain[-1]
    
    def add_block(self, new_block):
        self.chain.append(new_block)
    
    def print_chain(self):
        for block in self.chain:
            print(block)

def finney_attack_simulation():
    print("\n" + "="*50)
    print("🚨 Finney Attack Simulation Starting...")
    print("="*50 + "\n")
    
    blockchain = Blockchain()
    
    attacker_balance = 10
    merchant_balance = 0
    
    print(f"Initial Balances:")
    print(f"  Attacker: {attacker_balance} BTC")
    print(f"  Merchant: {merchant_balance} BTC\n")
    
    print("⛏️ Step 1: Attacker mines a HIDDEN block (not published)")
    tx_hidden = Transaction("attacker", "attacker", 10)
    hidden_block = Block(1, [tx_hidden], blockchain.get_latest_block().hash)
    print("   Hidden block created but NOT broadcasted to network.\n")
    
    print("💸 Step 2: Attacker sends 10 BTC to Merchant (0-confirmation transaction)")
    print("   Merchant sees the transaction and accepts it immediately ❗")
    merchant_balance += 10
    print(f"   Merchant Balance now: {merchant_balance} BTC\n")
    
    print("📢 Step 3: Attacker releases the hidden block to the network")
    blockchain.add_block(hidden_block)
    print("   Network accepts attacker's pre-mined block!\n")
    
    print("⚠️ RESULT:")
    print("   The transaction to merchant is INVALIDATED by the network")
    merchant_balance -= 10
    
    print(f"\nFinal Balances:")
    print(f"  Attacker: {attacker_balance} BTC (unchanged - got money back!)")
    print(f"  Merchant: {merchant_balance} BTC ❌ LOST THE MONEY AND THE GOODS")
    
    print("\n📊 Blockchain State (what the network sees):")
    blockchain.print_chain()
    
    print("\n" + "="*50)
    print("✅ EXPLANATION:")
    print("Because the merchant accepted a transaction with 0 confirmations,")
    print("the attacker was able to replace it with a pre-mined block.")
    print("This is exactly how the Finney Attack works!")
    print("="*50)

if __name__ == "__main__":
    finney_attack_simulation()
