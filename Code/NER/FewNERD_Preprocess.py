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
all_sents, all_y, all_tag_list = list(), list(), list()
tags_type = list()
    