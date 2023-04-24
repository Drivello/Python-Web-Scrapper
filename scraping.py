from bs4 import BeautifulSoup 
import requests

try:
    response = requests.get('https://simpsonizados.me/serie/los-simpson/')
    if response.status_code != 200:
        raise Exception('Error: response.status_code differs from 200')
    web_content = BeautifulSoup(response.content, 'lxml')
except Exception as e:
    print(e)