def nltk_sent_tokenize(text:str, minimum_token_num=10):
    from nltk.tokenize import sent_tokenize
    sentences = sent_tokenize(text) # is a list[str]
    new_sentences = [sentences[0]]
    for sentence_index, sentence in enumerate(sentences[1:]):
        if get_token_num(new_sentences[-1])<minimum_token_num:
            new_sentences[-1] = new_sentences[-1] + ' ' + sentence

        else:
            if sentence_index == len(sentences)-2: # start from one
                if get_token_num(sentence) >= minimum_token_num:
                    new_sentences.append(sentence)
                else:
                    new_sentences[-1] = new_sentences[-1] + ' ' + sentence
            else:
                new_sentences.append(sentence)
    return new_sentences

def nltk_sent_tokenize_for_list(text_list: list, minimum_token_num=20):
    sentences = []
    for text in text_list:
        sentences += nltk_sent_tokenize(text, minimum_token_num=minimum_token_num)
    return sentences

def get_token_num_for_list(text_list: list):
    token_num = 0
    for text in text_list:
        token_num += get_token_num(text)
    return token_num

def get_token_num(text:str):
    import re
    words = re.findall(r'\b\w+\b', text)
    return len(words)



# import spacy

# # Load the English model
# nlp = spacy.load('en_core_web_sm')

# # Example paragraph
# paragraph = ['(cid:131) The contractor is also working on the curb, gutter and storm drain\ninstallation on Civic Center Way from Webb Way to the condos. This\nportion of the work may require temporary road closures. However, it\nis anticipated that this phase of the project will be completed at the\nend of February 2021.\n\n(cid:190) Project Schedule: August 2020 through March 2021\n\nPage 3 of 6\n\nAgenda Item # 4.A.\n\n\n\n\n\n\n\n\nCapital Improvement Projects (Not Started)\n\nAnnual Street Maintenance\n\n(cid:190) Project Description: This project provides for the reconstruction and\n\nmaintenance of City streets.\n\n(cid:190) Estimated Schedule:\n\n(cid:131) Complete Design: Spring 2021\n(cid:131) Begin Construction: Summer 2021\n\nBluffs Park Shade Structure\n\n(cid:190) Project Description: This project consists of the installation of four single-\n\npost shade structures at Malibu Bluffs Park\n\n(cid:190) Estimated Schedule:\n\n(cid:131) Complete Design: Summer 2021\n(cid:131) Begin Construction: Fall 2021', '(cid:131) The project assessment engineer has begun\n\nthe process of\n\nevaluating the project costs.\n\n(cid:131) Next public community meeting is scheduled for March 25th.\n\n(cid:190) Project Schedule:\n\n(cid:131) Complete Design: December 2021\n(cid:131) Begin Construction: March 2022\n\nPage 2 of 6\n\nAgenda Item # 4.A.\n\n\n\n\n\n\n\n\n\n\nMalibu Park Drainage Improvements\n\n(cid:190) Updates:\n\n(cid:131) Staff is making minor modifications to the project plans to reduce the\n\noverall project costs.\n\n(cid:131) Project is scheduled to go out to bid next week.\n\n(cid:190) Project Schedule:\n\n(cid:131) Complete Design: February 2021\n(cid:131) Begin Construction: April 2021\n\nCapital Improvement Projects (Construction)\n\nCity Hall Roof Replacement\n\n(cid:190) Updates: The City has held project meetings with the contractor and is\n\ndeveloping a project schedule.\n\n(cid:190) Project Schedule: February – April 2021\n\nBluffs Park Workout Station', '(cid:190) Updates: The contractor is waiting for the delivery of the new workout\nstation equipment. The equipment is anticipated to be delivered at the end\nof February.\n\n(cid:190) Project Schedule: November 2020 – March 2021\n\nCivic Center Way Improvements\n\n(cid:190) Updates:\n\n(cid:131) Work Hours: Monday through Friday 7:00AM to 4:00PM, Saturdays\n\n7:00AM to 4:00PM\n\n(cid:131) The contractor is currently working at the section between Vista\nPacifica and the condos on Civic Center Way. This phase of work will\nrequire the temporary closure of Civic Center Way. Portions of the\ncurb and gutter have been placed and the contactor is working on the\nproposed retaining wall. This portion of work is anticipated to be\ncompleted in early February 2021.', 'Public Works Commission\nAgenda Report\n\nPublic Works\nCommission Meeting\n03-02-21\nItem\n4.A.\n\nTo:\n\nChair Merrick and Members of the Public Works Commission\n\nPrepared by:\n\nRobert DuBoux, Public Works Director/City Engineer\n\nDate prepared: February 18, 2021\n\nMeeting date: March 2, 2021\n\nSubject:\n\nCapital Improvement Projects and Disaster Recovery Projects Status\nReport\n\nRECOMMENDED ACTION: Receive and file report on the status of the City’s current and\nupcoming Capital Improvements Projects and Disaster Recovery Projects.\n\nDISCUSSION: Staff will provide a status update on the following active projects in the\nFiscal Year 2020-2021 Capital Improvement Program:\n\nCapital Improvement Projects (Design)\n\nMarie Canyon Green Streets\n(cid:190) Updates:\n\n(cid:131) The City has recently received Measure W funds to complete this\nproject. Staff is working on the project plans to prepare for public\nbidding.\n\n(cid:190) Project Schedule:', '(cid:190) Project Description: This project will be funded through a grant from FEMA\nafter the Woolsey Fire. The City will create a complete inventory of storm\ndrains, culverts, debris basins, manholes, and other drainage structures\nwithin the City.\n\n(cid:190) Estimated Schedule:\n\n(cid:131) Completion Date: Spring 2022\n\nPage 6 of 6\n\nAgenda Item # 4.A.']
# paragraph = '. '.join(paragraph)

