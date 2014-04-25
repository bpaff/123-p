
a = []
b = ((1, 2), (2, 3), (3, 4), (4, 5), (5, 6))

d = []
for c in b:
    d.append((c[0] + 1, c[1] + 2))

e = tuple((c[0] + 1, c[1] + 2) for c in b)

print d
print e
