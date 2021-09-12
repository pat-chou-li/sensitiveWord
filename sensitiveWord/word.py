# 此类用于敏感词相关操作

from change_to_pinyin import Hanzi2Pinyin
import json
from os import path
from alo import is_chinese
from alo import Ahocorasick


class sensitiveWord():
    words = []
    words1 = []
    words2 = []
    words3 = []
    words4 = []
    result = []
    _rever = {}
    chai_zi = {}
    lastWords = []
    ans = []
    _bushou = {}
    ans_num = 0
    org = []
    Hanzi_to_pinyin = ''

    #   初始化敏感词和原文
    def __init__(self, words, org):
        self.words = words
        self.org = org
        fp = open(path.join(path.dirname(
            __file__), 'chai_zi.json'), 'r', encoding='utf-8')
        self.chai_zi = json.load(fp)
        fp.close()

    # 删除原文和敏感词的换行
    def delWrap(self):
        for index, item in enumerate(self.words):
            self.words[index] = item.strip('\n')
        for index, item in enumerate(self.org):
            self.org[index] = item.strip('\n')

    # 生成多样化敏感词
    def Transformation(self):
        # list化敏感词，构成words1
        for item in self.words:
            self.words1.append(list(item))
        # 汉字转拼音，构成words2
        self.Hanzi_to_pinyin = Hanzi2Pinyin()
        for index, word in enumerate(self.words):
            self.words4.append([])
            _str = self.Hanzi_to_pinyin.convert(word)
            self.words2.append(_str)
            # 存放拼音首字母的临时_words数组
            _words = []
            for i in list(_str):
                _words.append(i[0])
            # 提取拼音首字母，构成words3
            self.words3.append(_words)
            # 拆分部首，构成words4
            for char in word:
                self.words4[index].append(self.chai_zi.setdefault(char, char))

    # 生成词典，用于最终多样化敏感词转为正常敏感词，放在<>中显示
    def createRever(self):
        for word in self.words:
            if is_chinese(word[0]):
                pass
            else:
                self._rever.setdefault(word, word)

    # 敏感词递归全排列
    def _arrangement(self, word, words1, words2, words3, words4, step, len, _list, result):
        if step == len:
            result.append(_list)
            self._rever.setdefault("".join(_list), word)
            return
        else:
            self._arrangement(word, words1, words2, words3, words4, step+1, len,
                              self.appendList(_list.copy(), words2[step]), result)
            self._arrangement(word, words1, words2, words3, words4, step+1, len,
                              self.appendList(_list.copy(), words3[step]), result)
            self._arrangement(word, words1, words2, words3, words4, step+1, len,
                              self.appendList(_list.copy(), '\\' + words2[step]), result)
            return result

    # 浅拷贝
    def appendList(self, ListA, word):
        ListA.append(word)
        return ListA

    # 生成最终敏感词List
    def createLastWords(self):
        for i in range(len(self.words)):
            if is_chinese(self.words1[i][0]):
                result = self._arrangement(self.words[i], self.words1[i], self.words2[i],
                                           self.words3[i], self.words4[i], 0, len(self.words1[i]), [], [])
                for word in result:
                    self.lastWords.append(word)
            else:
                self.lastWords.append(self.words[i])

    # 生成部首检测专用字典
    def createBushou(self):
        for index, item in enumerate(self.words4):
            self._bushou.setdefault(item[0][0], "".join(item))
            self._rever.setdefault("".join(item), self.words[index])

    # 实现过滤
    def getAnswer(self):
        # 调用Aho类实现过滤
        ahoTree = Ahocorasick()
        for word in self.lastWords:
            ahoTree.addWord(word)
        # 构造失配指针
        ahoTree.make()
        for index, sentence in enumerate(self.org):
            # 英文拼音均转为小写进行比较
            result = ahoTree.search(
                sentence.lower(), self.Hanzi_to_pinyin, self._bushou)
            if result != []:
                for index2, i in enumerate(result):
                    for j in result:
                        if i[0] == j[0] and i[1] < j[1]:
                            del(result[index2])
                for k in result:
                    self.ans_num += 1
                    self.ans.append('Line%d: <%s> %s' %
                                    (index+1, self._rever.setdefault((k[2])), sentence[k[0]:(k[1]+1)]))

        self.ans.insert(0, 'total: ' + str(self.ans_num))
        return self.ans
