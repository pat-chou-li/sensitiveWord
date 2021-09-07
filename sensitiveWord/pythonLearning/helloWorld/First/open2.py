f = open('scores.txt', encoding='gbk')
lines = f.readlines()
# print(lines)
f.close()

results = []
 
for line in lines:
   # print (line)
   data = line.split()
   # print (data)

   sum = 0
   score_list = data[1:]
   for score in score_list:
       sum += int(score)
   result = '%s \t: %d\n' % (data[0], sum)
   # print (result)
   
   results.append(result)

# print (results)
output = open('result.txt', 'w', encoding='gbk')
output.writelines(results)
output.close()