# # Process the paragraph
# doc = nlp(paragraph)

# # Extract sentences
# sentences = [sent.text for sent in doc.sents]
# for sentence in sentences:
#     print(sentence)
#     print("-"*50)
# # sometimes leave (cid: xxx) as single sentence


# def get_token_num(text:str):
#     import re
#     words = re.findall(r'\b\w+\b', text)
#     return len(words)

# from textblob import TextBlob
# from nltk import sent_tokenize


# # Example paragraph
# paragraphs = [
#         "forums \nsites \n(http://slifelabs.com  and  http://moodjam.org).  We  chose \nthese  web  sites  because  their  readers  and  users  were  more \nlikely  to  have  used  one  or  more  personal  informatics \nsystems. Survey participants were entered into a raffle for a \n$25  Amazon  gift  certificate.  We  interviewed  a  subset  of \nto  collect \nthese  participants  using \ninstant  messenger \nadditional  details  about \ntheir  responses.  Interviewees \nreceived an additional $10 Amazon gift certificate.",
#         "2.  Assogba,  Y.,  and  Donath,  J.  Mycrocosm:  Visual \n\nMicroblogging. HICSS'09, 2009, pp. 1-10. \n\n3.  Consolvo,  S.,  McDonald,  D.W.,  Toscos,  T.,  et  al. \nActivity  Sensing  in  the  Wild:  A  Field  Trial  of  Ubifit \nGarden. CHI‘08, 2008, pp. 1797-1806. \n\n4.  Froehlich, J., Dillahunt, T., Klasnja, P., et al. Ubigreen: \nfor  Tracking  and \n\nInvestigating  a  Mobile  Tool \n\nSupporting Green Transportation Habits. CHI’09, 2009, \npp. 1043-1052. \n\n5.  Franklin, B. Autobiography of Benjamin Franklin. New \n\nYork, 1916, pp. 146-155. \n\n6.  Frost, J. and Smith, B.K. Visualizing Health: imagery in \n\ndiabetes education. DUX ’03, 2003, pp. 1-14. \n\n7.  Gemmell,  J.,  Bell,  G.,  and  Lueder,  R.  MyLifeBits:  a \npersonal  database  for  everything.  Communications  of \nthe ACM, 2006, pp. 88-95.",
#         "Permission  to  make  digital  or  hard  copies  of  all  or  part  of  this  work  for \npersonal or classroom use is granted without fee provided that copies are \nnot made or distributed for profit or commercial advantage and that copies \nbear this notice and the full citation on the first page. To copy otherwise, \nor  republish,  to  post  on  servers  or  to  redistribute  to  lists,  requires  prior \nspecific permission and/or a fee. \nCHI 2010, April 10–15, 2010, Atlanta, Georgia, USA. \nCopyright 2010 ACM  978-1-60558-929-9/10/04....$10.00. \n\nto \n\ninformation  brought  by \n\nbecause  of  advances  in  sensor  technologies,  ubiquity  of \nthe  Internet,  and \naccess \nimprovements  in  visualizations.  A  class  of  systems  called \npersonal  informatics  is  appearing  that  help  people  collect \nand \n(e.g.,  Mint, \nhttp://mint.com, for finance and Nike+, http://nikeplus.com, \nfor physical activity). \n\nreflect  on  personal \n\ninformation \n\ninform  people  about",
#         "19. Pousman,  Z.,  Stasko,  J.T.,  and  Mateas,  M.  Casual \nInformation  Visualization:  Depictions  of  Data \nin \nEveryday Life. IEEE Transactions on Visualization and \nComputer Graphics, 2002, pp. 1145-1152. \n\n20. Scollon,  C.,  Kim-Prieto,  C.,  and  Diener,  E.  Experience \nSampling:  Promises  and  Pitfalls,  Strengths  and \nWeaknesses. Journal of Happiness Studies, 4, 2003, pp. \n5-34. \n\n21. Wolf,  G.  Know  Thyself:  Tracking  Every  Facet  of  Life, \nfrom  Sleep  to  Mood  to  Pain,  24/7/365.  Wired,  17.07, \n2009, pp. 92-95. \n\n22. Yau,  N. and Schneider,  J.  Self-Surveillance.  Bulletin of \n\nASIS&T, June/July 2009, pp. 24-30. \n\nCHI 2010: Performance, Stagecraft, and MagicApril 10–15, 2010, Atlanta, GA, USA566",
#         "these  properties,  we  recommend \n\nAuthor Keywords \nPersonal informatics, collection, reflection, model, barriers \n\nACM Classification Keywords \nH5.m.  Information  interfaces  and  presentation  (e.g.,  HCI): \nMiscellaneous.  \n\nGeneral Terms \nDesign, Human Factors \n\nINTRODUCTION AND MOTIVATION \nThe  importance  of  knowing  oneself  has  been  known  since \nancient  times.  Ancient  Greeks  who  pilgrimaged  to  the \nTemple  of  Apollo  at  Delphi  to  find  answers  were  greeted \nwith  the  inscription  “Gnothi  seauton”  or  “Know  thyself”. \nTo  this  day,  people  still  strive  to  obtain  self-knowledge. \nOne way to obtain self-knowledge is to collect information \nabout  oneself—one’s  behaviors,  habits,  and  thoughts—and \nreflect  on  them.  Computers  can  facilitate  this  activity"
#     ]

