import json
import elasticsearch
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

host = 'search-tweetmap-kbz75cdphmmyi74fzn74suhsye.us-west-2.es.amazonaws.com'
AWS_ACCESS_KEY = "AKIAJISODG75YKJSYFLQ"
AWS_SECRET_KEY = "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"
REGION = "us-west-2"

awsauth = AWS4Auth(AWS_ACCESS_KEY, AWS_SECRET_KEY, REGION, 'es')

es = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)
# es = elasticsearch.Elasticsearch()
mappings={"mappings": {"mytweets": {"properties": {"pin": {"properties": {"location": {"type": "geo_point"}}}}}}}
print(es.indices.create(index='myposts', body=json.dumps(mappings)))