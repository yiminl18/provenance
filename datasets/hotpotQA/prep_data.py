import  json, os



def get_question(dataset):

    return json.load(open(f"hotpot_dev_{dataset}_v1.json", 'r'))

