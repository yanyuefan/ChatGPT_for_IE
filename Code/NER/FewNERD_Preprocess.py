import json
import os

File_Name = "test.txt"

Dataset_Path = "./FewNERD/supervised/"

File_Name = Dataset_Path+File_Name

print('-'*20)
print(f'要处理的文件为：{File_Name}')

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
all_sents, all_c, all_f = list(), list(), list()
tags_type = list()

with open(File_Name, "r", encoding='utf-8') as f:
    sent, label, fine_label = list(), list(), list()
    for line in f.readlines():
        if line == "\n":
            all_sents.append(sent)
            all_c.append(label)
            all_f.append(fine_label)
            sent, label, fine_label = list(), list(), list()
        else:
            token, y = line.split()
            if y is 'O':
                c_label, f_label = 'O', 'O'
            else:
                c_label, f_label = y.split('-')
            sent.append(token)
            label.append(c_label)
            fine_label.append(f_label)

c_formated_data, f_formated_data= list(), list()
for i, (sent, c_label) in enumerate(zip(all_sents, all_c)):
     if len(sent) > 0 and len(c_label) > 0:
        c_formated_data.append(str(i) + "\t" +" ".join(sent) + "\t" + " ".join(c_label))

for i, (sent, f_label) in enumerate(zip(all_sents, all_f)):
     if len(sent) > 0 and len(f_label) > 0:
        f_formated_data.append(str(i) + "\t" +" ".join(sent) + "\t" + " ".join(f_label))
       
output_test_file_name = 'processed_FewNERD_test_sup_croase.txt'
with open(Dataset_Path+output_test_file_name, "w", encoding='utf-8') as writer:
    for line in c_formated_data:
        writer.write(line + "\n")

print(f'croase example:\t {c_formated_data[1]}')

output_test_file_name = 'processed_FewNERD_test_sup_fine.txt'
with open(Dataset_Path+output_test_file_name, "w", encoding='utf-8') as writer:
    for line in f_formated_data:
        writer.write(line + "\n")

print(f'fine example:\t {f_formated_data[1]}')