#     # in this case, the last sentence in new_sentences may be < 25. ( after + still < 25)

            
#     for sentence in new_sentences:
#         if get_token_num(sentence) >= 25:
#             # sentences1_new.append(sentence)
#             print("*"*50)
#             print(sentence)
#             print("*"*50)
#         else:
#             print("-"*50)
#             print(sentence)
#             print("-"*50)
#     print('<'*50)
#     print('>'*50)
        




# # purely using  . to split, but no individual word is splitted. automatically remove  multiple \n within para 


# from transformers import pipeline

# # Load a pre-trained model for sentence segmentation
# tokenizer = pipeline('sentiment-analysis')

# # Example paragraph
# paragraph = "This is the first sentence. Here's another sentence! And the third sentence follows."

# # Tokenize into sentences
# sentences = tokenizer(paragraph, truncation=True)
# for sentence in sentences:
#     print(sentence)
#     print("-"*50)



# import stanza

# # 下载并初始化斯坦福NLP模型
# stanza.download('en')
# nlp = stanza.Pipeline('en')

# # 示例段落
# paragraph = ['(cid:131) The contractor is also working on the curb, gutter and storm drain\ninstallation on Civic Center Way from Webb Way to the condos. This\nportion of the work may require temporary road closures. However, it\nis anticipated that this phase of the project will be completed at the\nend of February 2021.\n\n(cid:190) Project Schedule: August 2020 through March 2021\n\nPage 3 of 6\n\nAgenda Item # 4.A.\n\n\n\n\n\n\n\n\nCapital Improvement Projects (Not Started)\n\nAnnual Street Maintenance\n\n(cid:190) Project Description: This project provides for the reconstruction and\n\nmaintenance of City streets.\n\n(cid:190) Estimated Schedule:\n\n(cid:131) Complete Design: Spring 2021\n(cid:131) Begin Construction: Summer 2021\n\nBluffs Park Shade Structure\n\n(cid:190) Project Description: This project consists of the installation of four single-\n\npost shade structures at Malibu Bluffs Park\n\n(cid:190) Estimated Schedule:\n\n(cid:131) Complete Design: Summer 2021\n(cid:131) Begin Construction: Fall 2021', '(cid:131) The project assessment engineer has begun\n\nthe process of\n\nevaluating the project costs.\n\n(cid:131) Next public community meeting is scheduled for March 25th.\n\n(cid:190) Project Schedule:\n\n(cid:131) Complete Design: December 2021\n(cid:131) Begin Construction: March 2022\n\nPage 2 of 6\n\nAgenda Item # 4.A.\n\n\n\n\n\n\n\n\n\n\nMalibu Park Drainage Improvements\n\n(cid:190) Updates:\n\n(cid:131) Staff is making minor modifications to the project plans to reduce the\n\noverall project costs.\n\n(cid:131) Project is scheduled to go out to bid next week.\n\n(cid:190) Project Schedule:\n\n(cid:131) Complete Design: February 2021\n(cid:131) Begin Construction: April 2021\n\nCapital Improvement Projects (Construction)\n\nCity Hall Roof Replacement\n\n(cid:190) Updates: The City has held project meetings with the contractor and is\n\ndeveloping a project schedule.\n\n(cid:190) Project Schedule: February – April 2021\n\nBluffs Park Workout Station', '(cid:190) Updates: The contractor is waiting for the delivery of the new workout\nstation equipment. The equipment is anticipated to be delivered at the end\nof February.\n\n(cid:190) Project Schedule: November 2020 – March 2021\n\nCivic Center Way Improvements\n\n(cid:190) Updates:\n\n(cid:131) Work Hours: Monday through Friday 7:00AM to 4:00PM, Saturdays\n\n7:00AM to 4:00PM\n\n(cid:131) The contractor is currently working at the section between Vista\nPacifica and the condos on Civic Center Way. This phase of work will\nrequire the temporary closure of Civic Center Way. Portions of the\ncurb and gutter have been placed and the contactor is working on the\nproposed retaining wall. This portion of work is anticipated to be\ncompleted in early February 2021.', 'Public Works Commission\nAgenda Report\n\nPublic Works\nCommission Meeting\n03-02-21\nItem\n4.A.\n\nTo:\n\nChair Merrick and Members of the Public Works Commission\n\nPrepared by:\n\nRobert DuBoux, Public Works Director/City Engineer\n\nDate prepared: February 18, 2021\n\nMeeting date: March 2, 2021\n\nSubject:\n\nCapital Improvement Projects and Disaster Recovery Projects Status\nReport\n\nRECOMMENDED ACTION: Receive and file report on the status of the City’s current and\nupcoming Capital Improvements Projects and Disaster Recovery Projects.\n\nDISCUSSION: Staff will provide a status update on the following active projects in the\nFiscal Year 2020-2021 Capital Improvement Program:\n\nCapital Improvement Projects (Design)\n\nMarie Canyon Green Streets\n(cid:190) Updates:\n\n(cid:131) The City has recently received Measure W funds to complete this\nproject. Staff is working on the project plans to prepare for public\nbidding.\n\n(cid:190) Project Schedule:', '(cid:190) Project Description: This project will be funded through a grant from FEMA\nafter the Woolsey Fire. The City will create a complete inventory of storm\ndrains, culverts, debris basins, manholes, and other drainage structures\nwithin the City.\n\n(cid:190) Estimated Schedule:\n\n(cid:131) Completion Date: Spring 2022\n\nPage 6 of 6\n\nAgenda Item # 4.A.']
# paragraph = '. '.join(paragraph)

