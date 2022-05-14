import pytest
from ingestion.ingestors import BatchIngestor
from ingestion.apis import RecentAPI
from ingestion.writers import FileWriter
from unittest.mock import patch
import json


@pytest.fixture
def ingestor_fix():
    return BatchIngestor(query_params = {'query':'filds'},
                         n_requests = 2,
                         api_cls = RecentAPI,
                         folder_name = 'temp_folder',
                         writers_cls = FileWriter
                         )



def test_get_data():
    with patch('ingestion.apis.RecentAPI.get_tweets', return_value = {'foo':'bar'}):
        ingestor = BatchIngestor(query_params = {'query':'filds'},
                         n_requests = 2,
                         api_cls = RecentAPI,
                         folder_name = 'temp_folder',
                         writers_cls = FileWriter
                         )
        r = ingestor._get_data()
        assert  r == {'foo':'bar'}




class DummyWriter(FileWriter):
    def __init__(self, folder_name = ''):
        self.address = folder_name
        self.data_dict = {'data' : []}


def test_indgest(tmpdir):
    with patch('ingestion.ingestors.BatchIngestor._get_data', return_value = {'foo':'bar'}):
        
        file = tmpdir.mkdir("sub").join('textfile.txt')
        
        ingestor = BatchIngestor(query_params = {'query':'filds'},
                         n_requests = 2,
                         api_cls = RecentAPI,
                         folder_name = file.strpath,
                         writers_cls = DummyWriter
                         )
        
        ingestor.ingest()
        assert  file.read() == json.dumps({'data':[{'foo':'bar'}]}, indent = 6, sort_keys = True)