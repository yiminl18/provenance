from pipeline.base_algorithm import BaseAlgorithm
from typing import List
from pipeline.utils.tokenizer import nltk_sent_tokenize, remove_elements_by_indexes
from pipeline.utils.similarity import get_jaccard_similarity

class GreedySearch(BaseAlgorithm):
    def __init__(self, model_name: str, threshold: float = 0.99):
        super().__init__()
        self.model_name = model_name
        self.threshold = threshold

    def _run_algorithm(self, Q: str, A: str, P: str) -> List[str]:
        index_to_delete = []
        evidence_answer = ""
        jaccard_similarity = 0
        cost_list = []
        P_sentences = nltk_sent_tokenize(P)

        for i in range(len(P_sentences)):
            temp_index_to_delete = index_to_delete.copy()
            temp_index_to_delete.append(i)
            temp_sentence = remove_elements_by_indexes(P_sentences, temp_index_to_delete)
            temp_evidence_answer = self.RAG_generation(Q, temp_sentence)
            
            temp_jaccard_similarity = get_jaccard_similarity(A, temp_evidence_answer)
            
            if temp_jaccard_similarity > self.threshold:
                index_to_delete = temp_index_to_delete
                evidence_answer = temp_evidence_answer
        
        if not evidence_answer: # no deletion
            evidence_answer = A
            
        evidence = remove_elements_by_indexes(P_sentences, index_to_delete)
        
        return evidence
        