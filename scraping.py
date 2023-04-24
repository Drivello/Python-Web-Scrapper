from bs4 import BeautifulSoup 
import requests
async def main():
    try:
        response = await requests.get('https://simpsonizados.me/serie/los-simpson/')

        if response.status_code != 200:
            raise Exception('Error: response.status_code differs from 200')
        
        main_web_content = BeautifulSoup(response.content, 'lxml')
        seasons_data = main_web_content.find_all(class_ = 'se-c')

        for season in seasons_data:

            season_number = season.find(class_ = 'title').text.split(' ')[1]
            chapters = season.find_all('li')

            for chapter in chapters:

                season = 'Season %s' % season_number
                episode_number = chapter.find(class_ = 'numerando').text.split(' - ')[1]
                episode = 'S%sE%s' % (season_number, episode_number)
                episode_data = chapter.find(class_ = 'episodiotitle')
                title = episode_data.find('a').text
                date = chapter.find('span').text
                url = episode_data.find('a').get('href')

                response = requests.get(url)
                episode_web_content = BeautifulSoup(response.content, 'lxml')

                resume = episode_web_content.find('div', itemprop='description').find('p').text
                
                print('#'*60)
                print(season) 
                print(episode)
                print(title)
                print(resume)
                print(date)
                print(url)

    except Exception as e:
        print(e)

main()