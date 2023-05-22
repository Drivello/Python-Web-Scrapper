from bs4 import BeautifulSoup
from dotenv import load_dotenv
from datetime import datetime
import asyncio
import aiohttp
import json
import os
import logging

load_dotenv()
SIMPSONS_URL = os.getenv('SIMPSONS_URL')
API_POST_EPISODE_URL = os.getenv('API_POST_EPISODE_URL')
SIMPSONS_FILE_NAME = os.path.dirname(os.path.abspath(__file__))+'/data/' + os.getenv('SIMPSONS_FILE_NAME') + '.json'
SCRAPPER_LOG = os.path.dirname(os.path.abspath(__file__))+'/data/' + os.getenv('SCRAPPER_LOG') + '.log'

logging.basicConfig(filename= SCRAPPER_LOG, level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

original_format = '%b. %d, %Y'
desired_format = '%Y-%m-%d'

def format_date(original_date, original_format):
    date_obj = datetime.strptime(original_date, original_format)
    return date_obj.strftime(desired_format)


async def get_season_data(session, season):
    season_number = season.find(class_='title').text.split(' ')[1]
    season_episodes = season.find_all('li')

    for episode in season_episodes:
        
        episode_number_found = episode.find(class_='numerando')
        episode_number = episode_number_found.text.split(' - ')[1] if episode_number_found else None

        episode_data = episode.find(class_='episodiotitle')
        if episode_data: 
            title_found = episode_data.find('a')
            title = title_found.text if title_found else None

            date_found = episode.find('span')
            date = date_found.text if date_found else None

            url_found = episode_data.find('a')
            url = url_found.get('href') if url_found else None
        else:
            title, date, url = None, None, None

        resume = await get_resume(session, url)

        episode_info = {
            'date': format_date(date,original_format),
            'number': int(episode_number),
            'season_number': int(season_number),
            'name': title,
            'url': url,
            'summary': resume
        }

        await post_episode(session, API_POST_EPISODE_URL, episode_info)

        logging.info(f"Scrapping episode {episode_number} of season {season_number} with title '{title}'")
        print(f"Scrapping episode {episode_number} of season {season_number} with title '{title}'")

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get(SIMPSONS_URL) as response:
            try: 
                check_response(response)
                main_web_content = await get_soup(response)
                seasons_data = main_web_content.find_all(class_='se-c')
                coroutines = [get_season_data(session, season) for season in seasons_data]
                await asyncio.gather(*coroutines)

            except Exception as e:
                logging.error(str(e))

def check_response(response):
    if not response.ok:
        raise Exception('Error: response is not valid')

async def get_soup(response, type = 'lxml'):
    return BeautifulSoup(await response.text(), type)

async def get_resume(session, url):
    async with session.get(url) as response:
        try:
            check_response(response)
            episode_web_content = await get_soup(response)
            resume_found = episode_web_content.find(id='info').find('div').find('p')
            return resume_found.text if resume_found else 'No description available' 
        except:
            return 'No description available'
    
async def post_episode(session, url, episode):
    async with session.post(url, json=episode) as response: 
        return response.text()


if __name__ == '__main__':
    asyncio.run(main())
