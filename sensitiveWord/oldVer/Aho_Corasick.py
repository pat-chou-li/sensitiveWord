# python3 -m pip install pyahocorasick
import ahocorasick


class Aho:
    wordList = []
    sent = ''
    actree = None
    sent_cp = ''

    def __init__(self, wordList, sent):
        self.wordList = wordList
        self.sent = sent
        self.actree = self.build_actree(wordList)
        self.sent_cp = sent

    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    def filter(self):
        result = []
        for i in self.actree.iter(self.sent):
            result.append(i)
        return result
