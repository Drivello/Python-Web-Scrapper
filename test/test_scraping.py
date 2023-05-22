"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from bs4 import BeautifulSoup
from scraping import get_soup, check_response, get_season_data

def test_check_response():
    response_ok = MagicMock(ok=True)
    response_not_ok = MagicMock(ok=False)

    assert check_response(response_ok) is None
    with pytest.raises(Exception):
        check_response(response_not_ok)

@pytest.mark.asyncio
async def test_get_soup():
    text = '<html><body><p>Hello world</p></body></html>'
    response = AsyncMock()
    response.text.return_value = text
    soup = await get_soup(response, 'html.parser')
        
    assert soup.p.string == 'Hello world'

@patch('scraping.get_resume')
@pytest.mark.asyncio
async def test_get_season_data(mock_get_resume):

    season = BeautifulSoup('<div class="season"><div><span class="title">Season 1</span></div><div><li><div class="numerando">1 - 1</div><div class="episodiotitle"><a href="url-ep-1">Episodio 1</a></div></li></div></div>', 'html.parser')
    mock_get_resume.return_value = 'No description available' 

    scrapped_episodes = []
    await get_season_data(None, season, scrapped_episodes)

    assert scrapped_episodes[0]['season'] == '1'
    assert scrapped_episodes[0]['episode'] == '1'
    assert scrapped_episodes[0]['title'] == 'Episodio 1'
    assert scrapped_episodes[0]['resume'] == 'No description available'
    assert scrapped_episodes[0]['date'] is None
    assert scrapped_episodes[0]['url'] == 'url-ep-1'
"""