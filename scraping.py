import asyncio
import aiohttp
import json
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import logging

load_dotenv()
SIMPSONS_URL = os.getenv('SIMPSONS_URL')
SIMPSONS_FILE_NAME = 'scrapper/' + os.getenv('SIMPSONS_FILE_NAME') + '.json'
SCRAPPER_LOG = 'scrapper/' + os.getenv('SCRAPPER_LOG') + '.log'

logging.basicConfig(filename= SCRAPPER_LOG, level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

async def get_season_data(session, season, scrapped_episodes):
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

        async with session.get(url) as response:
            check_response(response)
            episode_web_content = await get_soup(response)
            resume_found = episode_web_content.find(id='info').find('div').find('p')
            resume = resume_found.text if resume_found else 'No description available' 

        episode_info = {
            'season': season_number,
            'episode': episode_number,
            'title': title,
            'resume': resume,
            'date': date,
            'url': url
        }
        scrapped_episodes.append(episode_info)
        logging.info(f"Scrapping episode {episode_number} of season {season_number} with title '{title}'")

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get(SIMPSONS_URL) as response:
            try: 
                check_response(response)
                main_web_content = await get_soup(response)
                seasons_data = main_web_content.find_all(class_='se-c')
                scrapped_episodes = []
                coroutines = [get_season_data(session, season, scrapped_episodes) for season in seasons_data]
                await asyncio.gather(*coroutines)

                with open(SIMPSONS_FILE_NAME, 'w') as file_open:
                    json.dump(scrapped_episodes, file_open, indent=4)
                    logging.info(f"Data written to {SIMPSONS_FILE_NAME}")
            except Exception as e:
                logging.error(str(e))

def check_response(response):
    if not response.ok:
        raise Exception('Error: response is not valid')

async def get_soup(response, type = 'lxml'):
    return BeautifulSoup(await response.text(), type)

if __name__ == '__main__':
    asyncio.run(main())
