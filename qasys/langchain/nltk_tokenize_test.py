import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

para = "(cid:190) Updates:\n\n(cid:131) The project consultant has started the design of this project.\n\n(cid:190) Project Schedule:\n\n(cid:131) Complete Design: Spring 2022\n(cid:131) Begin Construction: Summer 2022\n\nTrancas Canyon Park Slope Stabilization Project (CalJPIA Project)\n\n(cid:190) Updates:\n\n(cid:131) The project consultant has started the design of this project.\n\n(cid:190) Project Schedule:\n\n(cid:131) Complete Design: Spring 2022\n(cid:131) Begin Construction: Summer 2022\n\nStorm Drain Master Plan (FEMA Project)\n\n(cid:190) Project Description: This project is funded through a grant from FEMA after\nthe Woolsey Fire. The City will create a complete inventory of storm drains,\nculverts, debris basins, manholes, and other drainage structures within the\nCity.\n\n(cid:190) Updates: Council approved an agreement in December for design services.\n\nA kick-off meeting was held in late December.\n\n(cid:190) Estimated Schedule:\n\n(cid:131) Completion Date: Spring 2022"
# Tokenize the paragraph into sentences
sentences = sent_tokenize(para)
for sentence in sentences:
    print(sentence)
    print('-'*50)