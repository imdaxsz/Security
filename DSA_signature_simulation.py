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

q = 101
p = 8081
e0 = 3

e1 = e0**(int((p-1)/q)) % p # (=6968)
d = 61
e2 = e1**d % p # (=2038)

print("Alice's key:", e1, e2, p, q, d)

hM = 5000
r = 61

S1 = (e1**r % p) % q
rinv = modinv(r, q)
S2 = ((hM + d*S1) * rinv) % q


print("Bob receives (hM, s1, s2):", hM, S1, S2)
S2inv = modinv(S2, q)
V = ((e1**(hM*S2inv) * e2**(S1*S2inv)) % p) % q #맞음 (=54)

if S1 == V:
    print("Bob verified the message:", V)
else:
    print("Bob found the message is corrupted:", S1, V)

