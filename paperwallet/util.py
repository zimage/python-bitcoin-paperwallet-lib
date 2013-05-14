import Crypto.Hash.SHA256 as SHA256
import Crypto.Hash.RIPEMD as RIPEMD160
import hashlib
import bitcoin.base58

def hash_160(public_key):
  h1 = SHA256.new(public_key).digest()
  h2 = RIPEMD160.new(h1).digest()
  return h2

def public_key_to_bc_address(public_key):
  h160 = hash_160(public_key)
  return encode_base58_check(h160)

def private_key_to_wallet_import_format(private_key):
  return encode_base58_check(private_key[9:9+32], version='\x80')

def encode_base58_check(payload, version="\x00"):
  vh160 = version+payload
  h3=SHA256.new(SHA256.new(vh160).digest()).digest()
  addr=vh160+h3[0:4]
  return bitcoin.base58.encode(addr)
