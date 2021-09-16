import sys
from typing import List
from os import path
from word import sensitiveWord

if __name__ == '__main__':
    # 导入初始的敏感词
    wordsFile = open(sys.argv[1], encoding='UTF-8')
    words = wordsFile.readlines()
    wordsFile.close()

    # 导入需过滤文件
    orgFile = open(sys.argv[2], encoding='UTF-8')
    org = orgFile.readlines()
    orgFile.close()

    # 生成敏感词类
    _sensitiveWord = sensitiveWord(words, org)

    # 删除原文及敏感词的换行符
    _sensitiveWord.delWrap()

    # 生成多样化的敏感词
    _sensitiveWord.Transformation()

    # _rever用于将最终的拼音转回汉字
    _sensitiveWord.createRever()

    # 构成最终敏感词库
    _sensitiveWord.createLastWords()

    # 生成部首检测专用字典
    _sensitiveWord.createBushou()

    # 实现过滤，得到答案
    ans = _sensitiveWord.getAnswer()
    ansFile = open(sys.argv[3], 'w', encoding='UTF-8')
    for i in ans:
        ansFile.write(i + '\n')
    ansFile.close()
