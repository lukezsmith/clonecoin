import hashlib
import json
from time import time

class Clonechain(object):
    def __init__(self):
        self.chain = []
        self.pending_transactions = []

        # instantiate the first block
        self.new_block()

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