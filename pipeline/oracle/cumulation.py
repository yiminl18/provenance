# pipeline/cumulation.py
from pipeline.base_algorithm import BaseAlgorithm
from typing import List, Dict, Any
from pipeline.utils.tokenizer import nltk_sent_tokenize, convert_intervals_to_set, remove_elements_by_intervals, interval_all_len_1, partition_intervals, remove_intervals
from pipeline.utils.similarity import get_jaccard_similarity
from pipeline.baseline.llm_query import build_prompt, process_result
from pipeline.baseline.llm_query import LLMQuery
from pipeline.oracle.greedy import GreedySearch

class CumulationSearch(BaseAlgorithm):
    def __init__(self, model_name: str, threshold: float = 1):
        super().__init__()
        self.model_name = model_name
        self.threshold = threshold
        
    
    def _run_algorithm(self, Q: str, A: str, P: str) -> List[str]:
        

        llmquery_client = LLMQuery(model_name=self.model_name)
        llm_result = llmquery_client.run(Q, A, P)
        raw_jaccard = get_jaccard_similarity(A, self.RAG_generation(Q, llm_result))
        if raw_jaccard >= self.threshold:
            return llm_result
        # print('llm_result', llm_result)
        # print('raw_jaccard', raw_jaccard)
        
        # try to remove by greedy search
        greedy_client = GreedySearch(model_name=self.model_name, threshold=raw_jaccard)
        greedy_result = greedy_client.run(Q, A, '\n'.join(llm_result))
        if get_jaccard_similarity(A, self.RAG_generation(Q, greedy_result)) >= self.threshold:
            return greedy_result
        # print('greedy_result', greedy_result)

        # If both methods fail to meet threshold, try BFS-style evidence collection
        final_result = self.bfs_evidence_collection(Q, A, P, greedy_result)
        



        self.update_history(llmquery_client.llm_performance_history, llmquery_client.llm_completion_history)
        self.update_history(greedy_client.llm_performance_history, greedy_client.llm_completion_history)
        return final_result

    def bfs_evidence_collection(self, Q: str, A: str, P: str, current_evidence: List[str]) -> List[str]:
        """Collect additional evidence using BFS-style approach"""
        # Tokenize passage into sentences
        P_sentences = nltk_sent_tokenize(P)
        
        # Remove sentences already in current evidence
        remaining_sentences = [s for s in P_sentences if s not in current_evidence]
        
        # Calculate similarity scores for all remaining sentences
        extracted_search_list = self.LLM_extractor(A) + [Q]
        sentence_scores = []
        for sentence in remaining_sentences:
            score = max([get_jaccard_similarity(element, sentence) for element in extracted_search_list])
            sentence_scores.append((sentence, score))
        
        # Sort by similarity score in descending order
        sentence_scores.sort(key=lambda x: x[1], reverse=True)
        
        best_evidence = current_evidence.copy()
        best_jaccard = get_jaccard_similarity(A, self.RAG_generation(Q, current_evidence))
        
        # Try adding sentences one by one
        for sentence, score in sentence_scores:
            test_evidence = best_evidence + [sentence]
            current_jaccard = get_jaccard_similarity(A, self.RAG_generation(Q, test_evidence))
            
            if current_jaccard >= self.threshold:
                return test_evidence
            elif current_jaccard > best_jaccard:
                best_evidence = test_evidence
                best_jaccard = current_jaccard
        
        return best_evidence
    
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