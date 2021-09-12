import sys
import json
from typing import List
from alo import Ahocorasick
from change_to_pinyin import Hanzi2Pinyin
from alo import is_chinese
from os import path


# 敏感词递归全排列
def _arrangement(word, words1, words2, words3, words4, step, len, _list, result, _rever):
    if step == len:
        result.append(_list)
        _rever.setdefault("".join(_list), word)
        return
    else:
        _arrangement(word, words1, words2, words3, words4, step+1, len,
                     appendList(_list.copy(), words2[step]), result, _rever)
        _arrangement(word, words1, words2, words3, words4, step+1, len,
                     appendList(_list.copy(), words3[step]), result, _rever)
        _arrangement(word, words1, words2, words3, words4, step+1, len,
                     appendList(_list.copy(), '\\' + words2[step]), result, _rever)
        return result


def appendList(ListA, word):
    ListA.append(word)
    return ListA


fp = open(path.join(path.dirname(
    __file__), 'chai_zi.json'), 'r', encoding='utf-8')
chai_zi = json.load(fp)
fp.close()

# 导入初始的敏感词
wordsFile = open(sys.argv[1], encoding='UTF-8')
# wordsFile = open(path.dirname(
#   __file__) + '\\static\\words.txt', encoding='UTF-8')
words = wordsFile.readlines()
wordsFile.close()

# 导入需过滤文件
orgFile = open(sys.argv[2], encoding='UTF-8')
# orgFile = open(path.dirname(
#    __file__) + '\\static\\org.txt', encoding='UTF-8')
org = orgFile.readlines()
orgFile.close()

# 删除初始敏感词、原文的换行符
for index, item in enumerate(words):
    words[index] = item.strip('\n')

for index, item in enumerate(org):
    org[index] = item.strip('\n')
# 敏感词库 words1为原敏感词的拆分数组，
# words2为拼音形式，
# words3为拼音形式的首字母，
# words4为部首拆分数组.
words1 = []
words2 = []
words3 = []
words4 = []
# list化敏感词，构成words1
for item in words:
    words1.append(list(item))
# 汉字转拼音，构成words2
Hanzi_to_pinyin = Hanzi2Pinyin()
for index, word in enumerate(words):
    words4.append([])
    _str = Hanzi_to_pinyin.convert(word)
    words2.append(_str)
    # 存放拼音首字母的临时words数组
    _words = []
    for i in list(_str):
        _words.append(i[0])
    # 提取拼音首字母，构成words3
    words3.append(_words)
    # 拆分部首，构成words4
    for char in word:
        words4[index].append(chai_zi.setdefault(char, char))

# print(words1)
# print(words2)
# print(words3)
# print(words4)
# 最终敏感词库
lastWords = []
# _rever用于将最终的拼音转回汉字
_rever = {}
for word in words:
    if is_chinese(word[0]):
        pass
    else:
        _rever.setdefault(word, word)

# 构成最终敏感词库
for i in range(len(words)):
    if is_chinese(words1[i][0]):
        result = _arrangement(words[i], words1[i], words2[i],
                              words3[i], words4[i], 0, len(words1[i]), [], [], _rever)
        for word in result:
            lastWords.append(word)
    else:
        lastWords.append(words[i])
ans = []

# 部首检测专用字典
_bushou = {}
for index, item in enumerate(words4):
    _bushou.setdefault(item[0][0], "".join(item))
    _rever.setdefault("".join(item), words[index])
# 此方法无法检测部首拆分后中间增加干扰，或不完全拆分

ans_num = 0
# 调用Aho类实现过滤
ahoTree = Ahocorasick()
for word in lastWords:
    ahoTree.addWord(word)
    # 构造失配指针
ahoTree.make()
for index, sentence in enumerate(org):
    # 英文拼音均转为小写进行比较
    result = ahoTree.search(sentence.lower(), Hanzi_to_pinyin, _bushou)
    if result != []:
        for index2, i in enumerate(result):
            for j in result:
                if i[0] == j[0] and i[1] < j[1]:
                    del(result[index2])
        for k in result:
            ans_num = ans_num + 1
            ans.append('Line%d: <%s> %s' %
                       (index+1, _rever.setdefault((k[2])), sentence[k[0]:(k[1]+1)]))

ans.insert(0, 'total: ' + str(ans_num))

ansFile = open(sys.argv[3], 'w', encoding='UTF-8')
# ansFile = open(path.dirname(
#    __file__) + '\\static\\ans.txt', 'w', encoding='UTF-8')
for i in ans:
    ansFile.write(i + '\n')
ansFile.close()
