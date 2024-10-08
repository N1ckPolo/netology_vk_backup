import requests
import os
from dotenv import load_dotenv
import json


load_dotenv()
VK_TOKEN = os.getenv('VK_TOKEN')

class VK_Connect:
    
    def __init__(self, token, version='5.131'):
        self.token = token
        self.version = version
        self.base_url = 'https://api.vk.com/method/'
        self.params = {
            'access_token': self.token,
            'v': self.version,
        }
    
    
    def photos_get(self, owner_id, album_id='profile', count=5):
        photo_url = f'{self.base_url}photos.get'
        params = {
            **self.params,
            'owner_id': owner_id,
            'album_id': album_id,
            'count': count,
            'extended': 1
        }
        response = requests.get(photo_url, params=params)
        # pprint(response.json())
        photo_URLs = []
        data_list = []
        for item in response.json()['response']['items']:
            date = item['date']
            file_name = f"{item['likes']['count']}"
            if file_name in map(lambda x: x[1], photo_URLs):
                file_name = f"{item['likes']['count']}_{date}" 
            
            if 'orig_photo' in item:
                photo_URL = item['orig_photo']['url']
                data = {
                    'file_name': f'{file_name}.jpg', 
                    'size': f"{item['orig_photo']['height']}*{item['orig_photo']['width']}"
                }
                data_list.append(data)
            
            else:
                photo_URL = item['sizes'][-1]['url']
                data = {
                    'file_name': f'{file_name}.jpg', 
                    'size': f"{item['sizes'][-1]['height']}*{item['sizes'][-1]['width']}"
                }
                data_list.append(data)
            
            
            photo_URLs.append((photo_URL, file_name))
        
        with open('result.json', 'w') as fp:
            json.dump(data_list, fp, indent='')
        return photo_URLs