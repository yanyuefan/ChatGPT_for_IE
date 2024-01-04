import json

dataset_path = "./ACE05/"
ner_ace_path = dataset_path+"processed_ace_test.txt"

id2label = ['ORG', 'PER', 'GPE', 'LOC', 'FAC', 'VEH', 'WEA']
label2id = { l:i for i, l in enumerate(id2label) }

def get_truth(tokens, truth):
    """
    return dict {entity:label}
    """
    assert len(tokens) == len(truth)

    entity, label = list(), list()
    token_type_dict = dict()
    for i in range(len(tokens)):
        if truth[i].startswith("B-"):
            entity.append(tokens[i])
            label.append(truth[i].split("-")[-1])
        elif truth[i].startswith("I-"):
            entity.append(tokens[i])
        else:
            if len(entity) != 0:
                token_type_dict.update({ " ".join(entity): label[0] })
                entity, label = list(), list()
    
    if len(entity) > 0:
        token_type_dict.update({ " ".join(entity): label[0] })
    
    return token_type_dict

data = list()
for line in map(lambda x: x.strip().split("\t"), open(ner_ace_path, "r").readlines()):
    # 1. Raw data infomation
    sentid = line[0]
    sentence = line[1]
    label = get_truth(sentence.split(), line[2].split())
    
    # 2. Generate Prompt
    close_pred = "Given label set: %s\nText: %s\nQuestion: Please extract the named entity from the given text. Based on the given label set, provide the answer in the format: [{\"Entity Name\": \"Entity Label\"}] without any additional things including your explanations or notes." % (id2label, sentence)
    # close_reason = "Question: Tell me the reason why does the entity belong to this type?"
    data.append({
        "info": {
            "sentid": sentid,
            "sentence": sentence,
            "label": label
        },
        "close": {
            "close_pred": close_pred,
            # "close_reason": close_reason,
        }
    })

with open(dataset_path+"prompts.json", "w") as f:
    f.write(json.dumps(data, indent=4))