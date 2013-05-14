import hashlib
import bitcoin.base58
import bitcoin.serialize

def public_key_to_bc_address(public_key):
  h160 = bitcoin.serialize.ser_uint160(bitcoin.serialize.Hash160(public_key))
  return encode_base58_check(h160)

def private_key_to_wallet_import_format(private_key):
  return encode_base58_check(private_key[9:9+32], version='\x80')

def encode_base58_check(payload, version="\x00"):
  vh160 = version+payload
  h3=bitcoin.serialize.ser_uint256(bitcoin.serialize.Hash(vh160))
  addr=vh160+h3[0:4]
  return bitcoin.base58.encode(addr)
