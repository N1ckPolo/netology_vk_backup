import os
from dotenv import load_dotenv
from YA_Connect import YA_Connect
from VK_Connect import VK_Connect

load_dotenv()
YA_TOKEN = os.getenv('YA_TOKEN')
VK_TOKEN = os.getenv('VK_TOKEN')

ya = YA_Connect(YA_TOKEN)
vk = VK_Connect(VK_TOKEN)

print('Зравствуйте, введите ID пользователя VK, фотографии которого нужно сохранить:')
owner_id = input('VK ID: ')
album_name = input('Откуда хотите сохранить фотографии, стена/профиль? (Значение по умолчанию: "профиль") ')
album_dict = {'стена': 'wall', 'профиль': 'profile'}
album_id = album_dict.get(album_name.lower())
if not album_id:
    album_id = 'profile'
count = input('Укажите количество фотографий (Количество по умолчанию: 5): ')
if not count:
    count = 5
folder = input('Введите имя папки создаваемой на ЯндексДиск (Название по умолчанию:"VK_Photos"): ')
if not folder:
    folder = 'VK_Photos'  

get_photo = vk.photos_get(owner_id, album_id, count)
save_photo = ya.save_photos(get_photo, folder)

print("\nГотово! Подробности сохранены в result.json, в корневой директоии проекта")


# Добавить в будущем:
#     Обработку варианта с пустыми строками поместить в определение самих функций
#     Обработку вариантов без ввода VK ID, символы в count итд
#     Сохранение фото на GoogleDrive