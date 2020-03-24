from Crypto.PublicKey import RSA

key = RSA.generate(2048)
private_key = key.exportKey()
public_key = key.PublicKey.exportKey()

print(private_key)