def get_pos(n):
    return (n / 2, n * 2)


x, y = get_pos(1)

z = get_pos(1)

print(x, y)
print(z)


def changeList(l):
    l[0] = 2


l = [1, 2, 3, 4]
print(l)
changeList(l)
print(l)