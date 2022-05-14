import pytest
from ingestion.apis import RecentAPI

from unittest.mock import patch



@pytest.fixture
def recentapi():
    return RecentAPI('API_Folder_Name')


def test_bearer_oauth():
    class DummyResponse:
        def __init__(self):
            self.headers = {}
    r = DummyResponse()
    api = RecentAPI('Dummy_Token_Value')
    actual = api._bearer_oauth(r).headers
    expected = {'Authorization': 'Bearer Dummy_Token_Value', 'User-Agent': 'v2RecentSearchPython'}
    assert actual == expected


def test_url(recentapi):
    api = recentapi
    assert api.url == "https://api.twitter.com/2/tweets/search/recent"


class MockRequestsGet():
    def __init__(self, status_code):
        self.status_code = status_code
    
    @staticmethod
    def json():
        return {'meta':{'foo':'bar','next_token':'my_awesome_token'}}


def test_next_token_flag_false(recentapi):
    mocked_requests_get = MockRequestsGet(200)

    with patch('ingestion.apis.requests.get', return_value = mocked_requests_get):
        api = recentapi
        r = api.get_tweets({'dummy':'dict'})
        assert  r == [{'meta':{'foo':'bar','next_token':'my_awesome_token'}},
                      {'meta':{'foo':'bar','next_token':'my_awesome_token'}}]