# # 处理段落
# doc = nlp(paragraph)

# # 提取句子
# sentences = [sentence.text for sentence in doc.sentences]
# for sentence in sentences:
#     print(sentence)
#     print("-"*50)
# result: tend to break a sentence



# from stanfordcorenlp import StanfordCoreNLP

# # 初始化StanfordCoreNLP
# nlp = StanfordCoreNLP('./stanford-corenlp-full-2018-10-05')

# # # 示例段落
# paragraph = ['(cid:131) The contractor is also working on the curb, gutter and storm drain\ninstallation on Civic Center Way from Webb Way to the condos. This\nportion of the work may require temporary road closures. However, it\nis anticipated that this phase of the project will be completed at the\nend of February 2021.\n\n(cid:190) Project Schedule: August 2020 through March 2021\n\nPage 3 of 6\n\nAgenda Item # 4.A.\n\n\n\n\n\n\n\n\nCapital Improvement Projects (Not Started)\n\nAnnual Street Maintenance\n\n(cid:190) Project Description: This project provides for the reconstruction and\n\nmaintenance of City streets.\n\n(cid:190) Estimated Schedule:\n\n(cid:131) Complete Design: Spring 2021\n(cid:131) Begin Construction: Summer 2021\n\nBluffs Park Shade Structure\n\n(cid:190) Project Description: This project consists of the installation of four single-\n\npost shade structures at Malibu Bluffs Park\n\n(cid:190) Estimated Schedule:\n\n(cid:131) Complete Design: Summer 2021\n(cid:131) Begin Construction: Fall 2021', '(cid:131) The project assessment engineer has begun\n\nthe process of\n\nevaluating the project costs.\n\n(cid:131) Next public community meeting is scheduled for March 25th.\n\n(cid:190) Project Schedule:\n\n(cid:131) Complete Design: December 2021\n(cid:131) Begin Construction: March 2022\n\nPage 2 of 6\n\nAgenda Item # 4.A.\n\n\n\n\n\n\n\n\n\n\nMalibu Park Drainage Improvements\n\n(cid:190) Updates:\n\n(cid:131) Staff is making minor modifications to the project plans to reduce the\n\noverall project costs.\n\n(cid:131) Project is scheduled to go out to bid next week.\n\n(cid:190) Project Schedule:\n\n(cid:131) Complete Design: February 2021\n(cid:131) Begin Construction: April 2021\n\nCapital Improvement Projects (Construction)\n\nCity Hall Roof Replacement\n\n(cid:190) Updates: The City has held project meetings with the contractor and is\n\ndeveloping a project schedule.\n\n(cid:190) Project Schedule: February – April 2021\n\nBluffs Park Workout Station', '(cid:190) Updates: The contractor is waiting for the delivery of the new workout\nstation equipment. The equipment is anticipated to be delivered at the end\nof February.\n\n(cid:190) Project Schedule: November 2020 – March 2021\n\nCivic Center Way Improvements\n\n(cid:190) Updates:\n\n(cid:131) Work Hours: Monday through Friday 7:00AM to 4:00PM, Saturdays\n\n7:00AM to 4:00PM\n\n(cid:131) The contractor is currently working at the section between Vista\nPacifica and the condos on Civic Center Way. This phase of work will\nrequire the temporary closure of Civic Center Way. Portions of the\ncurb and gutter have been placed and the contactor is working on the\nproposed retaining wall. This portion of work is anticipated to be\ncompleted in early February 2021.', 'Public Works Commission\nAgenda Report\n\nPublic Works\nCommission Meeting\n03-02-21\nItem\n4.A.\n\nTo:\n\nChair Merrick and Members of the Public Works Commission\n\nPrepared by:\n\nRobert DuBoux, Public Works Director/City Engineer\n\nDate prepared: February 18, 2021\n\nMeeting date: March 2, 2021\n\nSubject:\n\nCapital Improvement Projects and Disaster Recovery Projects Status\nReport\n\nRECOMMENDED ACTION: Receive and file report on the status of the City’s current and\nupcoming Capital Improvements Projects and Disaster Recovery Projects.\n\nDISCUSSION: Staff will provide a status update on the following active projects in the\nFiscal Year 2020-2021 Capital Improvement Program:\n\nCapital Improvement Projects (Design)\n\nMarie Canyon Green Streets\n(cid:190) Updates:\n\n(cid:131) The City has recently received Measure W funds to complete this\nproject. Staff is working on the project plans to prepare for public\nbidding.\n\n(cid:190) Project Schedule:', '(cid:190) Project Description: This project will be funded through a grant from FEMA\nafter the Woolsey Fire. The City will create a complete inventory of storm\ndrains, culverts, debris basins, manholes, and other drainage structures\nwithin the City.\n\n(cid:190) Estimated Schedule:\n\n(cid:131) Completion Date: Spring 2022\n\nPage 6 of 6\n\nAgenda Item # 4.A.']
# paragraph = '. '.join(paragraph)
# print(paragraph)
# # 分割成句子
# sentences = nlp.sent_tokenize(paragraph)
# for sentence in sentences:
#     print(sentence)

