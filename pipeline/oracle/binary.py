# pipeline/binary.py
from pipeline.base_algorithm import BaseAlgorithm
from typing import List, Dict, Any, Set
from pipeline.utils.tokenizer import nltk_sent_tokenize, convert_intervals_to_set, remove_elements_by_intervals, interval_all_len_1, partition_intervals, remove_intervals
from pipeline.utils.similarity import get_jaccard_similarity

class BinarySearch(BaseAlgorithm):
    def __init__(self, model_name: str, threshold: float = 0.99):
        super().__init__()
        self.model_name = model_name
        self.threshold = threshold
    
    def _run_algorithm(self, Q: str, A: str, P: str) -> List[str]:
        sentences = nltk_sent_tokenize(P)
        iterate_list = [[0, len(sentences)-1]]
        iterate_set = convert_intervals_to_set(iterate_list)
        updated_iterate_list = iterate_list
        intervals_to_be_removed = []
        final_try_result = {}

        while True:
            temp_intervals_to_be_removed = []
            
            for interval in updated_iterate_list:
                # print(interval)
                try_result = self._try_interval(
                    sentences=sentences,
                    interval=interval,
                    intervals_to_be_removed=intervals_to_be_removed,
                    question=Q,
                    raw_answer=A
                )
                print(intervals_to_be_removed)
                if not try_result["influence"]:  # no influence, remove it
                    # print("No influence")
                    final_try_result = try_result
                    intervals_to_be_removed.append(interval)
                    temp_intervals_to_be_removed.append(interval)
                else:
                    continue

            # Check if binary search should end
            
            intervals_to_be_removed_set = convert_intervals_to_set(intervals_to_be_removed)
            
            if interval_all_len_1(updated_iterate_list) or iterate_set == intervals_to_be_removed_set: # tried finest granularity or remove all
                if not intervals_to_be_removed:  # no deletion
                    final_try_result = {
                        "influence": True,
                        "evidence": sentences,
                        "evidence_answer": A,
                        "jaccard_similarity": 1
                    }
                return final_try_result["evidence"]

            # Update intervals for next iteration
            updated_iterate_list = remove_intervals(updated_iterate_list, temp_intervals_to_be_removed)
            updated_iterate_list = partition_intervals(updated_iterate_list)
            print(updated_iterate_list)

    def _try_interval(self, sentences: List[str], interval: List[int], 
                     intervals_to_be_removed: List[List[int]], 
                     question: str, raw_answer: str) -> Dict[str, Any]:
        """Try removing an interval and check if it influences the answer"""
        intervals_to_be_removed = intervals_to_be_removed.copy()
        intervals_to_be_removed.append(interval)
        
        temp_sentences = remove_elements_by_intervals(sentences, intervals_to_be_removed)
        evidence_answer = self.RAG_generation(question, temp_sentences)
        jaccard_similarity = get_jaccard_similarity(raw_answer, evidence_answer)
        return {
            "influence": jaccard_similarity < self.threshold,
            "evidence": temp_sentences,
            "evidence_answer": evidence_answer,
            "jaccard_similarity": jaccard_similarity
        }