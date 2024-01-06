import json
import os

File_Name = "test.txt"
Dataset_Path = "./FewNERD/supervised/{}".format(File_Name)

print('-'*20)
print(f'要处理的文件为：{Dataset_Path}')

### 2	Nadim Ladki	B-PER I-PER
# They	O
# finished	O
# the	O
# season	O
# 14–19	O
# ,	O
# 9–9	O
# in	O
# C-USA	event-sportsevent
# play	event-sportsevent
# to	O
# finish	O
# in	O
# seventh	O
# place	O
# .	O
all_sents, all_c, all_f, all_tag_list = list(), list(), list()
tags_type = list()

with open(Dataset_Path, "r") as f:
    sent, label, fine_label = list(), list(), list()
    for line in f.readlines():
        if line == "\n":
            all_sents.append(sent)
            all_c.append(label)
            all_f.append(fine_label)
            sent, label, fine_label = list(), list(), list()
        else:
            token, y = line.split()
            c_label, f_label = y.split('-')
            sent.append(token)
            label.append(c_label)
            fine_label.append(f_label)

formated_data = list()
for i, (sent, c_label) in enumerate(zip(all_sents, all_c)):
     if len(sent) > 0 and len(label) > 0:
        formated_data.append(str(i) + "\t" +" ".join(sent) + "\t" + " ".join(label))