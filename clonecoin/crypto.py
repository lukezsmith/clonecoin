import hashlib
from base58 import b58encode
from fastecdsa import keys, curve, ecdsa
from fastecdsa.point import Point

def generate_private_key():
    """
    Return randomly generated private key in hex
    """
    return keys.gen_private_key(curve.secp256k1)

def get_public_key(private_key):
    """
    Return public key associated with the private key passed
    """
    pub_key = keys.get_public_key(int(private_key), curve.secp256k1)
    return str(pub_key.x) + 'x' + str(pub_key.y)

def get_address(public_key):
    """
    Get address from supplied public key
    """
    # encode public key
    public_key = public_key.encode()
    # perform SHA256 hash on public key
    raw_hash = hashlib.sha256(public_key)
    # SHA1 (same as RIPEMD) hash on the raw hash
    short_hash = hashlib.sha1(raw_hash.digest())

    # prepend with version byte (0x00)
    extended_hash = short_hash.copy()
    short_hash_array = bytearray(short_hash.digest())
    short_hash_array.insert(0, 0x00)
    short_hash_bytes = bytes(short_hash_array)
    extended_hash.update(short_hash_bytes) 

    # perform secondary SHA256 hash
    secondary_hash = hashlib.sha256(extended_hash.digest())

    # perform tertiary SHA256
    tertiary_hash = hashlib.sha256(secondary_hash.digest())

    # get checksum
    checksum = tertiary_hash.digest()[:4]

    # add checksum to SHA1 hash
    raw_address = short_hash.copy()

    short_hash_array = bytearray(short_hash.digest())
    checksum_bytes = bytearray(bytes(checksum))
    checksum_bytes.extend(short_hash_array)
    checksum_bytes = bytes(checksum_bytes)

    raw_address.update(checksum_bytes)  

    # encode to base58
    address = b58encode(raw_address.digest()) 
    return address.decode()