from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import PKCS1_v1_5 as pkcs1_15
from Cryptodome.Hash import SHA256
import pickle

# 1. 인증서 (X.509가 아닌)를 만드는 Python 함수를 작성하자.
def genCertificate(myPubKey, CAPrivKey):
    myPubKey = myPubKey.exportKey('PEM')
    h = SHA256.new(myPubKey)
    S = pkcs1_15.new(CAPrivKey).sign(h)
    #S는 SHA256으로 구한 myPubKey의 해시값에 CAPrivKey로 RSA 서명을 한 signature
    return [myPubKey, S]


# 2. 인증서로 인증서를 검증하는 Python 함수를 작성하자.
def veriCertificate(aCertificate, CACertificate):
    CACertificate_pub = CACertificate[0]
    CACertificate_pub = RSA.importKey(CACertificate_pub)

    aCertificate_pub = aCertificate[0]
    h = SHA256.new(aCertificate_pub)
    S = aCertificate[1]
    try:
        pkcs1_15.new(CACertificate_pub).verify(h, S)
        print("Certificate is verified")
    except(ValueError, TypeError):
        print("Certificate is not verified")
        exit(1)


# a. CA의 RSA 개인키를 만든다. 이를 파일 CAPriv.pem에 저장한다.
CA_priv = RSA.generate(2048)
f = open('CAPriv.pem', 'wb')
f.write(CA_priv.exportKey('PEM', passphrase="!@#$"))
f.close()

# b. CA의 RSA 개인키에서 공개키 CA_pub를 추출한다. 이를 파일 CAPub.pem에 저장한다.
f = open('CAPub.pem', 'wb')
CA_pub = CA_priv.publickey().exportKey('PEM')
f.write(CA_pub)
f.close()


# c. CA는 자신의 공개키에 SAH256을 적용하고, 자신의 개인키로 서명하여 서명 S_CA를 만들고,
# 이를 이용하여 자신의 root 인증서 [CA_pub, S_CA]를 만들어 CACertCA.plk 파일에 저장한다.
f = open('CAPriv.pem', 'r')
CA_priv = RSA.importKey(f.read(), passphrase="!@#$")
f.close()
f = open('CAPub.pem', 'r')
CA_pub = RSA.importKey(f.read())
f.close()

root = genCertificate(CA_pub, CA_priv)
f = open('CACertCA.plk', 'wb')
pickle.dump([root[0], root[1]], f)
f.close()


# d. Bob은 자신의 RSA 개인키를 만든다. 이를 파일 BobPriv.pem에 저장한다.
Bob_priv = RSA.generate(2048)
f = open('BobPriv.pem', 'wb')
f.write(Bob_priv.exportKey('PEM', passphrase="!@#$"))
f.close()

# e. Bob은 개인키에서 공개키 Bob_pub를 추출하여 파일 BobPub.pem에 저장한다.
f = open('BobPub.pem', 'wb')
Bob_pub = Bob_priv.publickey().exportKey('PEM')
f.write(Bob_pub)
f.close()

# f. CA는 자신의 개인키로 서명한 Bob의 공개키 인증서 [Bob_pub, S_Bob_CA]를 만들어 BobCertCA.plk에 저장한다.
f = open('BobPub.pem', 'r')
Bob_pub = RSA.importKey(f.read())
f.close()

[Bob_pub, S_Bob_CA] = genCertificate(Bob_pub, CA_priv)
f = open('BobCertCA.plk', 'wb')
pickle.dump([Bob_pub, S_Bob_CA], f)
f.close()


# g. Bob은 M = "I bought 100 doge coins." 메시지에 SHA256을 적용한 후
# 자신의 개인키로 서명한 서명 S, 메시지 M, 그리고 공개키 인증서 [Bob_pub, S_Bob_CA]를  Alice에게 보낸다.
f = open('BobPriv.pem', 'r')
Bob_priv = RSA.importKey(f.read(), passphrase="!@#$")
f.close()

f = open('BobCertCA.plk', 'rb')
S_Bob_CA = pickle.load(f)[1]
f.close()

M = "I bought 100 doge coins"
h = SHA256.new(M.encode('utf-8'))
S = pkcs1_15.new(Bob_priv).sign(h)
print("Bob sent message:", S, M, [Bob_pub, S_Bob_CA])

# h. Alice는 메시지 [M, S, [Bob_pub, S_Bob_CA]]를 받는다.
print("\nAlice received message:", M, S, [Bob_pub, S_Bob_CA])

# i. Alice는 Bob의 공개키 인증서를 검증하기 위해 CA의 root 인증서 [CA_pub, S_CA]를 파일 CACertCA.plk에서 읽는다.
f = open('CACertCA.plk', 'rb')
data = pickle.load(f)
[CA_pub, S_CA] = [data[0], data[1]]
#print("\nAlice got data from CACertCA.plk")
#print("CA_pub:", CA_pub)
#print("S_CA:", S_CA)
f.close()

# j. CA의 root 인증서를 CA의 root 인증서로 검증한다. 검증 실패의 경우 오류 메시지를 출력하고 종료한다.
print("\n<CA의 root 인증서를 CA의 root 인증서로 검증>")
veriCertificate([CA_pub, S_CA], root)

# k. Bob의 인증서를 CA의 root 인증서로 검증한다. 검증 실패의 경우 오류 메시지를 출력하고 종료한다
print("\n<Bob 인증서를 CA의 root 인증서로 검증>")
veriCertificate([Bob_pub, S_Bob_CA], root)

# l. 메시지 [M, S]를 Bob의 인증서에 있는 공개키로 검증한다. 검증 실패의 경우 오류 메시지를 출력하고 종료한다.
f = open('BobPub.pem', 'r')
Bob_pub = RSA.importKey(f.read())
f.close()
h = SHA256.new(M.encode('utf-8'))
print("\n<메시지 [M, S] 검증>")
try:
    pkcs1_15.new(Bob_pub).verify(h, S)
    print("The signature is valid.")
except(ValueError, TypeError):
    print("The signature is not valid.")


# m. 여기까지 정상적으로 오면 "Good job. Well done!"을 출력하고 종료한다.
print("\nGood job. Well done!")



