import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from dotenv import load_dotenv
load_dotenv()
from unittest.mock import patch, MagicMock
from scraping import (
    format_date,
    get_season_data,
    check_response,
    get_resume,
    post_episode
)

### Fixtures

@pytest.fixture
def episode_info():
    return {
        'date': 'Mar. 23, 1991',
        'number': 1,
        'season_number': 1,
        'name': 'Episode 1',
        'url': 'https://example.com/episode1',
        'summary': 'Summary of Episode 1'
    }

@pytest.fixture
def session_mock():
    return MagicMock()

@pytest.fixture
def response_mock():
    response = MagicMock()
    response.ok = True
    return response

@pytest.fixture
def soup_mock():
    soup = MagicMock()
    soup.text.return_value = '<html>...</html>'
    return soup

### Test date format

@pytest.mark.parametrize(
    'original_date, original_format, expected_date',
    [
        ('Mar. 23, 1991', '%b. %d, %Y', '1991-03-23'),
        ('Jan. 01, 2000', '%b. %d, %Y', '2000-01-01'),
        ('Dec. 31, 2022', '%b. %d, %Y', '2022-12-31')
    ]
)
def test_format_date(original_date, original_format, expected_date):
    assert format_date(original_date, original_format) == expected_date

@patch('scraping.get_resume')
@patch('scraping.format_date')
@pytest.mark.asyncio
async def test_get_season_data(mock_get_resume, mock_format_date, session_mock, episode_info):
    season_mock = MagicMock()
    season_mock.find.return_value = MagicMock()
    season_mock.find.return_value.text = '1 1'
    season_mock.find_all.return_value = [MagicMock()]

    episode_mock = season_mock.find_all.return_value[0]
    #episode_mock.find.return_value = MagicMock()

    episode_mock.find.return_value.text.side_effect = [ '1 - 1' , 'Episode 1']

    mock_get_resume.return_value = 'No description available'

    mock_format_date.return_value = 'Mar. 23, 1991'

    ### __aenter__ => async with mock
    session_mock.get.return_value.__aenter__.return_value = response_mock
    session_mock.get.return_value.__aenter__.return_value.text = lambda: '<html>...</html>'
    session_mock.post.return_value.__aenter__.return_value = response_mock

    await get_season_data(session_mock, season_mock)

    assert session_mock.post.called
    assert session_mock.post.call_args[0][0] == os.getenv('API_POST_EPISODE_URL')
    assert session_mock.post.call_args[0][1] == episode_info

@pytest.mark.asyncio
async def test_get_resume(session_mock):
    url = 'https://example.com/episode1'

    session_mock.get.return_value.__aenter__.return_value = response_mock
    session_mock.get.return_value.__aenter__.return_value.text = '<html>...</html>'

    resume = await get_resume(session_mock, url)

    assert resume == 'No description available'

@pytest.mark.asyncio
async def test_post_episode(session_mock, episode_info):
    session_mock.post.return_value.__aenter__.return_value = soup_mock

    result = await post_episode(session_mock, 'API_POST_EPISODE_URL', episode_info)

    assert result == response_mock.text
    assert session_mock.post.called
    assert session_mock.post.call_args[0][0] == 'API_POST_EPISODE_URL'
    assert session_mock.post.call_args[0][1] == episode_info

