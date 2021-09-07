from random import randint

num = randint(5, 10)
print("Guess what I think?")
bingo = False
while bingo == False:
    answer = int(input())

    if (answer < num):
        print('too small!')

    elif (answer > num):
        print('too big!')

    else:
        print('BINGO！')
        bingo = True
print('over')