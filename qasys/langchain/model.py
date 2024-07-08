

#this is the models API. You pass the model (name of the model) and prompt, the API will return the response out 
def model(model_name, prompt, json_mode=False):
    if(model_name == 'bert'):
        from models.bert_model import bert
        return bert(prompt)
    if(model_name == 'gpt35'):
        from models.gpt_35 import gpt_35
        return gpt_35(prompt, json_mode=json_mode)
    if(model_name == 'gpt35_azure'):
        from models.gpt_35_azure import gpt_35_azure
        return gpt_35_azure(prompt)
    if(model_name == 'gpt35long'):
        from models.gpt_35_long import gpt_35_long
        return gpt_35_long(prompt)
    if(model_name == 'gpt4'):
        from models.gpt_4 import gpt_4
        return gpt_4(prompt)
    if(model_name == 'gpt4o'):
        from models.gpt_4o import gpt_4o
        return gpt_4o(prompt, json_mode=json_mode)
    if(model_name == 'flant5small'):
        from models.flan_t5_small_model import flant5small
        return flant5small(prompt)
    if(model_name == 'flant5base'):
        from models.flan_t5_base_model import flant5base
        return flant5base(prompt)
    if(model_name == 'flant5large'):
        from models.flan_t5_large_model import flant5large
        return flant5large(prompt)
    if(model_name == 'ai21'):
        from models.ai21_model import ai21
        return ai21(prompt)
    if(model_name == 'gpt4_azure'):
        from models.gpt_4_azure import gpt_4_azure
        return gpt_4_azure(prompt)
    if(model_name == 'gpt4_long'):
        from models.gpt_4_long import gpt_4_long
        return gpt_4_long(prompt)
    return 'input model does not exist'


