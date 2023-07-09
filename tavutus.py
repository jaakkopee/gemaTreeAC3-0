import getwordsfromdbs2 as gwdb
import hyphenate_finnish as hf
import sys
words = gwdb.getDeepMem()

hyphenatedWords = []

for i in words:
    hyphenated = hf.hyphenate(i)
    hyphenList=hyphenated.replace("\xad", " ").split()
    hyphenatedWords += [hyphenList]

#a function to search for words in hyphenatedWords by their nth syllable
def searchBySyllable(syllable, n):
    results = []
    for i in hyphenatedWords:
        if len(i) > n:
            if i[n] == syllable:
                results.append(i)
    return results

searchSyllable = sys.argv[1]
searchSyllableN = int(sys.argv[2])-1
