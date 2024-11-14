# pipeline/baseline/bfs.py - BFS search algorithm implementation
from pipeline.base_algorithm import BaseAlgorithm
from typing import List
from pipeline.model_price import ModelConfig
from pipeline.utils.tokenizer import nltk_sent_tokenize, get_token_num_for_list
from langchain.docstore.document import Document
from pipeline.utils.indexing import store_splits
from pipeline.utils.sequentialize import sort_substrings

class BFS(BaseAlgorithm):
    """BFS search algorithm implementation"""
    
    def __init__(self, model_name='gpt-4o-mini', threshold=0.5):
        super().__init__()
        self.model_name = model_name
        self.model_pricing = ModelConfig.get_model_pricing(model_name)
        self.threshold = threshold
    
    def _run_algorithm(self, Q: str, A: str, P: str) -> List[str]:
        # create search key words pool
        extracted_search_list = self.LLM_extractor(A) + [Q] # Q remains unchanged
        extracted_search_list = list(set(extracted_search_list)) # remove duplicates
        extracted_search_list = [x for x in extracted_search_list if x] # remove empty strings

        P_sentences = nltk_sent_tokenize(P)
        total_token_num = get_token_num_for_list(P_sentences, self.model_name)
        all_splits = [Document(page_content=s, metadata={"source": "local"}) for s in P_sentences]
        vector_store = store_splits(all_splits, "baseline1")

        searched_docs = []
        less_similar_evidence_with_index = []
        unsorted_unfiltered_evidence_with_index = []
        unsorted_evidence_with_index = []
        evidence = []

        for extracted_search in extracted_search_list:
            searched_docs.append(vector_store.similarity_search_with_score(extracted_search, k=30)) # using large k to return all chunks' score, then we can filter by threshold. # return is a list of tuple, (Document, score) # lower score more similar
        vector_store.delete_collection()
        # cosine distance to regular cosine similarity
        searched_docs = [[(doc[0], 1-doc[1]) for doc in docs] for docs in searched_docs]

        # bfs style
        # For each list, take the tuple with the highest score, put it into evidence, until the token number in evidence exceeds 20% of the total token number
        for i in range(len(searched_docs[0])): # i is the index of top i in each list element
            if get_token_num_for_list(evidence) < total_token_num * 0.2:
            # if True: # get all evidence astisfies the threshold
                for j in range(len(searched_docs)): # j is the index of search_pool list
                    if searched_docs[j][i][0].page_content in evidence:
                        continue
                    elif searched_docs[j][i][1] < self.threshold: # filter out less similar ones:
                        less_similar_evidence_with_index.append([searched_docs[j][i][0].page_content, j, searched_docs[j][i][1]])
                        unsorted_unfiltered_evidence_with_index.append([searched_docs[j][i][0].page_content, j, searched_docs[j][i][1]])
                        continue
                    else:
                        unsorted_unfiltered_evidence_with_index.append([searched_docs[j][i][0].page_content, j, searched_docs[j][i][1]])
                        evidence.append(searched_docs[j][i][0].page_content)
                        unsorted_evidence_with_index.append([searched_docs[j][i][0].page_content, j, searched_docs[j][i][1]])
            else:
                break
        evidence = sort_substrings(P_sentences, evidence)
        return evidence

    
    def LLM_extractor(self, question: str) -> list:
        bad_words = ['Yes', 'No', 'yes', 'no', 'YES', 'NO', 'None', 'none', 'NONE', "I don't know.",]
        if question in bad_words:
            return []

        prompt = \
        f"""
        Your task is to decompose a sentence Q into its components.
        If the sentence is a single entity, return the entity name.
        If the sentence contains multiple entities, ectract these entities and use @ to separate them.
        If the sentence is a predicate (or condition, e.g. date) , return the predicate as it is.
        If the sentence contains multiple predicates, extract these predicates and use @ to separate them.
        If the sentence is a mix of entities and predicates, extract all these entities and predicates and use @ to separate them.
        Now consider the following question Q {question}. Your answer:
        """
        
        result = self.LLM(prompt)
        result = result.split('@') # a list[str]
        return result