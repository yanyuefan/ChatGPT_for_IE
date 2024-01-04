import jsonlines
import os

File_Name = "test.txt"
Dataset_Path = "./FewNERD/supervised/{}".format(File_Name)

print('-'*20)
print(f'要处理的文件为：{Dataset_Path}')
all_sents, all_y, all_tag_list = list(), list(), list()
tags_type = list()
    