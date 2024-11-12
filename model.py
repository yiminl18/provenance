from typing import Literal

# This is the models API. You pass the model (name of the model) and prompt, 
# the API will return the response out.
def model(
    model_name: Literal[
        'bert', 'gpt-3.5', 'gpt-3.5_azure', 'gpt-3.5-long',
        'gpt-4-turbo', 'gpt-4o', 'gpt-4o-mini',
        'flant5small', 'flant5base', 'flant5large',
        'ai21', 'gpt-4-azure', 'gpt-4-long',
        'o1-preview', 'o1-mini',
    ], 
    prompt: str
):
    if model_name == 'bert':
        from models.bert_model import bert
        return bert(prompt)
    if model_name == 'gpt-3.5':
        from models.gpt_35 import gpt_35
        return gpt_35(prompt)
    if model_name == 'gpt-3.5-azure':
        from models.gpt_35_azure import gpt_35_azure
        return gpt_35_azure(prompt)
    if model_name == 'gpt-3.5-long':
        from models.gpt_35_long import gpt_35_long
        return gpt_35_long(prompt)
    if model_name == 'gpt-4-turbo':
        from models.gpt_4_turbo import gpt_4_turbo
        return gpt_4_turbo(prompt)
    if model_name == 'gpt-4o':
        from models.gpt_4o import gpt_4o
        return gpt_4o(prompt)
    if model_name == 'gpt-4o-mini':
        from models.gpt_4o_mini import gpt_4o_mini
        return gpt_4o_mini(prompt)
    if model_name == 'flant5small':
        from models.flan_t5_small_model import flant5small
        return flant5small(prompt)
    if model_name == 'flant5base':
        from models.flan_t5_base_model import flant5base
        return flant5base(prompt)
    if model_name == 'flant5large':
        from models.flan_t5_large_model import flant5large
        return flant5large(prompt)
    if model_name == 'ai21':
        from models.ai21_model import ai21
        return ai21(prompt)
    if model_name == 'gpt-4-azure':
        from models.gpt_4_azure import gpt_4_azure
        return gpt_4_azure(prompt)
    if model_name == 'gpt-4-long':
        from models.gpt_4_long import gpt_4_long
        return gpt_4_long(prompt)
    if model_name == 'o1-preview':
        from models.o1_preview import o1_preview
        return o1_preview(prompt)
    if model_name == 'o1-mini':
        from models.o1_mini import o1_mini
        return o1_mini(prompt)
    raise ValueError(f"Unsupported model: {model_name}")
