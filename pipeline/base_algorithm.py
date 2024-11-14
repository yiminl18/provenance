# pipeline/base_algorithm.py - BaseAlgorithm class implementation
from abc import ABC, abstractmethod
from typing import List, Any
from pipeline.performance import AlgorithmPerformance
from openai.types.chat import ChatCompletion
from pipeline.model_price import ModelConfig
import time
from model import model
from pipeline.performance_reporter import PerformanceReporter

class BaseAlgorithm(ABC):
    
    def __init__(self):
        self.llm_performance_history: List[AlgorithmPerformance] = []
        self.run_performance_history: List[AlgorithmPerformance] = []
        self.llm_completion_history: List[ChatCompletion] = []
        self.performance_reporter = PerformanceReporter()
    
    @abstractmethod
    def _run_algorithm(self, *args, **kwargs) -> Any:
        """actual algorithm implementation"""
        pass
    
    def run(self, *args, **kwargs) -> Any:
        '''
        Input: Q:str, A:str, P:str
        Output: List[str]
        '''
        start_time = time.time()
        result = self._run_algorithm(*args, **kwargs)
    
        execution_time = time.time() - start_time
        run_id = int(start_time) # use unix timestamp as run_id
        total_input_tokens = 0
        total_output_tokens = 0
        total_cost = 0
            # Filter and sum performance metrics after start_time
        recent_performances = [p for p in self.llm_performance_history if p.timestamp >= start_time]
        if recent_performances:
            total_input_tokens = sum(p.input_token_num for p in recent_performances)
            total_output_tokens = sum(p.output_token_num for p in recent_performances)
            total_cost = sum(p.cost for p in recent_performances)
            
        run_performance_history = AlgorithmPerformance(
            timestamp=run_id,
            execution_time=execution_time,
            input_token_num=total_input_tokens,
            output_token_num=total_output_tokens,
            cost=total_cost
        )
        self.run_performance_history.append(run_performance_history)

        return result
    
    def LLM(self, prompt) -> str:
        """
        Input: prompt, str
        model_name is set when initializing the class
        Output: str
        """
        # TODO use different model in one class
        start_time = time.time()
        response = model(self.model_name, prompt)
        # record eval
        self.llm_completion_history.append(response)
        input_token_num = response.usage.prompt_tokens
        output_token_num = response.usage.completion_tokens
        cost = ModelConfig.calculate_cost(response)
        execution_time = time.time() - start_time
        performance = AlgorithmPerformance(
            timestamp=response.created,
            execution_time=execution_time,
            input_token_num=input_token_num,
            output_token_num=output_token_num,
            cost=cost
        )
        self.llm_performance_history.append(performance)
        # get LLM output
        result = response.choices[0].message.content
        return result
    
    def get_total_cost(self) -> float:
        return sum(metric.cost for metric in self.llm_performance_history)
    def get_average_cost(self) -> float:
        if not self.llm_performance_history:
            return 0.0
        return self.get_total_cost() / len(self.llm_performance_history)
    def get_total_time(self) -> float:
        return sum(metric.execution_time for metric in self.llm_performance_history)
    def get_average_time(self) -> float:
        if not self.llm_performance_history:
            return 0.0
        return self.get_total_time() / len(self.llm_performance_history)

    def test_randomness(self, repeat: int = 5) -> None:
        """
        test randomness will clear the history and run the algorithm multiple times
        to see performance, run function like get_average_cost()
        """
        self.__init__()
        for _ in range(repeat):
            self._run_algorithm()
        return None
    
    def RAG_generation(self, Q: str, E: list[str]) -> str:
        """
        Input: Q:str
                E:list[str]
        Output: List[str]
        """
        system_prompt = """
        You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use a maximum of three sentences and keep the answer concise."""
        question_for_evaluation = Q +' Only return the answer without any explanations. Separate the answers with commas if there are multiple items. Return None if no answer is found. Please answer this question based on the following description, which contains a set of evidences to help answer the question.'
        evidence_str = ' '.join(E)
        text = f""" Question: {question_for_evaluation}\n\nRetrieved context: {evidence_str}\n\nAnswer: """
        prompt = system_prompt + text

        return self.LLM(prompt)

    
    # def _get_performence_history(self) -> None:
    #     for history in self.llm_completion_history:
    #         start_time = time.time()
    #         input_token_num = history.usage.prompt_tokens
    #         output_token_num = history.usage.completion_tokens
    #         cost = ModelConfig.calculate_cost(history)
    #         execution_time = time.time() - start_time
    #         performance = AlgorithmPerformance(
    #             timestamp=history.created,
    #             execution_time=execution_time,
    #             input_token_num=input_token_num,
    #             output_token_num=output_token_num,
    #             cost=cost
    #         )
    #         self.llm_performance_history.append(performance)
        
    