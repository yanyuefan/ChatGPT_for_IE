import json
import os

### F1, precise, recall



        
TP, FP, FN = 0, 0, 0

OutputPath = "./"

Datasets_name = "CoNLL2003"
E_Setting = "0shot"
Process_name = "Origin"

outfile_name = OutputPath+Datasets_name+"_"+E_Setting+"_"+Process_name+".json"

bar = json.load(open(outfile_name, "r"))


all_target_entity = list()
for num in range(len(bar)):
    #  'GroundTruth': {'the AMA': 'ORG', 'the Bush administration': 'ORG', 'out of control trial lawyers': 'PER', 'doctors': 'PER', 'their': 'PER', 'the country': 'GPE'}, 'ChatGPTOutput': {'AMA': 'ORG', 'Bush administration': 'ORG'}
    target = bar[num]['GroundTruth']
    pred = bar[num]['ChatGPTOutput']
    for key, value in pred.items():
        if key in target and target[key] == value:
            TP += 1
        elif key not in target:
            FP += 1
    for k, v in target.items():
        all_target_entity.append({k:v})
        if k not in pred:
            FN += 1
        

### TP: pred和target一样，且预测正确
### FN: pred没预测到，但是target有
### FP：pred有，但target没有
### Recall = TP/TP+FN
### pre = TP/TP+FP
### F1 = 2 x (pre x Rec) / (pre + Rec)
pre = TP/(TP+FP)
Recall = TP/(TP+FN)
F1 = 2 * (pre * Recall) / (pre + Recall)


o = f'{Datasets_name}+{E_Setting}+{Process_name} all entity num is {len(all_target_entity)}, TP is {TP}, FN is {FN}. precise is {pre:.4f}, recall is {Recall:.4f}, F1 is {F1:.4f}'

o_fn = OutputPath+Datasets_name+'/{}'.format(Datasets_name+"_"+E_Setting+"_"+Process_name+".txt")
with open(o_fn,'w') as f:
    f.write(o)