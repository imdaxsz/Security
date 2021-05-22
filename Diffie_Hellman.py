# 공개 키
g = 7
p = 23

# Alice는 R1을 계산하고 Bob에게 보낸다.
x = 3
R1 = 7**3 % 23 # = 21

# Bob은 R2를 계산하고 Alice에게 보낸다.
y = 6
R2 = 7**6 % 23

# Alice의 대칭 키 K 계산
AK = 4**3 % 23

# Bob의 대칭 키 K 계산
BK = 21**6 % 23

print("Alice의 대칭 키 K:", AK)
print("Bob의 대칭 키 K:", BK)
print("g^xy mod p =", g**(x*y) % 23)

