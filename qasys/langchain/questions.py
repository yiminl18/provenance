def civic_q():
    q = []
    q.append('What are the names of mentioned capital improvement projects?')
    q.append('What are the names of projects starting before 2022?')
    q.append('What are the names of projects that were completed before 2022?')
    q.append('What are the names of disaster projects starting later than 2022?')
    q.append('What are the names of disaster projects advertised before 2023')

    return q

def paper_q():
    q = []
    q.append('How many authors are there for this paper?')
    q.append('What is the publication year of this paper?')
    q.append('What are the names of authors whose institutions are in the US?')
    q.append('What is the publication venue of this paper? (e.g. CHI, CSCW, etc.)')
    q.append('Does this paper involve the theory “A Model of Personal Informatics”?')
    return q

def notice_q():
    q = []
     
    q.append('What is the issue date of the notice?')
    q.append('What are the violation codes for the items listed in this notice?')
    q.append('What is the name of the company being informed later than 2023 and located in California?')
    q.append('What is the name of the company receiving the notice with a non-zero civil penalty?')
    q.append('What is the name of the company receiving the notice that has proposed compliance and a warning?')
    return q

def civic_path():
    q = []
    q.append('data/civic/raw_data/malibucity_agenda__01262022-1835.pdf')
    q.append('data/civic/raw_data/malibucity_agenda__01272021-1626.pdf')
    q.append('data/civic/raw_data/malibucity_agenda__03022021-1648.pdf')
    q.append('data/civic/raw_data/malibucity_agenda__03232022-1869.pdf')
    q.append('data/civic/raw_data/malibucity_agenda__03242021-1665.pdf')
    q.append('data/civic/raw_data/malibucity_agenda__04282021-1687.pdf')
    return q

def paper_path():
    q = []
    q.append('data/paper/raw_data/A Lived Informatics Model of Personal Informatics.pdf')
    q.append('data/paper/raw_data/Reviewing Reflection: On the Use of Reflection in Interactive System Design.pdf')
    q.append('data/paper/raw_data/When Personal Tracking Becomes Social: Examining the Use of Instagram for Healthy Eating.pdf')
    # has ground truth for theroy question
    q.append('data/paper/raw_data/A Stage-based Model of Personal Informatics Systems.pdf')
    q.append('data/paper/raw_data/A Trip to the Moon: Personalized Animated Movies for Self-reflection.pdf')
    q.append('data/paper/raw_data/A Wee Bit More Interaction: Designing and Evaluating an Overactive Bladder App.pdf')
    # no ground truth for theroy question
    return q

def notice_path():
    q = []
    q.append('data/NoticeViolation/raw_data/12023008NOPV_PCO PCP_06152023_(20-187757)_text.pdf')
    q.append('data/NoticeViolation/raw_data/12023011NOPV_PCP_05052023_(21-207810)_text.pdf')
    q.append('data/NoticeViolation/raw_data/12023013NOPV_PCO PCP_05042023_(22-233209)_text.pdf')
    q.append('data/NoticeViolation/raw_data/12023022NOPV_PCO_04132023_(22-234207)_text.pdf')
    q.append('data/NoticeViolation/raw_data/12023027NOPV_PCP_06012023_(21-199435)_text.pdf')
    q.append('data/NoticeViolation/raw_data/12023028NOPV_PCO_05252023_(22-232998)_text.pdf')
    return q
