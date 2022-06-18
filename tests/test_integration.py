import pytest
import os

from ingestion.apis import RecentAPI

from ingestion.ingestors import BatchIngestor
from ingestion.writers import FileWriter, S3Writer

from glob import glob

import json

def test_query_error():

    with pytest.raises(Exception):
        query_params = {
                        'query': 'from:elonmusk',
                        'user.fields':'id,location,name,public_metrics',
                        'tweet.fields': 'author_id,public_metrics, DOES_NOT_EXISTS,created_at',
                        'expansions':'geo.place_id,author_id,entities.mentions.username,in_reply_to_user_id,referenced_tweets.id.author_id',
                        'max_results':'10'
                        }

        BatchIngestor(query_params,
                    2,
                    RecentAPI,
                    'data/RecentAPI',
                    FileWriter).ingest()



def test_received_data(tmpdir):

    query_params = {
                    'query': '"World Cup"',
                    'user.fields':'id,location,name,public_metrics',
                    'tweet.fields': 'author_id,public_metrics,conversation_id,created_at',
                    'max_results':'10'
                    }
                    
    mkdir_path = tmpdir.mkdir("sub")

    BatchIngestor(query_params,
                2,
                RecentAPI,
                mkdir_path.strpath,
                FileWriter).ingest()

    
    
    path = glob(f'{mkdir_path.strpath}/*')
    with open(path[0], 'r') as file:
        file = file.read()

        assert list(json.loads(file.split('\n\n\n')[0]).keys())[0] == 'data'





def test_raise_401():
    query_params = {
                        'query': 'from:elonmusk',
                        'user.fields':'id,location,name,public_metrics',
                        'tweet.fields': 'author_id,public_metrics, conversation_id',
                        'expansions':'geo.place_id,author_id,entities.mentions.username,in_reply_to_user_id,referenced_tweets.id.author_id',
                        'max_results':'10'
                        }

    os.environ['BEARER_TOKEN'] = 'fake_token'
    with pytest.raises(Exception):
        BatchIngestor(query_params,
                    2,
                    RecentAPI,
                    'data/RecentAPI',
                    FileWriter).ingest()