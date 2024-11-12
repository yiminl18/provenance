# algorithms/llm_query.py - LLM查询算法实现
from pipeline.base_algorithm import BaseAlgorithm
from pipeline.performance_reporter import PerformanceReporter
from model import model
from pipeline.utils.tokenizer import get_token_num
from pipeline.utils.similarity import get_jaccard_similarity
from pipeline.baseline.template import llm_query_example
from typing import List
import time
from pipeline.model_price import ModelConfig
from pipeline.performance import AlgorithmPerformance
from datetime import datetime

class LLMQuery(BaseAlgorithm):
    """LLM查询算法实现"""
    
    def __init__(self, model_name='gpt-4o-mini'):
        super().__init__()
        self.model_name = model_name
        self.performance_reporter = PerformanceReporter()
        self.model_pricing = ModelConfig.get_model_pricing(model_name)
    
    def _run_algorithm(self, Q: str, A: str, P: str) -> List[str]:
        start_time = time.time()
        prompt = self._build_prompt(Q, A, P)
        response = model(self.model_name, prompt) # ChatCompletion
        self.run_history.append(response)
        input_token_num = response.usage.prompt_tokens
        output_token_num = response.usage.completion_tokens
        cost = ModelConfig.calculate_cost(response)
        result = response.choices[0].message.content
        result = self._process_result(result, P)
        
        execution_time = time.time() - start_time
        performance = AlgorithmPerformance(
            timestamp=datetime.now(),
            execution_time=execution_time,
            input_token_num=input_token_num,
            output_token_num=output_token_num,
            cost=cost
        )
        self.performance_history.append(performance)
        return result
    
    def _build_prompt(self, Q: str, A: str, P: str) -> str:
        return f"""
        Given a question, and the answer to the question, and a list of relevant context sentences,
        Return a set of sentences from the relevant context that can provide evidence for the given answer to the given question.
        These evidence sentences must be CHOSEN from the given context list, meaning that they must be EXACTLY the same as the sentence elements in the context list.
        Each returned evidence sentence must not be edited, say no omission, no addition, no modification.
        The number of evidences should be as few as possible, being the most concise and informative.
        Concatenate multiple evidences to a string in sequence. If no evidence can be found, return None.
        For example, if the question is {llm_query_example.example_Q()},
        the answer is {llm_query_example.example_A()}, 
        and the context is: {self._preprocess_context(llm_query_example.example_P())}.
        So the expected output should be: {llm_query_example.example_output()}
        which can not start from the middle of a context element, can not end in the middle of a context element.
        Now consider the following question, answer and context:
        ###{Q}##
        ###{A}###
        ###{self._preprocess_context(P)}###
        Your output here:
        """
    
    @staticmethod
    def _preprocess_context(P: str) -> str: # explicitly convert to string
        from pipeline.utils.tokenizer import nltk_sent_tokenize
        P_sent_list = nltk_sent_tokenize(P)
        return repr(P_sent_list)
    
    @staticmethod
    def _process_result(result: str, reference: str, similarity_threshold: float = 0.7) -> List[str]:
        from pipeline.utils.tokenizer import nltk_sent_tokenize
        
        None_list = ['None', 'none', 'NONE', 'None.', '##None##', 'None##', '##None', 
                     'None##.', '##None##.', 'None.', 'None.##', '##None.']
        
        if result in None_list:
            return []
            
        original_result_list = nltk_sent_tokenize(result, 10)
        filtered_result_list = []
        
        for r in original_result_list:
            if get_jaccard_similarity(r, reference, 'intersection') > similarity_threshold:
                r = r[2:] if r.startswith('- ') else r
                filtered_result_list.append(r)
                
        return filtered_result_list