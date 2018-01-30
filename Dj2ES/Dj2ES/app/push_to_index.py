from elasticsearch import Elasticsearch
import base64
import json

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

class Command():

    def ingest_doc(filepath):
        f = open(filepath, 'rb')
        f_read = f.read()
        f.close()
        b64 = base64.b64encode(f_read).decode('ascii')
        res = es.index(index='eng', doc_type='doc', pipeline='attachment',
                  body={'base64': b64})
        return res

    def search(term):
        if term=='business':
            with open('rqe_business_ind_tha.json', encoding='utf-8') as data_file:
                data = json.loads(data_file.read())
                
                l = []



                for encodings in data['expansionResult']['term'][0]['language'][1]['encoding'][0]['translation']:
                    
                    decoded = base64.b64decode(encodings['value']).decode('utf-8').lower() #- for latin alphabets that are decoded in capitals (EG in ind)
                    
                    l.append(decoded)
                
                res = es.search(index="eng", doc_type='doc', body={
                    "query": {
                        "bool": {
                            "must": {
                                "match_all": {} 
                            }, 
                            "filter": { 
                                "terms": { 
                                    "content": l
                                }
                            }
                        }
                    }, 
                    "size": 2, 
                    "from": 0, 
                    "_source": ["content"], 
                    "highlight": { 
                        "pre_tags" : ["", ""],
                        "post_tags" : ["", ""], 
                        "fields": {}}}) # filter_path=['hits.hits._id', 'hits.hits._type']) _source_exclude=['base64','attachment.content']

        else:
            res = es.search(index="eng", doc_type='doc', body={"query": {"match": {"content": term}}, "size": 2, "from": 0, "_source": ["content"], "highlight": {"pre_tags" : ["", ""], "post_tags" : ["", ""],"fields": {"content": {}}}}) # filter_path=['hits.hits._id', 'hits.hits._type']) _source_exclude=['base64','attachment.content']
        return res


    def match_all():
        res = es.search(index="ind", doc_type='doc', _source_exclude=['base64'],
                body={'query': {'match_all': {}}} )
        return res

    def get_id(my_id):
        res = es.get(index='eng', doc_type='doc', id=my_id,
                    _source_exclude=['attachment.content'] )
        return res
