import asyncio
import aiohttp
from bs4 import BeautifulSoup

async def get_season_data(session, season):
    season_number = season.find(class_='title').text.split(' ')[1]
    chapters = season.find_all('li')

    for chapter in chapters:
        episode_number = chapter.find(class_='numerando').text.split(' - ')[1]
        episode = f'S{season_number}E{episode_number}'
        episode_data = chapter.find(class_='episodiotitle')
        title = episode_data.find('a').text
        date = chapter.find('span').text
        url = episode_data.find('a').get('href')

        async with session.get(url) as response:
            episode_web_content = BeautifulSoup(await response.text(), 'lxml')
            resume_paragraph = episode_web_content.find(id='info').find('div').find('p')
            resume = resume_paragraph.text if resume_paragraph else 'No description available' 

        print('#' * 60)
        print(f'Season {season_number}')
        print(episode)
        print(title)
        print(date)
        print(url)
        print(resume)

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://simpsonizados.me/serie/los-simpson/') as response:
            try: 
                if response.status != 200:
                    raise Exception('Error: response.status_code differs from 200')
                main_web_content = BeautifulSoup(await response.text(), 'lxml')
                seasons_data = main_web_content.find_all(class_='se-c')
                coroutines = [get_season_data(session, season) for season in seasons_data]
                await asyncio.gather(*coroutines)
            except Exception as e:
                print(e)

if __name__ == '__main__':
    asyncio.run(main())
