# base_algorithm.py - 定义算法基类
from abc import ABC, abstractmethod
from typing import List, Any
from pipeline.performance import AlgorithmPerformance
from openai.types.chat import ChatCompletion

class BaseAlgorithm(ABC):
    """算法基类，提供性能监控和数据管理功能"""
    
    def __init__(self):
        self.performance_history: List[AlgorithmPerformance] = []
        self.run_history: List[ChatCompletion] = []
    
    @abstractmethod
    def _run_algorithm(self, *args, **kwargs) -> Any:
        """实际运行算法的逻辑"""
        pass
    
    def run(self, *args, **kwargs) -> Any:
        '''
        Input: Q:str, A:str, P:str
        Output: List[str]
        '''
        
        result = self._run_algorithm(*args, **kwargs)

        return result
    
    def get_total_cost(self) -> float:
        return sum(metric.cost for metric in self.performance_history)
    def get_average_cost(self) -> float:
        if not self.performance_history:
            return 0.0
        return self.get_total_cost() / len(self.performance_history)
    def get_total_time(self) -> float:
        return sum(metric.execution_time for metric in self.performance_history)
    def get_average_time(self) -> float:
        if not self.performance_history:
            return 0.0
        return self.get_total_time() / len(self.performance_history)

    def test_randomness(self, repeat: int = 5) -> None:
        """
        test randomness will clear the history and run the algorithm multiple times
        to see performance, run function like get_average_cost()
        """
        self.__init__()
        for _ in range(repeat):
            self._run_algorithm()
        return None
    