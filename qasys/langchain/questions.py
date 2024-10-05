def civic_q():
    q = []
    q.append('What are the names of mentioned capital improvement projects?')
    q.append('What are the names of projects starting before 2022?')
    q.append('What are the names of projects that were completed before 2022?')
    q.append('What are the names of disaster projects starting later than 2022?')
    q.append('What are the names of disaster projects advertised before 2023')

    return q 

def notice_q():
    q = []
     
    q.append('What is the issue date of the notice?')
    q.append('What are the violation codes for the listed items?')
    q.append('What is the name of the company being informed later than 2023 and located in California?')
    q.append('What is the name of the company receiving the notice with a non-zero civil penalty?')
    q.append('What is the name of the company receiving the notice that has proposed compliance and a warning?')
    return q

def paper_q():
    q = []
    q.append('How many authors are there for this paper?')
    q.append('What is the publication year of this paper?')
    q.append('What are the names of authors whose institutions are in the US for this paper?')
    q.append('What is the publication venue of this paper? (e.g. CHI, CSCW, etc.)')
    q.append('Does this paper involve the theory "A Model of Personal Informatics"?')
    return q

def civic_path():
    q = []
    q.append('data/civic/raw_data/malibucity_agenda__01262022-1835.pdf')
    q.append('data/civic/raw_data/malibucity_agenda__01272021-1626.pdf')
    q.append('data/civic/raw_data/malibucity_agenda__03022021-1648.pdf')
    q.append('data/civic/raw_data/malibucity_agenda__03232022-1869.pdf')
    q.append('data/civic/raw_data/malibucity_agenda__03242021-1665.pdf')
    # q.append('data/civic/raw_data/malibucity_agenda__04282021-1687.pdf')
    return q

def paper_path():
    q = []
    q.append('data/paper/raw_data/A Lived Informatics Model of Personal Informatics.pdf')
    q.append('data/paper/raw_data/Reviewing Reflection: On the Use of Reflection in Interactive System Design.pdf')
    q.append('data/paper/raw_data/When Personal Tracking Becomes Social: Examining the Use of Instagram for Healthy Eating.pdf')
    # has ground truth for theroy question
    q.append('data/paper/raw_data/A Stage-based Model of Personal Informatics Systems.pdf')
    q.append('data/paper/raw_data/A Trip to the Moon: Personalized Animated Movies for Self-reflection.pdf')
    # q.append('data/paper/raw_data/A Wee Bit More Interaction: Designing and Evaluating an Overactive Bladder App.pdf')
    # no ground truth for theroy question
    return q

def notice_path():
    q = []
    q.append('data/NoticeViolation/raw_data/12023008NOPV_PCO PCP_06152023_(20-187757)_text.pdf')
    q.append('data/NoticeViolation/raw_data/12023011NOPV_PCP_05052023_(21-207810)_text.pdf')
    q.append('data/NoticeViolation/raw_data/12023013NOPV_PCO PCP_05042023_(22-233209)_text.pdf')
    q.append('data/NoticeViolation/raw_data/12023022NOPV_PCO_04132023_(22-234207)_text.pdf')
    q.append('data/NoticeViolation/raw_data/12023027NOPV_PCP_06012023_(21-199435)_text.pdf')
    # q.append('data/NoticeViolation/raw_data/12023028NOPV_PCO_05252023_(22-232998)_text.pdf')
    return q

def get_evaluation_instruction(question:str, question_set:list[str], dataset_name:str):
    '''
    Get evaluation instruction given a question and dataset name
    '''
    evaluation_instruction = ''
    question_index= question_set.index(question)
    if dataset_name == 'paper':
        if question_index == 0 or question_index == 1:
            evaluation_instruction = " Return only a number."
        elif question_index == 3:
            evaluation_instruction = " Return only one word representing the venue."
        elif question_index == 4:
            evaluation_instruction = " Return yes or no."

    if dataset_name == 'notice':
        if question_index == 0:
            evaluation_instruction = " Return only one date."
        if question_index == 2 or question_index == 3 or question_index == 4:
            evaluation_instruction = " Return only one company name."
    return evaluation_instruction

def civic_ground_truth():
    q = []
    # q.append('What are the names of mentioned capital improvement projects?')
    q.append({
        "entity1": {
            "entity_name": "project",
            "attributes": {
                "type": "capital improvement"
            }
        }
    })
    # q.append('What are the names of projects starting before 2022?')
    q.append({
        "entity1": {
            "entity_name": "project",
            "attributes": {
                "start_date": "before 2022"
            }
        }
    })
    # q.append('What are the names of projects that were completed before 2022?')
    q.append({
        "entity1": {
            "entity_name": "project",
            "attributes": {
                "complete_date": "before 2022"
            }
        }
    })
    # q.append('What are the names of disaster projects starting later than 2022?')
    q.append({
        "entity1": {
            "entity_name": "project",
            "attributes": {
                "type": "disaster project",
                "start_date": "later than 2022"
            }
        }
    })
    # q.append('What are the names of disaster projects advertised before 2023')
    q.append({
        "entity1": {
            "entity_name": "project",
            "attributes": {
                "type": "disaster project",
                "advised_date": "before 2023"
            }
        }
    })
    return q

def notice_ground_truth():
    q = []
    # q.append('What is the issue date of the notice?')
    q.append({
        "entity1": {
            "entity_name": "notice",
            "attributes": {
                "issue_date": "disaster project"
            }
        }
    })
    # q.append('What are the violation codes for the listed items?')
    q.append({
        "entity1": {
            "entity_name": "items",
            "attributes": {
                "violation_code": "",
            }
        }
    })
    # q.append('What is the name of the company being informed later than 2023 and located in California?')
    q.append({
        "entity1": {
            "entity_name": "company",
            "attributes": {
                "informed_date": "later than 2023",
                "location": "California"
            }
        }
    })
    # q.append('What is the name of the company receiving the notice with a non-zero civil penalty?')
    q.append({
        "entity1": {
            "entity_name": "company",
            "attributes": {
                "status": "received notice",
                "penalty_type": "non-zero civil penalty"
            }
        }
    })
    # q.append('What is the name of the company receiving the notice that has proposed compliance and a warning?')
    q.append({
        "entity1": {
            "entity_name": "company",
            "attributes": {
                "status": "received notice",
                "proposed_entity1": "compliance",
                "proposed_entity2": "warning"
            }
        }
    })
    return q

def paper_ground_truth():
    q = []
    # q.append('How many authors are there for this paper?')
    q.append({
        "entity1": {
            "entity_name": "this paper",
            "attributes": {
                "authors": ""
            }
        }
    })
    # there are also other papers in a paper e.g. reference, so we need to specify "this paper"
    # q.append('What is the publication year of this paper?')
    q.append({
        "entity1": {
            "entity_name": "this paper",
            "attributes": {
                "publication_year": ""
            }
        }
    })
    # q.append('What are the names of authors whose institutions are in the US for this paper?')
    q.append({
        "entity1": {
            "entity_name": "this paper's authors",
            "attributes": {
                "institution location": "US"
            }
        }
    }) # not sure if entity name is good
    # q.append('What is the publication venue of this paper? (e.g. CHI, CSCW, etc.)')
    q.append({
        "entity1": {
            "entity_name": "this paper",
            "attributes": {
                "publication_venue": ""
            }
        }
    })
    # q.append('Does this paper involve the theory “A Model of Personal Informatics”?')
    q.append({
        "entity1": {
            "entity_name": "this paper",
            "attributes": {
                "theory": "A Model of Personal Informatics"
            }
        }
    })
    return q