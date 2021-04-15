#Bob
b = [7, 11, 19, 39, 79, 157, 313]
n = 900
r = 37

def calculate(b, n, r):
    return [i * r % n for i in b]

t = calculate(b, n, r)

def permute(t):
    table = [4, 2, 5, 3, 1, 7, 6]
    return [t[i-1] for i in table]

a = permute(t)

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

rd = modinv(r, n)

print("Bob generates keys")
print("t:", t)
print("a:", a)
print("Bob's private (n, r, rd, b):", n, r, rd, b)


# Alice
x = []
for i in str(format(ord('g'), 'b')):
    x.append(int(i))

def knapsackSum(a, x):
    s = 0
    for i in range(len(x)):
        s += a[i] * x[i]
    return s

s = knapsackSum(a, x)
print("\nAlice data:", x)
print("Alice makes cypertext:", s, "and sends it.")


# Bob
def inv_knapsackSum(s, a):
    x=[]
    for i in range(len(a)-1, -1, -1):
        if s >= a[i]:
            x.insert(0, 1)
            s = s - a[i]
        else:
            x.insert(0, 0)
    return x

s2 = s * rd % n
x2 = inv_knapsackSum(s2, b)
bx = permute(x2)

print("\nBob computes:")
print("s':", s2)
print("x':", x2)
print("x:", bx)