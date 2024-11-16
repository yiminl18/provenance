from pipeline.base_algorithm import BaseAlgorithm
from typing import List
from pipeline.utils.tokenizer import nltk_sent_tokenize, remove_elements_by_indexes
from pipeline.utils.similarity import get_jaccard_similarity
from pipeline.utils.indexing import get_index_by_similarity

class GreedySearch(BaseAlgorithm):
    def __init__(self, model_name: str, threshold: float = 0.99, 
                 convergence = False, initialization = True, 
                 early_stopping = False, early_stopping_overhead = 5):
        super().__init__()
        self.model_name = model_name
        self.threshold = threshold
        self.convergence = convergence
        self.initialization = initialization
        self.early_stopping = early_stopping
        self.early_stopping_overhead = early_stopping_overhead # if early_stopping is True, this is the maximum number of continuous deletion

    def _run_algorithm(self, Q: str, A: str, P: str) -> List[str]:
        index_to_delete = []
        evidence_answer = ""
        P_sentences = nltk_sent_tokenize(P)
        continuous_deletion = 0

        iterate_list = list(range(len(P_sentences)))
        if self.initialization:
            iterate_list = get_index_by_similarity(P, Q)

        original_list = iterate_list.copy()

        while True:

            for i in iterate_list:
                continuous_deletion += 1
                temp_index_to_delete = index_to_delete.copy()
                temp_index_to_delete.append(i)
                temp_sentence = remove_elements_by_indexes(P_sentences, temp_index_to_delete)
                temp_evidence_answer = self.RAG_generation(Q, temp_sentence)
                
                temp_jaccard_similarity = get_jaccard_similarity(A, temp_evidence_answer)
                
                if temp_jaccard_similarity > self.threshold:
                    index_to_delete = temp_index_to_delete
                    evidence_answer = temp_evidence_answer

                # early stop
                if continuous_deletion > self.early_stopping_overhead and self.early_stopping:
                    break
            
            if not evidence_answer: # no deletion
                evidence_answer = A
                break

            if not self.convergence: # ignore While loop
                break

            if remove_elements_by_indexes(original_list, index_to_delete) == iterate_list: # no more deletion for While loop
                break

            iterate_list = remove_elements_by_indexes(original_list, index_to_delete) # next While loop
            
        evidence = remove_elements_by_indexes(P_sentences, index_to_delete)
        
        return evidence
        