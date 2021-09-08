lst_1 = [1, 2, 3, 4, 5, 6]


def double_func(x):
    return x * 2


lst_2 = map(double_func, lst_1)
print(list(lst_2))