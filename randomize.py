import json
import random
import os
from dotenv import load_dotenv

load_dotenv()
SIMPSONS_FILE_NAME = os.getenv('SIMPSONS_FILE_NAME')

with open(SIMPSONS_FILE_NAME+'.json') as f:
    data = json.load(f)

random_episode = random.choice(data)

print(f"Capítulo {random_episode['season']}x{random_episode['episode']}: {random_episode['title']}")
print(f"Miralo en: {random_episode['url']}")