# # 关闭NLP服务
# nlp.close()
# Item # 4.A. will be break



# from transformers import pipeline

# # 初始化用于句子分割的管道
# nlp = pipeline("sentiment-analysis")

# # 输入段落
# paragraph = """
# Hugging Face's transformers library is an amazing tool for NLP tasks. 
# It provides pre-trained models for various tasks such as text classification, question answering, and text generation. 
# With just a few lines of code, you can get state-of-the-art results on many benchmarks.
# """

# # 使用管道将段落分割成句子
# sentences = nlp.tokenizer.tokenize(paragraph, return_tensors='pt', padding=True, truncation=True)
# print(sentences)
# decoded_sentences = [nlp.tokenizer.decode(sentence, skip_special_tokens=True) for sentence in sentences]

# # # 输出结果
# for sentence in decoded_sentences:
#     print(sentence)
# unable to run


# from nltk.tokenize import word_tokenize
# paragraph = ['(cid:131) The contractor is also working on the curb, gutter and storm drain\ninstallation on Civic Center Way from Webb Way to the condos. This\nportion of the work may require temporary road closures. However, it\nis anticipated that this phase of the project will be completed at the\nend of February 2021.\n\n(cid:190) Project Schedule: August 2020 through March 2021\n\nPage 3 of 6\n\nAgenda Item # 4.A.\n\n\n\n\n\n\n\n\nCapital Improvement Projects (Not Started)\n\nAnnual Street Maintenance\n\n(cid:190) Project Description: This project provides for the reconstruction and\n\nmaintenance of City streets.\n\n(cid:190) Estimated Schedule:\n\n(cid:131) Complete Design: Spring 2021\n(cid:131) Begin Construction: Summer 2021\n\nBluffs Park Shade Structure\n\n(cid:190) Project Description: This project consists of the installation of four single-\n\npost shade structures at Malibu Bluffs Park\n\n(cid:190) Estimated Schedule:\n\n(cid:131) Complete Design: Summer 2021\n(cid:131) Begin Construction: Fall 2021', '(cid:131) The project assessment engineer has begun\n\nthe process of\n\nevaluating the project costs.\n\n(cid:131) Next public community meeting is scheduled for March 25th.\n\n(cid:190) Project Schedule:\n\n(cid:131) Complete Design: December 2021\n(cid:131) Begin Construction: March 2022\n\nPage 2 of 6\n\nAgenda Item # 4.A.\n\n\n\n\n\n\n\n\n\n\nMalibu Park Drainage Improvements\n\n(cid:190) Updates:\n\n(cid:131) Staff is making minor modifications to the project plans to reduce the\n\noverall project costs.\n\n(cid:131) Project is scheduled to go out to bid next week.\n\n(cid:190) Project Schedule:\n\n(cid:131) Complete Design: February 2021\n(cid:131) Begin Construction: April 2021\n\nCapital Improvement Projects (Construction)\n\nCity Hall Roof Replacement\n\n(cid:190) Updates: The City has held project meetings with the contractor and is\n\ndeveloping a project schedule.\n\n(cid:190) Project Schedule: February – April 2021\n\nBluffs Park Workout Station', '(cid:190) Updates: The contractor is waiting for the delivery of the new workout\nstation equipment. The equipment is anticipated to be delivered at the end\nof February.\n\n(cid:190) Project Schedule: November 2020 – March 2021\n\nCivic Center Way Improvements\n\n(cid:190) Updates:\n\n(cid:131) Work Hours: Monday through Friday 7:00AM to 4:00PM, Saturdays\n\n7:00AM to 4:00PM\n\n(cid:131) The contractor is currently working at the section between Vista\nPacifica and the condos on Civic Center Way. This phase of work will\nrequire the temporary closure of Civic Center Way. Portions of the\ncurb and gutter have been placed and the contactor is working on the\nproposed retaining wall. This portion of work is anticipated to be\ncompleted in early February 2021.', 'Public Works Commission\nAgenda Report\n\nPublic Works\nCommission Meeting\n03-02-21\nItem\n4.A.\n\nTo:\n\nChair Merrick and Members of the Public Works Commission\n\nPrepared by:\n\nRobert DuBoux, Public Works Director/City Engineer\n\nDate prepared: February 18, 2021\n\nMeeting date: March 2, 2021\n\nSubject:\n\nCapital Improvement Projects and Disaster Recovery Projects Status\nReport\n\nRECOMMENDED ACTION: Receive and file report on the status of the City’s current and\nupcoming Capital Improvements Projects and Disaster Recovery Projects.\n\nDISCUSSION: Staff will provide a status update on the following active projects in the\nFiscal Year 2020-2021 Capital Improvement Program:\n\nCapital Improvement Projects (Design)\n\nMarie Canyon Green Streets\n(cid:190) Updates:\n\n(cid:131) The City has recently received Measure W funds to complete this\nproject. Staff is working on the project plans to prepare for public\nbidding.\n\n(cid:190) Project Schedule:', '(cid:190) Project Description: This project will be funded through a grant from FEMA\nafter the Woolsey Fire. The City will create a complete inventory of storm\ndrains, culverts, debris basins, manholes, and other drainage structures\nwithin the City.\n\n(cid:190) Estimated Schedule:\n\n(cid:131) Completion Date: Spring 2022\n\nPage 6 of 6\n\nAgenda Item # 4.A.']
# paragraph = '. '.join(paragraph)
# words = word_tokenize(paragraph)
# print(words)


