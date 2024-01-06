import openai
import json
import re
import time
import requests

from tqdm import tqdm
# payload={}
# headers={
#     'Authorization':'sk-QeKxddTyC2GfSeVMAc73450fF841435e9a5aDaF2EdE82348'
# }
# url="https://www.plus7.plus/dashboard/billing/usage"

# response=requests.request("GET",url,headers=headers,data=payload)

# print(response.text)
# #20240104 {"object":"list","total_usage":27.7084}

from openai import OpenAI

client = OpenAI(
    api_key = "sk-QeKxddTyC2GfSeVMAc73450fF841435e9a5aDaF2EdE82348",
    base_url = "https://www.plus7.plus/v1"
)
dataset_path = './ACE05/'
ner_path = "prompts.json"
cnt = 0
data = list()
max_attempts = 5  # 设置最大尝试次数


with open(dataset_path+ner_path, "r") as file:
    content = json.load(file)
    bar = tqdm(content)

    for line in bar:
        i = line["info"]["sentence"]
        print(f"sentence: {i} .")
        attempts = 0

        while attempts < max_attempts:
            try:
                close_pred_chatgpt_ans = client.chat.completions.create(
                    model="gpt-3.5-turbo-1106",
                    messages=[
                        {"role": "user", "content": line["close"]["close_pred"]}
                    ],
                )
                close_pred_chatgpt_ans = close_pred_chatgpt_ans.choices[0].message.content

                close_pred_chatgpt_ans_processed = {
                    list(item.keys())[0]: list(item.values())[0] for item in eval(
                    re.search(r'\[(.*?)\]', close_pred_chatgpt_ans).group(0))
                }
        
                for entity, pred_close in close_pred_chatgpt_ans_processed.items():        
                    if entity in line["info"]["label"].keys():
                        ground_truth = line["info"]["label"][entity]
                    else:
                        ground_truth = "O"

                answer = {
                        "idx": cnt,
                        "sentIdx": line["info"]["sentid"],
                        "sentence": line["info"]["sentence"],
                        "GroundTruth": line["info"]["label"],
                        "ChatGPTOutput": close_pred_chatgpt_ans_processed
                        }  
                data.append(answer)
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                time.sleep(3)
                attempts += 1
        cnt += 1
            
OutputPath = "./"

Datasets_name = "ACE05"
E_Setting = "0shot"
Process_name = "Origin"

outfile_name = OutputPath+Datasets_name+"_"+E_Setting+"_"+Process_name+".json"

with open(outfile_name, "w") as f:
    f.write(json.dumps(data, indent=4))

    
