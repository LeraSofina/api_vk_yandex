import requests
from pprint import pprint
import json
from tqdm import tqdm

vk_id = input("Введите id VK: ")
vk_token = input("Введите токен VK: ")
ya_token = input("Введите токен Яндекс Диска: ")
folder_name = input('Введите название папки на Яндекс Диске: ')


class VK:

    def __init__(self, vk_token: str, vk_id: str, version='5.131'):
        self.token = vk_token
        self.id = vk_id
        self.version = version

    def get_users_photos(self, album_id=input('Введите ID альбома: ')):
        params = {
            'owner_id': self.id,
            'album_id': album_id,
            'access_token': self.token,
            'photo_sizes': 1,
            'extended': 1,
            'v': self.version
        }
        new_list = []
        new_dict = {}
        req = requests.get('https://api.vk.com/method/photos.get',
                           params).json()
        all_photos = req['response']['items']
        for photo in all_photos:
            new_dict = {
                'file_name': f"{photo['likes']['count']}-{photo['date']}.jpg",
                'URL': photo['sizes'][-1]['url'],
                'size': photo['sizes'][-1]['type']
            }
            new_list.append(new_dict)
        pprint(new_list)
        with open('data.json', 'w') as outfile:
            json.dump(new_list, outfile, indent=0)
        return new_list


class YaUploader:

    def __init__(self, ya_token: str):
        self.token = ya_token
        self.url = 'https://cloud-api.yandex.net/v1/disk/resources/'
        self.headers = {
            'Authorization': f'OAuth {self.token}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def create_folder(self, folder_name):
        params = {
            'path': f'{folder_name}'
        }
        requests.put(self.url, headers=self.headers, params=params)

    def upload_file_to_disk(self, folder_name):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        for file in tqdm(data):
            params = {
                'url': file['URL'],
                'path': f"{folder_name}/{file['file_name']}"
            }
            response = requests.post(upload_url,
                                     params=params,
                                     headers=self.headers)
        response.raise_for_status()
        if response.status_code == 202:
            print('Фото успешно загружено на Яндекс Диск')


if __name__ == '__main__':
    user_vk = VK(vk_token, vk_id)
    data = user_vk.get_users_photos()
    pprint(data)
    user_vk.get_users_photos()
    user_ya = YaUploader(ya_token)
    user_ya.create_folder(folder_name)
    user_ya.upload_file_to_disk(folder_name)