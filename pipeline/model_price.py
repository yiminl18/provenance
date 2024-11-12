from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional, Pattern
import re
from openai.types.chat import ChatCompletion

@dataclass
class ModelPricing:
    input_price: float  # Price per 1M input tokens
    output_price: float  # Price per 1M output tokens
    cached_input_price: float = 0.0  # Price per 1M cached input tokens
    context_window: int = 4096

class ModelConfig:
    """Model configuration and pricing management"""
    
    # Model patterns and their corresponding pricing
    MODEL_PATTERNS = [
        # GPT-4O Models
        (r"^gpt-4o(-\d{4}-\d{2}-\d{2})?$", ModelPricing(
            input_price=2.50,
            output_price=10.00,
            cached_input_price=1.25,
            context_window=128000
        )),
        # GPT-4O Mini Models
        (r"^gpt-4o-mini(-\d{4}-\d{2}-\d{2})?$", ModelPricing(
            input_price=0.150,
            output_price=0.600,
            cached_input_price=0.075,
            context_window=128000
        )),
        # O1 Preview Models
        (r"^o1-preview(-\d{4}-\d{2}-\d{2})?$", ModelPricing(
            input_price=15.00,
            output_price=60.00,
            cached_input_price=7.50,
            context_window=128000
        )),
        # O1 Mini Models
        (r"^o1-mini(-\d{4}-\d{2}-\d{2})?$", ModelPricing(
            input_price=3.00,
            output_price=12.00,
            cached_input_price=1.50,
            context_window=128000
        )),
        # ChatGPT-4O Latest
        (r"^chatgpt-4o-latest$", ModelPricing(
            input_price=5.00,
            output_price=15.00,
            context_window=128000
        )),
        # GPT-4 Turbo Models
        (r"^gpt-4-(turbo|0125-preview|1106-preview)(-\d{4}-\d{2}-\d{2})?$", ModelPricing(
            input_price=10.00,
            output_price=30.00,
            context_window=128000
        )),
        # GPT-4 Base
        (r"^gpt-4$", ModelPricing(
            input_price=30.00,
            output_price=60.00,
            context_window=8192
        )),
        # GPT-4 32k
        (r"^gpt-4-32k(-\d{4}-\d{2}-\d{2})?$", ModelPricing(
            input_price=60.00,
            output_price=120.00,
            context_window=32768
        )),
        # GPT-3.5 Turbo Latest
        (r"^gpt-3.5-turbo-0125$", ModelPricing(
            input_price=0.50,
            output_price=1.50,
            context_window=16385
        )),
        # GPT-3.5 Turbo Instruct
        (r"^gpt-3.5-turbo-instruct$", ModelPricing(
            input_price=1.50,
            output_price=2.00,
            context_window=4096
        )),
        # GPT-3.5 Turbo 1106
        (r"^gpt-3.5-turbo-1106$", ModelPricing(
            input_price=1.00,
            output_price=2.00,
            context_window=16385
        )),
        # GPT-3.5 Turbo 0613
        (r"^gpt-3.5-turbo-0613$", ModelPricing(
            input_price=1.50,
            output_price=2.00,
            context_window=4096
        )),
        # GPT-3.5 Turbo 16k
        (r"^gpt-3.5-turbo-16k-0613$", ModelPricing(
            input_price=3.00,
            output_price=4.00,
            context_window=16384
        )),
        # GPT-3.5 Turbo 0301
        (r"^gpt-3.5-turbo-0301$", ModelPricing(
            input_price=1.50,
            output_price=2.00,
            context_window=4096
        )),
    ]

    @classmethod
    def get_model_pricing(cls, model_name: str) -> ModelPricing:
        """Get model pricing configuration using regex pattern matching"""
        for pattern, pricing in cls.MODEL_PATTERNS:
            if re.match(pattern, model_name):
                return pricing
        raise ValueError(f"Unsupported model: {model_name}")

    @classmethod
    def calculate_cost(cls, response: ChatCompletion) -> float:
        """Calculate the model running cost"""
        usage = response.usage
        model_name = response.model
        pricing = cls.get_model_pricing(model_name)
        
        # Calculate costs in millions of tokens
        input_tokens = usage.prompt_tokens / 1_000_000
        output_tokens = usage.completion_tokens / 1_000_000
        
        # Calculate cached tokens if available
        cached_tokens = 0
        if hasattr(usage, 'prompt_tokens_details') and hasattr(usage.prompt_tokens_details, 'cached_tokens'):
            cached_tokens = usage.prompt_tokens_details.cached_tokens / 1_000_000
            input_tokens -= cached_tokens  # Subtract cached tokens from input tokens
        
        # Calculate costs
        input_cost = input_tokens * pricing.input_price
        output_cost = output_tokens * pricing.output_price
        cached_cost = cached_tokens * pricing.cached_input_price
        
        total_cost = input_cost + output_cost + cached_cost
        return round(total_cost, 6)

    @classmethod
    def get_detailed_cost(cls, response: ChatCompletion) -> Dict[str, float]:
        """Get detailed cost breakdown"""
        usage = response.usage
        model_name = response.model
        pricing = cls.get_model_pricing(model_name)
        
        # Calculate tokens in millions
        input_tokens = usage.prompt_tokens / 1_000_000
        output_tokens = usage.completion_tokens / 1_000_000
        cached_tokens = 0
        
        if hasattr(usage, 'prompt_tokens_details') and hasattr(usage.prompt_tokens_details, 'cached_tokens'):
            cached_tokens = usage.prompt_tokens_details.cached_tokens / 1_000_000
            input_tokens -= cached_tokens
        
        costs = {
            'input_cost': round(input_tokens * pricing.input_price, 6),
            'output_cost': round(output_tokens * pricing.output_price, 6),
            'cached_cost': round(cached_tokens * pricing.cached_input_price, 6),
            'total_cost': round(cls.calculate_cost(response), 6)
        }
        
        return costs