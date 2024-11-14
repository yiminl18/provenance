# performance.py - 定义性能指标相关的数据结构
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict

@dataclass
class AlgorithmPerformance:
    """store performance metrics of an algorithm"""
    timestamp: datetime
    execution_time: float
    input_token_num: int
    output_token_num: int
    cost: float
    additional_info: Dict = field(default_factory=dict)