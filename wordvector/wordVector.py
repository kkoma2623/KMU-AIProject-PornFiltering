import glob
from math import log10
import json
from konlpy.tag import Kkma
kkma = Kkma()

with open('news.json', 'r') as f:
    news = json.load(f)

with open('tfidf_vec.json', 'r',encoding='utf8') as f:
    llist = json.load(f)
top_list = []
for i in llist:
    res = sorted(i.items(),key=(lambda x:x[1]),reverse=True)
    top_list.append(res[:15])
    print(res[:15])
print(top_list)
with open('topList.json', 'w', encoding='utf-8') as make_file:
    json.dump(top_list, make_file, indent="\t")

with open('data.json', 'r',encoding='utf8') as f:
    data = json.load(f)

for target in data:
    news['target']=kkma.nouns(data[target])
    wordId = []
    for oneNews in news:
        for text in set(news[oneNews]):
            if text in wordId:
                continue
            else:
                wordId.append(text)
    df = [0 for _ in range(len(wordId))]
    for oneFile in news:
        for text in set(news[oneFile]):
            df[wordId.index(text)] += 1
    wordVec = {}
    for oneNews in news:
        tf = [0 for _ in range(len(wordId))]
        for text in news[oneNews]:
            tf[wordId.index(text)] += 1
        for i in range(len(wordId)):
            tf[i] *= float(log10(len(news)/df[i]))
        wordVec[oneNews]=tf
    llist.append(wordVec['target'])
    del news['target']
print(llist)
