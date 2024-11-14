import re, glob, os, json

def clean_string(input_string):
    # 使用正则表达式只保留英文字母和阿拉伯数字
    input_string = input_string.replace('\n', ' ')
    cleaned_string = re.sub(r'[^a-zA-Z0-9]', '', input_string)
    return cleaned_string

# def sort_evidence(raw_provenance, evidence):
#     # your code here
#     return sorted(evidence, key=lambda x: raw_provenance.index(x))

# print(sort_evidence(raw_provenance, evidence))

def sort_substrings(provenence, evidence):
    # 创建一个字典，用于存储B中的子字符串及其在A中的位置
    A = provenence
    B = evidence
    substring_positions = {}
    for b_str in B:
        for a_index, a_str in enumerate(A):
            a = clean_string(a_str)
            b = clean_string(b_str)
            if b in a:
                b_index = a.find(b)
                substring_positions[b_str] = (a_index, b_index)
                
    sorted_items = sorted(substring_positions.items(), key=lambda item: (item[1], item[0]))
    # 提取排序后的键
    sorted_keys = [item[0] for item in sorted_items]
    
    return sorted_keys # a list of str
    # # 根据在A中的位置对B进行排序
    # sorted_B = sorted(B, key=lambda x: substring_positions[x])
    # return sorted_B


def subset_sequentially(A, B):
    # A is superset, B is subset
    # A is a list of str
    # B is a list of str
    max_b_in_A_index = 0
    for b_index, b in enumerate(B):
        if b not in A:
            continue
        if max_b_in_A_index > A.index(b):
            # print(f"b_index: {b_index}")
            # print(f"max_b_in_A_index: {max_b_in_A_index}, A.index(b): {A.index(b)}")
            # print(f"b: {b}")
            return False
        elif A.index(b) >= 0:
            # print(f"b_index: {b_index}")
            max_b_in_A_index = A.index(b)
            # print(f"max_b_in_A_index: {max_b_in_A_index}")

    return True






def sequential_checker(baseline_name:str, dataset_name:str, model_name:str):


    folder_path = f'test/output/provenance/{baseline_name}/{dataset_name}/{model_name}'

    file_paths = glob.glob(os.path.join(folder_path, '*.json'))

    # scores = [[] for _ in range(len(question_set))]
    scores = {'True': 0, 'False': 0}
    # # 依次读取每个JSON文件并解析为字典
    for file_path in file_paths:
        # 打开文件并读取内容
        with open(file_path, 'r', encoding='utf-8') as file:
            content = json.load(file)
            question = content["question"]
            baseline_type = content["baseline_type"]
            document_path = content["document_path"]
            raw_provenance = content["raw_provenance"]
            evidence = content["evidence"]
            raw_answer = content["raw_answer"]
            evidence_answer = content["evidence_answer"]
            search_pool = content["search_pool"]
            sorted_evidence = sort_substrings(raw_provenance, evidence)
            is_sequential = subset_sequentially(evidence, sorted_evidence)
            if is_sequential:
                scores['True'] += 1
            else:
                scores['False'] += 1
            # if len(sorted_evidence) != len(evidence):
            #     scores['False'] += 1
            # else:
            #     scores['True'] += 1
            
            # scores[question_index].append(jaccard_similarity_cleaned)

    return(scores['True']/ (scores['True'] + scores['False']))