# from transformers import BertTokenizer

# # 加载BERT的分词器
# tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# # 词级分词
# tokens = tokenizer.tokenize(paragraph)
# print(tokens)

# # 将词转换为ID
# token_ids = tokenizer.convert_tokens_to_ids(tokens)
# print(token_ids)

# a = [
#         "The design plans were approved by Planning Commission on September 20, 2021.",
#         "At the December 13, 2021, City Council meeting, Council directed staff to withdraw the proposed project and associated Coastal Development Permit and directed the Public Works and Public Safety Commissions to develop project alternatives.",
#         "A joint Public Works and Public Safety Commission meeting was held on January 20, 2022.",
#         "Project alternatives will be presented to the commissions at a future date.",
#         "Individual letters were mailed to all properties within Phase 2 with their preliminary estimated assessments.",
#         "Staff has been communicating with the property owners regarding their proposed assessments.",
#         "The Trancas Canyon Park Slope Stabilization Project consultant has started the design of this project.",
#         "Council approved an agreement in December for design services for the Storm Drain Master Plan project.",
#         "A kick-off meeting was held in late December for the Storm Drain Master Plan project.",
#         "The project was approved by the Planning Commission on September 8, 2021, and it is anticipated to have final approval by March 2022.",
#         "The City has hired a consultant to design this project.",
#         "The design has started and is anticipated to be completed by the Spring of 2022.",
#         "This project is currently under design with the City’s consultant.",
#         "It is anticipated that the final design will be complete by July 2022.",
#         "The project will be advertised for construction bids with construction beginning in Fall 2022."
#     ]
# print(get_token_num_for_list(a))

