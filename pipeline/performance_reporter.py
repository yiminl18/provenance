# performance_reporter.py - 性能指标报告相关功能
from typing import List
from pipeline.performance import AlgorithmPerformance
class PerformanceReporter:
    """处理算法性能指标的计算和报告"""
    
    @staticmethod
    def get_total_cost(metrics_history: List[AlgorithmPerformance]) -> float:
        return sum(metric.cost for metric in metrics_history)
    
    @staticmethod
    def get_total_time(metrics_history: List[AlgorithmPerformance]) -> float:
        return sum(metric.execution_time for metric in metrics_history)
    
    @staticmethod
    def get_average_cost(metrics_history: List[AlgorithmPerformance]) -> float:
        if not metrics_history:
            return 0.0
        return PerformanceReporter.get_total_cost(metrics_history) / len(metrics_history)
    
    @staticmethod
    def get_average_time(metrics_history: List[AlgorithmPerformance]) -> float:
        if not metrics_history:
            return 0.0
        return PerformanceReporter.get_total_time(metrics_history) / len(metrics_history)