if __name__ == "__main__":
    baseline_names = ['baseline1']
    dataset_names = ['civic', 'paper', 'notice']
    model_names = ['gpt35', 'gpt4o', 'gpt4omini']
    for baseline_name in baseline_names:
        for dataset_name in dataset_names:
            for model_name in model_names:
                print(f"baseline_name: {baseline_name}, dataset_name: {dataset_name}, model_name: {model_name}, sequential rate: {sequential_checker(baseline_name, dataset_name, model_name)}")


    # raw_provenance = [
    #     "(cid:131) Complete Design: Summer 2021\n(cid:131) Begin Construction: Summer/Fall 2021\n\nBirdview Avenue Improvements (CalOES Project)\n\n(cid:190) Updates:\n\n(cid:131) The design of this project has been included in the Malibu Park\nDrainage Improvements project and updates will be provided under\nthat project.\n\nOutdoor Warning Sirens (FEMA Project)\n\n(cid:190) Updates: This project will be funded through a grant from FEMA after the\nWooley Fire. The project consists of hiring a consultant to develop a plan that\nincludes the evaluation of a siren system and possible locations. Staff is\nworking on an RFQ to hire a consultant for the design.\n\n(cid:190) Project Schedule:\n\n(cid:131) Complete Design: Unknown\n\nDisaster Projects (Construction)\nNone at this time\n\nDisaster Projects (Completed)\nGuardrail Replacement Citywide (FEMA Project)\n\n(cid:190) Project Description: This project consisted of replacing the damaged\n\nguardrail throughout the City as a result of the Woolsey Fire.",
    #     "(cid:131) Complete Design: Spring 2022\n(cid:131) Begin Construction: Summer 2022\n\nLatigo Canyon Road Culvert Repairs (FEMA Project)\n\n(cid:190) Project Description: This project consists of repairing the existing storm drain\non Latigo Canyon Road located approximately 2,500 feet from PCH that was\ndamaged by the Woolsey Fire.\n\n(cid:190) Estimated Schedule:\n\n(cid:131) Complete Design: Winter 2021\n(cid:131) Begin Construction: Spring 2022\n\nEncinal Canyon Road Drainage Improvements (CalOES Project)\n\n(cid:190) Project Description: This project consists of repairing damage storm drain\nfacilities and roadway embankments that were damaged by the Woolsey Fire.\n\n(cid:190) Estimated Schedule:\n\n(cid:131) Complete Design: Winter 2021\n(cid:131) Begin Construction: Spring 2022\n\nStorm Drain Master Plan (FEMA Project)",
    #     "Corral Canyon Road Bridge Repairs (FEMA Project)\n\n(cid:190) Project Description: This project consisted of replacing fire damaged existing\nfencing and repairing the damaged embankment adjacent to the bridge.\n\nCorral Canyon Culvert Repairs (FEMA Project)\n\n(cid:190) Project Description: This project consisted of replacing a portion of Corral\n\nCanyon Road that was damaged from a failed storm drain.\n\nPage 5 of 6\n\nAgenda Item # 4.A.\n\n\n\n\n\n\n\n\n\n\n\n\nDisaster Projects (Not Started)\nClover Heights Storm Drain (FEMA Project)\n\n(cid:190) Project Description: This project consists of design and construction of a few\nstorm drains on Clover Heights. The existing storm drain facility ends at the\nintersection of Clover Heights and Harvester Road. During storms, this\nintersection floods and causes debris to block the road. An extended storm\ndrain towards the end of Clover Heights will help eliminate this issue.\n\n(cid:190) Estimated Schedule:",
    #     "(cid:190) Project Description: This project will be funded through a grant from FEMA\nafter the Woolsey Fire. The City will create a complete inventory of storm\ndrains, culverts, debris basins, manholes, and other drainage structures\nwithin the City.\n\n(cid:190) Estimated Schedule:\n\n(cid:131) Completion Date: Spring 2022\n\nPage 6 of 6\n\nAgenda Item # 4.A.",
    #     "(cid:190) Project Description: Per Malibu Municipal Code Section 17.48.070 requires\nvehicle impact protection devices to be installed for all parking spaces located\nadjacent to any outdoor pedestrian seating area. There are two locations\nwithin the City’s right-of-way and City-owned property that would require a\nvehicle impact protection device.\n\n(cid:190) Estimated Schedule:\n\n(cid:131) Complete Design: Summer 2021\n(cid:131) Begin Construction: Fall 2021\n\nMalibu Road Slope Repairs\n\n(cid:190) Project Description: The existing slope adjacent to the beach access stairs\nat 24712 Malibu Road has been eroded and caused damage to Malibu Road.\n\n(cid:190) Estimated Schedule:\n\n(cid:131) Complete Design: Fall 2021\n(cid:131) Begin Construction: Winter 2021\n\nDisaster Projects (Design)\n\nBroad Beach Road Water Quality Infrastructure Repairs (CalJPIA Project)\n\n(cid:190) Updates:\n\n(cid:131) The project consultant has started the design of the project.\n\n(cid:190) Project Schedule:"
    # ]
    # evidence = [
    #     "(cid:190) Project Schedule\n\n(cid:131) Complete Design: Spring 2021\n(cid:131) Begin Construction: Summer 2021\n\nPage 4 of 6\n\nAgenda Item # 4.A.",
    #         "Page 5 of 6\n\nAgenda Item # 4.A. Disaster Projects (Not Started)\nClover Heights Storm Drain (FEMA Project)\n\n(cid:190) Project Description: This project consists of design and construction of a few\nstorm drains on Clover Heights.",
    #         "An extended storm\ndrain towards the end of Clover Heights will help eliminate this issue. (cid:190) Estimated Schedule:",
    #         "(cid:190) Estimated Schedule:\n\n(cid:131) Completion Date: Spring 2022\n\nPage 6 of 6\n\nAgenda Item # 4.A.",
    #         "(cid:190) Project Description: This project will be funded through a grant from FEMA\nafter the Woolsey Fire.",
    #         "(cid:190) Project Schedule:\n\n(cid:131) Complete Design: Unknown\n\nDisaster Projects (Construction)\nNone at this time\n\nDisaster Projects (Completed)\nGuardrail Replacement Citywide (FEMA Project)\n\n(cid:190) Project Description: This project consisted of replacing the damaged\n\nguardrail throughout the City as a result of the Woolsey Fire.",
    #         "The existing storm drain facility ends at the\nintersection of Clover Heights and Harvester Road.",
    #         "(cid:190) Estimated Schedule:\n\n(cid:131) Complete Design: Winter 2021\n(cid:131) Begin Construction: Spring 2022\n\nStorm Drain Master Plan (FEMA Project)",
    #     "(cid:190) Project Schedule:\n\n(cid:131) Complete Design: Summer 2021\n(cid:131) Begin Construction: Summer/Fall 2021\n\nTrancas Canyon Park Slope Stabilization Project (CalJPIA Project)\n\n(cid:190) Updates:\n\n(cid:131) The project consultant has started the design of this project. (cid:190) Project Schedule:",
    #         "Outdoor Warning Sirens (FEMA Project)\n\n(cid:190) Updates: This project will be funded through a grant from FEMA after the\nWooley Fire."
    # ]
    # sorted_evidence = sort_substrings(raw_provenance, evidence)
    # for e in sorted_evidence:
    #     print(e)
    #     print('*'*10)
    # print('*'*10)
    # print(len(sorted_evidence))
    # print(len(evidence))
    # is_sequential = subset_sequentially(evidence, sorted_evidence)