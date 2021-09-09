import sys
from alo import Ahocorasick, Node
from change_to_pinyin import Hanzi2Pinyin
from alo import is_chinese
from os import path
# 导入初始的敏感词
#wordsFile = open(sys.argv[1], encoding='UTF-8')
wordsFile = open(path.dirname(
    __file__) + '\\static\\words.txt', encoding='UTF-8')
words = wordsFile.readlines()
wordsFile.close()

# 导入需过滤文件
#orgFile = open(sys.argv[2], encoding='UTF-8')
orgFile = open(path.dirname(
    __file__) + '\\static\\org.txt', encoding='UTF-8')
org = orgFile.readlines()
orgFile.close()

# 删除初始敏感词、原文的换行符
for index, item in enumerate(words):
    words[index] = item.strip('\n')

for index, item in enumerate(org):
    org[index] = item.strip('\n')
# 敏感词库
words1 = []
words2 = []
words3 = []
for item in words:
    words1.append(list(item))
# 汉字转拼音
Hanzi_to_pinyin = Hanzi2Pinyin()
for word in words:
    _str = Hanzi_to_pinyin.convert(word)
    words2.append(_str)
    # 存放拼音首字母的临时words数组
    _words = []
    for i in list(_str):
        _words.append(i[0])
    words3.append(_words)

# 最终敏感词库
lastWords = []
_rever = {}
for out_index, item in enumerate(words1):
    if is_chinese(item[0]):
        # 存放组合的临时数组
        __temp = []
        __temp.append(words1[out_index])
        __temp.append(words2[out_index])
        __temp.append(words3[out_index])
        for i in range(len(item)):
            for j in range(len(item)):
                for k in range(len(item)):
                    _str = ''
                    for length in range(len(item)):
                        if length == 0:
                            _str += __temp[i][length]
                        if length == 1:
                            _str += __temp[j][length]
                        if length == 2:
                            _str += __temp[k][length]
                    lastWords.append(_str)
                    # _rever字典用于将最终的“乱码”敏感词转换为正常敏感词，在<>中显示
                    _rever.setdefault(_str, words[out_index])
ans = []
ans_num = 0
# 调用Aho类实现过滤
for index, sentence in enumerate(org):
    ahoTree = Ahocorasick()
    for word in lastWords:
        ahoTree.addWord(word)
    # 构造失配指针
    ahoTree.make()
    # 英文拼音均转为小写进行比较
    result = ahoTree.search(sentence.lower())
    # print("".join(Hanzi_to_pinyin.convert(sentence)).lower())
    # result = ahoTree.search(
    #    "".join(Hanzi_to_pinyin.convert(sentence)).lower())
    if result != []:
        for k in result:
            ans_num = ans_num + 1
            ans.append('Line%d: <%s> %s' %
                       (index+1, (k[2]), sentence[k[0]:(k[1]+1)]))

ans.insert(0, 'total: ' + str(ans_num))

#ansFile = open(sys.argv[3], 'w', encoding='UTF-8')
ansFile = open(path.dirname(
    __file__) + '\\static\\ans.txt', 'w', encoding='UTF-8')
for i in ans:
    ansFile.write(i + '\n')
ansFile.close()
