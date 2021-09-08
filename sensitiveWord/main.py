import sys
from Aho_Corasick import Aho
# 导入初始的敏感词
wordsFile = open(sys.argv[1], encoding='UTF-8')
words = wordsFile.readlines()
wordsFile.close()

# 导入需过滤文件
orgFile = open(sys.argv[2], encoding='UTF-8')
org = orgFile.readlines()
orgFile.close()

# 删除初始敏感词、原文的换行符
for index, item in enumerate(words):
    words[index] = item.strip('\n')

for index, item in enumerate(org):
    org[index] = item.strip('\n')

ans = []

# 调用Aho类实现过滤
for index, item in enumerate(org):
    ob = Aho(words, item)
    result = ob.filter()
    if result != []:
        for item in result:
            _str = ('Line%d: <%s> %s' %
                    (index+1, words[item[1][0]], item[1][1]))
            ans.append(_str)

ansFile = open(sys.argv[3], 'w', encoding='UTF-8')
for i in ans:
    ansFile.write(i + '\n')
ansFile.close()
# ob = Aho(words, org[1])
# ob.filter()

# for index, item in enumerate(org):
#    print(str(index) + ':' + item)
