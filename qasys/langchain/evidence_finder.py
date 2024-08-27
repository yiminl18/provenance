from model import model
from pretrain_sentence_splitter import nltk_sent_tokenize

def jaccard_similarity_word_intersection(str1: str, str2:str):
    """
    Compute the Jaccard similarity between two strings by counting the number of common words.

    Parameters:
    str1 (str): The first string
    str2 (str): The second string

    Returns:
    float: The Jaccard similarity
    """
    # Split the strings into words
    words1 = set(str1.split())
    words2 = set(str2.split())
    
    # Compute the intersection and union of the two sets
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    # Compute the Jaccard similarity
    if len(union) == 0:
        return 0.0  # Prevent division by zero
    jaccard_sim = len(intersection) / min(len(words1), len(words2))
    return jaccard_sim

def find_evidence(Q: str, A: str, P: str, model_name = 'gpt35'):
    
    
    instruction = 'Given the following question: ##' + Q + '##, and the answer to the question: ##' +\
    A + '##. Return a set of sentences from the following description that can provide evidence for the given answer to the given question.' +\
    'These sentences must be raw text from the given descriptions. Each sentence needs to be a whole sentence ending with a period or other punctuation mark, but cannot end with a comma. Do not create new words or sentences. ##' +\
    P +'##. Concatenate multiple evidences to a string. If no evidence can be found, return None.'
    text = ''

    # version 0
    
    # instruction = """You are an expert in identifying evidence. Given a question Q, its answer A, and a relevant text span P, your task is to find one or more Attention Text Span(s) that lead to the answer A. An Attention Text Span is a sub-span within P that directly contributes to answering Q and generating A. The returned Attention Text Span(s) should be as concise as possible and MUST BE RAW TEXT EXTRACTED FROM P.
    # Now, I will provide you with Q, A, and P. 
    # ###
    # Return format requirements:
    # - If you find one or more Attention Text Span(s) in P that lead to A, please return the Attention Text Span(s) as a list like ['Hi how are you', 'I am fine thank you']. 
    # - If no Attention Text Span(s) can be found, please only return None.
    # ###
    # Now give me your List:
    # """
    #text = f"Question: {Q}\nAnswer: {A}\nDescription: {P}"
    
    prompt = (instruction,text)
    response = model(model_name,prompt) # response is a string
    result = []
    
    result = response
    flag = True
    None_list = ['None', 'none', 'NONE', 'None.', '##None##', 'None##', '##None', 'None##.', '##None##.', 'None.', 'None.##', '##None.'] # list of strings
    if response in None_list:
        result =''
        flag = False
        return '', '', response, False

    original_result = nltk_sent_tokenize(result, 5) # unfiltered, may be hallucinated
    filtered_result = []
    for r in original_result:
        if jaccard_similarity_word_intersection(r, P) > 0.7:
            prefix_to_remove = '- '
            r = r[len(prefix_to_remove):] if r.startswith(prefix_to_remove) else r
            filtered_result.append(r)

    return filtered_result, original_result, response, flag # result is a list of strings, response is a string, flag is a boolean

