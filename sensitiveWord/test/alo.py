import json
import codecs
from os import path

fp = open(path.join(path.dirname(
    __file__), 'chai_zi.json'), 'r', encoding='utf-8')
t = json.load(fp)
fp.close()
print(t['法'])
