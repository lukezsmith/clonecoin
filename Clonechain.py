import hashlib
import json
from time import time
import pprint
from fastecdsa import keys, curve,ecdsa


from clonecoin.crypto import generate_private_key, get_public_key, get_address

class Clonechain(object):
    def __init__(self):
        self.chain = []
        self.pending_transactions = []

        # instantiate the first block
        self.new_block(100, "The Times 03/Jan/2009 Chancellor on brink of second bailout for banks.")

    # function for adding a new block to the chain 
    def new_block(self, proof, previous_hash=None):
        block = {
            "index" : len(self.chain) + 1,
            "timestamp": time(),
            "transactions": self.pending_transactions,
            "proof": proof,
            "previous_hash": previous_hash or self.hash(self.chain[-1]),
        }

        self.pending_transactions = []
        self.chain.append(block)

        return block

    # function for retrieving the last block in the chain
    @property
    def last_block(self):
        return self.chain[-1]


    # function for creating a new transaction to be adde to a block in the chain
    def new_transaction(self, sender, recipient, amount):
        transaction = {
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
        }
        self.pending_transactions.append(transaction)
        return self.last_block['index'] + 1

    # function for hashing a block such that it is not possible to modify a block's contents
    def hash(self, block):
        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object.encode()

        raw_hash = hashlib.sha256(block_string)
        hex_hash = raw_hash.hexdigest()

        return hex_hash

class Wallet(object):
    def __init__(self):

        # generate private key
        self.private_key = generate_private_key()
        # get public key
        self.public_key = get_public_key(self.private_key)
        # get wallet address
        self.address = get_address(self.public_key)
    
if __name__ == "__main__":
    # instantiate blockchain
    blockchain = Clonechain()
    # instantiate a wallet 
    wallet = Wallet()
