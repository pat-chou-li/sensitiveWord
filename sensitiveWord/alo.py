def is_chinese(uchar):
    # 判断一个unicode是否是汉字
    if u'\u4e00' <= uchar <= u'\u9fa5':
        return True
    else:
        return False


def is_alphabet(uchar):
    # 判断一个unicode是否是英文字母
    if (u'\u0041' <= uchar <= u'\u005a') or (u'\u0061' <= uchar <= u'\u007a'):
        return True
    else:
        return False


def is_Illegal(uchar):
    if not (is_chinese(uchar) or is_alphabet(uchar)):
        return True
    else:
        return False


class Node(object):
    def __init__(self, depth):
        self.next = {}
        self.fail = None  # 失配指针
        self.isWord = False
        self.depth = depth


class Ahocorasick(object):
    def __init__(self):
        self.__root = Node(0)

    def addWord(self, word):
        tmp = self.__root
        for _list in word:
            if (_list[0] == '\\') is True:
                for char in _list:
                    if (char != '\\'):
                        tmp = tmp.next.setdefault(char, Node(tmp.depth+1))
            else:
                tmp = tmp.next.setdefault(_list, Node(tmp.depth+1))
        tmp.isWord = True

    def make(self):
        # 构建失败路径
        tmpQueue = list()
        tmpQueue.append(self.__root)
        while len(tmpQueue) > 0:
            temp = tmpQueue.pop()
            p = None
            for k, v in temp.next.items():
                if temp == self.__root:
                    temp.next[k].fail = self.__root
                else:
                    p = temp.fail
                    while p is not None:
                        if k in p.next:
                            temp.next[k].fail = p.next[k]
                            break
                        p = p.fail
                    if p is None:
                        temp.next[k].fail = self.__root
                tmpQueue.append(temp.next[k])

    def search(self, content, Hanzi_to_pinyin):
        # 返回列表，每个元素为匹配的模式串在句中的起止位置
        result = []
        startWordIndex = 0
        for currentPosition in range(len(content)):
            p = self.__root
            word = Hanzi_to_pinyin.convert(content[currentPosition])[0]
            endWordIndex = currentPosition
            sensitiveWord = []
            while word in p.next:
                sensitiveWord.append(word)
                if p == self.__root:
                    startWordIndex = currentPosition
                p = p.next[word]
                if p.isWord:
                    if (startWordIndex, endWordIndex, "".join(sensitiveWord)) not in result:
                        result.append(
                            (startWordIndex, endWordIndex, "".join(sensitiveWord)))
                if p.next and endWordIndex+1 < len(content):
                    endWordIndex += 1
                    #word = content[endWordIndex]
                    word = Hanzi_to_pinyin.convert(
                        content[endWordIndex])[0]
                    # jumpMax超过20的时候，不再认为是敏感词
                    jumpMax = 0
                    flagNo = False
                    while is_Illegal(word) and endWordIndex+1 < len(content):
                        jumpMax = jumpMax+1
                        endWordIndex += 1
                        #word = content[endWordIndex]
                        word = Hanzi_to_pinyin.convert(
                            content[endWordIndex])[0]
                        if (jumpMax > 20):
                            flagNo = True
                    if flagNo is True:
                        break
                else:
                    break
                while (word not in p.next) and (p != self.__root):
                    p = p.fail
                    startWordIndex += len(sensitiveWord) - p.depth
                    del(sensitiveWord[0:len(sensitiveWord) - p.depth])
                if p == self.__root:
                    break
        return result

    def replace(self, content):
       # 匹配到的字符串以'*'号表示
        replacepos = self.search(content)
        result = content
        for posindex in replacepos:
            result = result[0:posindex[0]] + \
                (posindex[1] - posindex[0] + 1) * \
                '*' + content[posindex[1] + 1:]
        return result
