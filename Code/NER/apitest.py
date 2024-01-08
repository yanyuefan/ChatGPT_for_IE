import openai
import json
import re
import time
import requests

from tqdm import tqdm

KEY = 'sk-QeKxddTyC2GfSeVMAc73450fF841435e9a5aDaF2EdE82348'

def call_fee():
    payload={}
    headers={
        'Authorization':KEY
    }
    url="https://www.plus7.plus/dashboard/billing/usage"

    response=requests.request("GET",url,headers=headers,data=payload)

    print(response.text)

#20240104 {"object":"list","total_usage":27.7084}
#20240106 {"object":"list","total_usage":32.8968}
#20240107 {"object":"list","total_usage":142.387}
#         {"object":"list","total_usage":250.7304}
#         {"object":"list","total_usage":254.312}
#20240108 {"object":"list","total_usage":749.2224}

from openai import OpenAI

client = OpenAI(
    api_key = KEY,
    base_url = "https://www.plus7.plus/v1"
)

def call_api(outfile_name, Datasets_name, label_set, max_attempts = 5):
    
    dataset_path = './{}/'.format(Datasets_name)
    ner_path = "prompts_wd.json"

    cnt = 0
    data = list()

    with open(dataset_path+ner_path, "r") as file:
        content = json.load(file)
        bar = tqdm(content)
        with open(outfile_name, "w") as o_f: 
            for line in bar:
                i = line["info"]["sentence"]
                print(f"sentence: {i} .")
                attempts = 0

                while attempts < max_attempts:
                    try:
                        bar.set_description("Pred")
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
                        break
                    except Exception as e:
                        print(f"An error occurred: {e}")
                        time.sleep(3)
                        attempts += 1

                for entity, pred_close in close_pred_chatgpt_ans_processed.items():        
                    # if entity in line["info"]["label"].keys():
                    #     ground_truth = line["info"]["label"][entity]
                    # else:
                    #     ground_truth = "O"
                    
                    while True:
                        try:
                            # 置信度 Conf
                            bar.set_description("Conf")
                            close_conf_chatgpt_ans = client.chat.completions.create(
                                model="gpt-3.5-turbo",
                                messages=[
                                    {"role": "user", "content": "Given label set: %s\nQuestion: What is the type of entity '%s' in the sentence '%s', and which category from the given label set would you use to describe this entity type? Answer me in json format like { \"label\": you choosed in the given label set } without any additional things including your notes and explanations!" % (label_set, entity, line["info"]["sentence"])},
                                    {"role": "assistant", "content": "{\"label\": \"%s\"}" % pred_close},
                                    {"role": "user", "content": line["close"]["close_conf"]},
                                ]
                            )
                            close_conf_chatgpt_ans = close_conf_chatgpt_ans.choices[0].message.content

                            close_conf_chatgpt_ans = int(re.search("\d+", close_conf_chatgpt_ans).group())
                            break
                        except:
                            time.sleep(3)

                    while True:
                        try:
                            # 难度 Diff
                            bar.set_description("Diff")
                            close_diff_chatgpt_ans = client.chat.completions.create(
                                model="gpt-3.5-turbo",
                                messages=[
                                    {"role": "user", "content": "Given label set: %s\nQuestion: What is the type of entity '%s' in the sentence '%s', and which category from the given label set would you use to describe this entity type? Answer me in json format like { \"label\": you choosed in the given label set } without any additional things including your notes and explanations!" % (label_set, entity, line["info"]["sentence"])},
                                    {"role": "assistant", "content": "{\"label\": \"%s\"}" % pred_close},
                                    {"role": "user", "content": line["close"]["close_diff"]},
                                ]
                            )
                            close_diff_chatgpt_ans = close_diff_chatgpt_ans.choices[0].message.content

                            close_diff_chatgpt_ans = json.loads(close_diff_chatgpt_ans)

                            # close_diff_chatgpt_ans = re.search("\{.*?\}", close_diff_chatgpt_ans).group()
                            break
                        except:
                            time.sleep(3)

                    
                    answer = {
                            "ent_idx": cnt,
                            "sentIdx": int(line["info"]["sentid"]),
                            "sentence": line["info"]["sentence"],
                            "GroundTruth": line["info"]["label"],
                            "ChatGPTOutput": close_pred_chatgpt_ans_processed,

                            "EntityMention": entity,
                            "ChatGPT CConf": close_conf_chatgpt_ans,
                            "ChatGPT CDiff": close_diff_chatgpt_ans
                            # "ChatGPT CDiff": close_diff_chatgpt_ans['Difficulty'],
                            # "ChatGPT CDiff Reason": close_diff_chatgpt_ans['Reason'] 
                            }
                    cnt += 1
                    data.append(answer)
                
            o_f.write(json.dumps(data, indent=4))

if __name__ == "__main__":
    Datasets_name = "Wnut17"
    # label_set = ['PER', 'LOC', 'ORG', 'MISC']
    # label_set = ['ORG', 'PER', 'GPE', 'LOC', 'FAC', 'VEH', 'WEA']
    label_set = ['corporation', 'creative-work', 'group', 'location', 'person', 'product']

    OutputPath = "./"
    E_Setting = "0shot"
    Process_name = "E_With_Diff_Conf"
    outfile_name = OutputPath+Datasets_name+"_"+E_Setting+"_"+Process_name+".json"

    max_attempts = 5
    call_api(outfile_name=outfile_name, Datasets_name=Datasets_name, label_set=label_set)
    # call_fee()