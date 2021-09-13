def is_chinese(uchar):
    # 判断一个unicode是否是汉字
    return u'\u4e00' <= uchar <= u'\u9fa5'


def is_alphabet(uchar):
    # 判断一个unicode是否是英文字母
    return (u'\u0041' <= uchar <= u'\u005a') or (u'\u0061' <= uchar <= u'\u007a')


def is_number(uchar):
    return '0' <= uchar <= '9'


def is_Illegal(uchar):
    return not (is_chinese(uchar) or is_alphabet(uchar))


class Node(object):
    def __init__(self, depth):
        self.next = {}
        self.fail = None  # 失配指针
        self.isWord = False
        self.depth = depth


class Ahocorasick(object):
    def __init__(self, _rever):
        self.__root = Node(0)
        self.result = []
        self._rever = _rever

    def addWord(self, word):
        tmp = self.__root
        for _list in word:
            if (_list[0] == '\\'):
                for char in _list:
                    if (char != '\\'):
                        tmp = tmp.next.setdefault(char, Node(tmp.depth+1))
            else:
                tmp = tmp.next.setdefault(_list, Node(tmp.depth+1))
        tmp.isWord = True

    def search(self, content, Hanzi_to_pinyin, _bushou):
        # 返回列表，每个元素为匹配的模式串在句中的起止位置
        self.result = []
        for currentPosition in range(len(content)):
            startWordIndex = currentPosition
            p = self.__root
            endWordIndex = currentPosition
            sensitiveWord = []
            if content[currentPosition] in _bushou and is_chinese(content[currentPosition]):
                self.search2(content, Hanzi_to_pinyin, _bushou,
                             content[currentPosition], startWordIndex, endWordIndex, sensitiveWord.copy(), p, 0)
            word = Hanzi_to_pinyin.convert(content[currentPosition])[0]
            self.search2(content, Hanzi_to_pinyin, _bushou,
                         word, startWordIndex, endWordIndex, sensitiveWord.copy(), p, 0)
        return self.result

    def search2(self, content, Hanzi_to_pinyin, _bushou, word, startWordIndex, endWordIndex, sensitiveWord, p, jumpMax):
        if word not in p.next:
            word = Hanzi_to_pinyin.convert(word)[0]

        if is_Illegal(word) and endWordIndex+1 < len(content):
            if jumpMax <= 20:
                jumpMax += 1
                if (startWordIndex == endWordIndex):
                    self.search2(content, Hanzi_to_pinyin, _bushou,
                                 content[endWordIndex+1], startWordIndex+1, endWordIndex + 1, sensitiveWord.copy(), p, jumpMax)
                else:
                    self.search2(content, Hanzi_to_pinyin, _bushou,
                                 content[endWordIndex+1], startWordIndex, endWordIndex + 1, sensitiveWord.copy(), p, jumpMax)
            else:
                return

        if word in p.next:
            sensitiveWord.append(word)
            # if p == self.__root:
            #   startWordIndex = currentPosition
            p = p.next[word]
            if p.isWord:
                flag = False
                for item in self.result:
                    if startWordIndex == item[0] and endWordIndex == item[1]:
                        flag = True
                    # _str存储整段可能的敏感词片段，如果它对应的敏感词是中文，中间还有数字，则删除
                _str = content[startWordIndex:endWordIndex+1]
                if is_chinese(self._rever["".join(sensitiveWord)][0]):
                    for char in _str:
                        if is_number(char):
                            flag = True
                            break
                if flag is False:
                    self.result.append(
                        (startWordIndex, endWordIndex, "".join(sensitiveWord)))
                # self.result.append(
                #    (startWordIndex, endWordIndex, "".join(sensitiveWord)))
            if p.next and endWordIndex + 1 < len(content):
                endWordIndex += 1
                if content[endWordIndex] in p.next and content[endWordIndex] in _bushou:
                    self.search2(content, Hanzi_to_pinyin, _bushou,
                                 content[endWordIndex], startWordIndex, endWordIndex, sensitiveWord.copy(), p, 0)
                word = Hanzi_to_pinyin.convert(content[endWordIndex])[0]
                self.search2(content, Hanzi_to_pinyin, _bushou,
                             word, startWordIndex, endWordIndex, sensitiveWord.copy(), p, 0)