# b = [
#         "Public Works Commission\nAgenda Report\n\nPublic Works\nCommission Meeting\n10-27-21\nItem\n4.A.\n\nTo:\n\nChair Simmens and Members of the Public Works Commission\n\nPrepared by:\n\nTroy Spayd, Assistant Public Works Director/City Engineer\n\nApproved by:\n\nRob DuBoux, Public Works Director/City Engineer\n\nDate prepared: October 21, 2021\n\nMeeting date: October 27, 2021\n\nSubject:\n\nCapital Improvement Projects and Disaster Recovery Projects Status\nReport\n\nRECOMMENDED ACTION: Receive and file report on the status of the City’s current and\nupcoming Capital Improvements Projects and Disaster Recovery Projects.\n\nDISCUSSION: Staff will provide a status update on the following active projects in the\nFiscal Year 2021-2022 Capital Improvement Program:\n\nCapital Improvement Projects (Design)\n\nMarie Canyon Green Streets\n(cid:190) Updates:",
#         "Westward Beach Road Improvements Project\n\n(cid:190) Updates:\n\n(cid:131) The design plans were approved by Planning Commission on\nSeptember 20, 2021. At the December 13, 2021, City Council meeting,\nCouncil directed staff to withdraw the proposed project and associated\nCoastal Development Permit and directed the Public Works and Public\nSafety Commissions\nto develop project\nalternatives. A joint Public Works and Public Safety Commission\nmeeting was held on January 20, 2022. Project alternatives will be\npresented to the commissions at a future date.\n\nthe project\n\nto review\n\n(cid:190) Project Schedule:\n\n(cid:131) Complete Design: Spring 2022\n(cid:131) Begin Construction: Summer/Winter 2022\n\nCivic Center Water Treatment Facility Phase 2\n\n(cid:190) Updates:\n(cid:131)\n\nIndividual letters were mailed to all properties within Phase 2 with their\npreliminary estimated assessments. Staff has been communicating\nwith the property owners regarding their proposed assessments.",
#         "Broad Beach Road Water Quality Infrastructure Repairs (CalJPIA Project)\n\n(cid:190) Updates:\n\n(cid:131) The project consultant prepared the specifications for the project. Staff\n\nis finalizing the bid documents.\n\n(cid:190) Project Schedule:\n\n(cid:131) Complete Design: February 2022\n(cid:131) Begin Construction: Spring 2022\n\nLatigo Canyon Road Roadway/Retaining Wall Improvements (FEMA Project)\n\n(cid:190) Updates:\n\n(cid:131) Staff is finalizing the design of this project.\n(cid:131) Staff is also working with FEMA/CalOES to substitute the existing\n\ntimber with non-combustible materials.\n\n(cid:190) Project Schedule\n\n(cid:131) Complete Design: February 2022\n(cid:131) Begin Construction: April 2022\n\nTrancas Canyon Park Planting and Irrigation Repairs (CalJPIA/FEMA Project)\n\n(cid:190) Updates:\n\n(cid:131) The project consultant has started the design of this project.\n\n(cid:190) Project Schedule:\n\n(cid:131) Complete Design: Spring 2022\n(cid:131) Begin Construction: Spring 2022",
#         "(cid:190) Project Description: This project was identified in the 2015 PCH Safety Study\nand includes installing new raised medians and improvements. New raised\nmedians are proposed east and west of PCH and Paradise Cove Road. The\nproposed improvements also include the relocation of the existing bus stop\nand new signage. The project will also include the installation of new raised\nmedians on PCH in the areas where the double yellow lines exist in the vicinity\nof Zuma Beach, specifically where the yellow paddles are installed.\n\nCapital Improvement Projects (Completed)\n\nCivic Center Way Improvements\n\n(cid:190) Updates: The contractor has completed the planting material maintenance\nperiod as described within the project documents. Council accepted this\nproject as complete at the September 13th City Council Meeting.\n\nCivic Center Stormwater Diversion Structure",
#         "(cid:190) Updates: The contractor has completed the storm drain improvements in the\nCivic Center Way are. The improvements modified the existing concrete\nchannel underneath Civic Center Way by adding a 3’ concrete curb adjacent\nto the existing flap gates. The new curb prevents brackish water intrusion\n\nPage 4 of 8\n\nAgenda Item # 4.A.\n\n\n\n\n\n\n\n\n\n\n\n\ninto the City’s Civic Center Stormwater Treatment Facility. This project is\nscheduled to be accepted by the Council at the January 24, 2022 meeting.\n\n2021 Annual Street Maintenance\n\n(cid:190) Updates: This project included resurfacing Malibu Road, Broad Beach Road,\nLatigo Canyon Road, Corral Canyon Road, Webb Way, Rambla Pacifico\nStreet and Vista Pacifica with a slurry seal treatment and adding speed\nhumps to Birdview Avenue. This project was identified in the City’s Pavement\nManagement Plan. This project is scheduled to be accepted by the Council\nat the January 24, 2022 meeting.\n\nDisaster Projects (Design)"
#     ] # baseline1
# print(get_token_num_for_list(b))