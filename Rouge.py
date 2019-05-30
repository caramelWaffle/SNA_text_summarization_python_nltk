import json
from rouge import Rouge

with open('./document.json') as f:
    data = json.load(f)

listData = list(data)
hyps = list()
refs = list()

for d in data:
    hyps.append(d.get('hyp'))
    refs.append(d.get('ref'))

rouge = Rouge()
scores = rouge.get_scores(hyps, refs)
print(hyps)
print(scores)