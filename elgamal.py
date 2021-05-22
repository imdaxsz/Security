from math import gcd
import random

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    return x % m

def primRoots(modulo):
    coprime_set = {num for num in range(1, modulo) if gcd(num, modulo) == 1}
    return [g for g in range(1, modulo) if coprime_set == {pow(g, powers, modulo)
            for powers in range(1, modulo)}]

# 키 생성(Key Generation)
def ElGamel_Key_Generation():
    # Select a large prime p
    p = int(input("prime p 입력: "))
    # Select e1 to be a primitive root in the group G = <Zp^*, X>
    e1 = primRoots(p)[0]
    # Select d to be a memeber of the group G = <Z_p^*, x> such that 1 <= d <= p-2
    d = random.randint(3,p-2) # 1과 2는 좋은 값이 아니기 때문에 제외
    e2 = e1**d % p
    Public_key = (e1, e2, p)
    Private_key = d
    return Public_key, Private_key

# 암호(Encryption)
def Elgamal_Encryption(e1, e2, p, P):
    # Select a random integer r in the group G=<Z_p^*, X>
    r = random.randint(3,p-3) # 1과 p에 너무 가까운 값은 제외
    C1 = e1**r % p
    C2 = (P*e2**r) % p
    return C1, C2

# 복호(Decryption)
def ElGamal_Decryption(d, p, C1, C2):
    # d=3 p=11 C1=5 C2=6
    ie = modinv(C1**d, p)
    P = (C2*ie) % p
    return P

P = int(input("평문을 입력하세요: "))
(e1, e2, p), d = ElGamel_Key_Generation()
C1, C2 = Elgamal_Encryption(e1, e2, p, P)

ans = ElGamal_Decryption(d, p, C1, C2)
print("e1: %d, e2: %d, d: %d" %(e1, e2, d))
print("C1: %d, C2: %d" %(C1, C2))
print("P:", ans)