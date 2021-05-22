from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import PKCS1_v1_5 as pkcs1_15
from Cryptodome.Hash import SHA256

# Alice side (key generation)
AlicePrivKey = RSA.generate(2048)
f = open('AlicePrivKey.pem', 'wb')
f.write(AlicePrivKey.exportKey('PEM', passphrase="!@#$"))
f.close()
f = open('AlicePubKey.pem', 'wb')
f.write(AlicePrivKey.publickey().exportKey('PEM'))
f.close()

# Bob side key generation
BobPrivKey = RSA.generate(2048)
f = open('BobPrivKey.pem', 'wb')
f.write(BobPrivKey.exportKey('PEM', passphrase="!@#$"))
f.close()
f = open('BobPubKey.pem', 'wb')
f.write(BobPrivKey.publickey().exportKey('PEM'))
f.close()


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

# Bob side receive message
f = open('BobPrivKey.pem', 'r')
BobPrivKey = RSA.importKey(f.read(), passphrase="!@#$")
f.close()
f = open('AlicePubKey.pem', 'r')
AlicePubKey = RSA.importKey(f.read())
f.close()

print("Bob received message (",message,  " ", signature,") from Alice.")
h = SHA256.new(message.encode('utf-8'))
try:
    pkcs1_15.new(AlicePubKey).verify(h, signature)
    print ("The signature is valid.")
except(ValueError, TypeError):
    print("The signature is not valid.")
