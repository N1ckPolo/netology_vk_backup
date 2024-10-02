import requests
import os
from dotenv import load_dotenv
from datetime import datetime
from VK_Connect import VK_Connect
from tqdm import tqdm
from time import sleep


load_dotenv()
YA_TOKEN = os.getenv('YA_TOKEN')
VK_TOKEN = os.getenv('VK_TOKEN')

class YA_Connect:
    
    def __init__(self, token):
        self.base_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        self.headers = {
            'Authorization': token,
        }
    
    
    def create_folder(self, folder_name='VK_Photos'):
        self.params = {'path': f'{folder_name}'}
        create_folder = requests.put(
            self.base_url, 
            headers=self.headers, 
            params=self.params
        )
        if create_folder.ok:
            print(f'Папка "{folder_name}" успешно создана')
            return folder_name
        elif create_folder.json()['error'] == "DiskPathPointsToExistentDirectoryError":
            folder_name = datetime.now().strftime(f"{folder_name}_%Y-%m-%d_%H-%M-%S")
            requests.put(
                self.base_url, 
                headers=self.headers, 
                params={'path': f'{folder_name}'}
            )
            print(f'Папка "{folder_name}" успешно создана\n\n')
            return folder_name
            
            
    def save_photos(self, owner_id, album_id='profile', count=5, folder='VK_Photos'):
        folder_name = self.create_folder(folder)
        vk = VK_Connect(VK_TOKEN)
        for photo in tqdm(vk.photos_get(owner_id, album_id, count), ncols=80, desc='Сохранение фото'):   
            sleep(.1)
            params_ya = {
                    'url': photo[0],
                    'path': f'disk:/{folder_name}/{photo[1]}'
                }
            save_photos = requests.post(
                f'{self.base_url}/upload', 
                params=params_ya, 
                headers=self.headers
            )
    

ya = YA_Connect(YA_TOKEN)
