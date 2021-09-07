file = open('data.txt', encoding="utf-8")
data = file.readlines()
print(data)
file.close()

file2 = open('newData.txt',"w",encoding="utf-8")
file2.write("".join(data))