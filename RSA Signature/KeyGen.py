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
