from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import PKCS1_v1_5 as pkcs1_15
from Cryptodome.Hash import SHA256

#Alice side(send message)
f = open('AlicePrivKey.pem', 'r')
AlicePrivKey = RSA.importKey(f.read(), passphrase="!@#$")
f.close()
f = open('BobPubKey.pem', 'r')
BobPubKey = RSA.importKey(f.read())
f.close()

message = 'digital sign'
h = SHA256.new(message.encode('utf-8'))
signature = pkcs1_15.new(AlicePrivKey).sign(h)

print("Alice sent(",message, " ", signature,") to Bob.")
f = open('message.txt', 'w')
f.write(message)
f.close()

f = open('signature.txt', 'wb')
f.write(signature)
f.close()