# # test
# Q = "What is the publication venue of this paper? (e.g. CHI, CSCW, etc.)"
# A = "CHI"
# P = [
#         "92.Tomico, O., Frens, J.W., and Overbeeke, K.C.J. (2009). \nCo-reflection: user involvement for highly dynamic \ndesign processes. Proc CHI Ext. Abst., 2695-2698.\n\n93.Tseng, T. and Bryant, C. (2013). Design, reflect, \nexplore: encouraging children's reflections with \nmechanix. Proc CHI Ext. Abst., 619-624.\n\n94.Valkanova, N., Jorda, S., Tomitsch, M., and Moere, A.V.\n(2013). Reveal-it!: the impact of a social visualization \nprojection on public awareness and discourse. Proc CHI,\n3461-3470.\n\n95.van Dijk, J., van der Roest, J., van der Lugt, R., and \nOverbeeke, K.C.J. 2011. NOOT: a tool for sharing \nmoments of reflection during creative meetings. Proc \nC&C, 157-164.\n\n96.Vygotsky, L. S. (1978). Mind and Society. Cambridge, \n\nMA: Harvard University Press.\n\n97.Wallace, J., Wright, P.C., McCarthy, J., Green, D.P., \n\nThomas, J., and Olivier, P. (2013). A design-led inquiry \ninto personhood in dementia. Proc CHI, 2617-2626.",
#         "ubicomp technologies. Proc UbiComp, 405-414.\n\n57.Li, I., Forlizzi, J., and Dey, A.K. (2010). Know thyself: \nmonitoring and reflecting on facets of one's life. Proc \nCHI Ext. Abst., 4489-4492.\n\n58.Li, I., Froehlich, J., Larsen, J.E., Grevet, C., and \n\nRamirez, E. (2013). Personal informatics in the wild. \nProc CHI Ext. Abst., 3179-3182.\n\n59.Li, I., Medynskiy, Y., Froehlich, J., and Larsen, J.E. \n\n(2012). Personal informatics in practice. Proc CHI Ext. \nAbst., 2799-2802.\n\n60.Lindley, S.E., Harper, R., and Sellen, A. (2009). \n\nDesiring to be in touch in a changing communications \nlandscape. Proc CHI, 1693-1702.\n\n61.Loke, L. and Robertson, T. (2009). Design \n\nrepresentations of moving bodies for interactive, \nmotion-sensing spaces. Int. J. Hum.-Comput. Stud., \n67(4), 394-410.\n\n62.Malacria, S., Scarr, J., Cockburn, A., Gutwin, C., and \nGrossman, T. (2013). Skillometers: reflective widgets \nthat motivate and help users to improve performance. \nProc UIST, 321-330.",
#         "41.Irani, L., Vertesi, J., Dourish, P., Philip, K., & Grinter, R.\nE. (2010). Postcolonial computing: a lens on design and \ndevelopment. Proc CHI, 1311–1320.\n\n42.Isaacs, E., Konrad, A., Walendowski, A., Lennig, T, \nHollis, V, and Whittaker, S. (2013). Echoes from the \npast: how technology mediated reflection improves \nwell-being. Proc CHI, 1071-1080.\n\n43.Johnston, A., Amitani, S., and Edmonds, E. (2005). \n\nAmplifying reflective thinking in musical performance. \nProc C&C, 166-175.\n\n44.Jones, J., Hall, S., Gentis, M., Reynolds, C., Gadwal, C.,\n\nHurst, A., Ronch, J., and Neylan, C. (2012). \nVisualizations for self-reflection on mouse pointer \nperformance for older adults. Proc ASSETS, 287-288.\n\n45.Joslyn, S. L., & Oakes, M. A. (2005). Directed \n\nforgetting of autobiographical events. Memory & \nCognition, 33(4), 577–587.\n\n46.Kannabiran, G., Bardzell, J., & Bardzell, S. (2011). How\n\nHCI Talks about Sexuality. Proc CHI, 695–704.",
#         "34.Hansen, N.B. and Dalsgaard, P. (2012). The productive \nrole of material design artefacts in participatory design \nevents. Proc NordiCHI, 665-674.\n\n35.Harrison, S., Sengers, P., & Tatar, D. (2011). Making \nepistemological trouble: Third-paradigm HCI as \nsuccessor science. Interacting with Computers, 23(5), \n385–392.\n\n36.Hebert, M.G. (2009). Vehicle #3: heliotropic furniture - \n\nan autonomous installation. Proc C&C, 465-466.\n\n37.Hummels, C. and Frens, J. (2009). The reflective \n\ntransformative design process. Proc CHI Ext. Abst., \n2655-2658.\n\n38.Hutchins, E. (1995). Cognition in the Wild. Cambridge, \n\nMA: MIT Press.\n\n39.Intille, S., Kukla, C., and Ma, X. (2002). Eliciting user \n\npreferences using image-based experience sampling and \nreflection. Proc CHI Ext. Abst., 738-739.\n\nReflectionDIS 2014, June 21–25, 2014, Vancouver, BC, Canada100\f40.Intille, S.S., Rondoni, J., Kukla, C., Ancona, I., and Bao,\nL. (2003). A context-aware experience sampling tool. \nProc CHI Ext. Abst., 972-973.",
#         "69.Nakakoji, K., Yamamoto, Y., Takada, S., and Reeves, \nB.N. (2000). Two-dimensional spatial positioning as a \nmeans for reflection in design. Proc DIS, 145-154.\n\n54.Leong, T. W., & Brynskov, M. (2009). CO2nfession: \nEngaging with values through urban conversations. \nProc OZCHI (pp. 209–216). Melbourne, Australia.\n\n70.Nelson, E.J. and Freier, N.G. (2008). Push-me, pull-me: \ndescribing and designing technologies for varying \ndegrees of reflection and invention. Proc IDC, 129-132.\n\n55.Li, I., Dey, A.K., & Forlizzi, J. (2010). A Stage-Based \n\n71.Norman, D. A. (1993). Things That Make Us Smart. \n\nModel of Personal Informatics Systems. Proc CHI, 557–\n566.\n\n56.Li, I., Dey, A.K., & Forlizzi, J. (2011). Understanding \n\nmy data, myself: supporting self-reflection with \n\nNew York: Perseus Group.\n\n72.Pirzadeh, A., He, L., and Stolterman, E. (2013). Personal\ninformatics and reflection: a critical examination of the \nnature of reflection. Proc CHI Ext. Abst., 1979-1988."
#     ]
# for p in P:
#     filtered_result, original_result, response, flag = find_evidence(Q, A, p)
#     for r in filtered_result:
#         print(r)
#         print(jaccard_similarity_word_intersection(r, p))
#     if len(filtered_result) != len(original_result):
#         print("-"*50)
#         print(filtered_result)
#         print(original_result)
#         print(P)
#         for r in original_result:
#             print(jaccard_similarity_word_intersection(r, p))
#         print("-"*50)
# a = "Author Keywords \nLived Informatics; Personal Informatics; Self-Tracking; \nLapsing; Physical Activity; Finances; Location. \n\nACM Classification Keywords \nH.5.m. Information interfaces and presentation (e.g., HCI)."
# b = '- Author Keywords include Personal Informatics. - The paper involves the theory "A Model of Personal Informatics".'
# print(jaccard_similarity_word_intersection(a, b))