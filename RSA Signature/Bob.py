from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import PKCS1_v1_5 as pkcs1_15
from Cryptodome.Hash import SHA256

# Bob side receive message
f = open('BobPrivKey.pem', 'r')
BobPrivKey = RSA.importKey(f.read(), passphrase="!@#$")
f.close()
f = open('AlicePubKey.pem', 'r')
AlicePubKey = RSA.importKey(f.read())
f.close()

f = open('message.txt', 'r')
message = f.read()
f.close()

f = open('signature.txt', 'rb')
signature = f.read()
f.close()

print("Bob received message (",message,  " ", signature,") from Alice.")
h = SHA256.new(message.encode('utf-8'))
try:
    pkcs1_15.new(AlicePubKey).verify(h, signature)
    print ("The signature is valid.")
except(ValueError, TypeError):
    print("The signature is not valid.")
