import jsonlines
import os

File_Name = "test.ACE2005.jsonlines"
Dataset_Path = "./ACE05/{}".format(File_Name)

print('-'*20)
print(f'要处理的文件为：{Dataset_Path}')
all_sents, all_y, all_tag_list = list(), list(), list()
tags_type = list()

with jsonlines.open(Dataset_Path) as reader:
    for doc_num, doc_item in enumerate(reader):
        # print(f'这是第{doc_num}个文件：')
        # for key in doc_item.keys():
        #     print(f'ACE内单个doc的key是{key}')
        NER_tags = doc_item['ners']
        NER_sentences = doc_item['sentences']
        # print(f'这个文件有{len(NER_tags)}组标注，{len(NER_sentences)}组句子')
        for sen_num, sen_item in enumerate(NER_tags):
            # print(f'第{sen_num}句有{len(sen_item)}组标注，{len(NER_sentences[sen_num])}个词')
            
            all_sents.append(NER_sentences[sen_num])
            all_y.append(NER_tags[sen_num])
            taglist = ['O' for _ in range(len(NER_sentences[sen_num]))] 
            for tag_num, tag_item in enumerate(NER_tags[sen_num]):
                start = tag_item[0]
                end = tag_item[1]
                label = tag_item[-1]
                taglist[start] = 'B-'+str(label)
                taglist[start + 1:end + 1] = ['I-'+str(label)] * (end - start)

                if label not in tags_type:
                    tags_type.append(label)
            # print(f'tags 是：{NER_tags[sen_num]}')
            # print(f'tagslist 是：{taglist}, length is {len(taglist)}')
            # print(f'sentence 是：{NER_sentences[sen_num]}')
            all_tag_list.append(taglist)

# 1	SOCCER - JAPAN GET LUCKY WIN , CHINA IN SURPRISE DEFEAT .	O O B-LOC O O O O B-PER O O O O
# formated_data = list()
# for i, (sent, label) in enumerate(zip(all_sents, all_tag_list)):
#      if len(sent) > 0 and len(label) > 0:
#         formated_data.append(str(i) + "\t" +" ".join(sent) + "\t" + " ".join(label)) 

# output_dir = './ACE05/'        
# output_test_file_name = 'processed_ACE_test.txt'
# with open(output_dir+output_test_file_name, "w") as writer:
#     for line in formated_data:
#         writer.write(line + "\n")

print(f'tags types: {tags_type}')

        
        