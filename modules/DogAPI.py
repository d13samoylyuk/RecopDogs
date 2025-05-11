import requests


class DogAPI:
    def __init__(self):
        self._breedimg_url = 'https://dog.ceo/api/breed/{breed}/images'
        self._breedsall_url =  'https://dog.ceo/api/breeds/list/all'
    
    def get_breed_image(self, breed):
        response = requests.get(self._breedimg_url.format(breed=breed))
        return response.json()
    
    def get_all_breeds(self):
        response = requests.get(self._breedsall_url)
        return response.json()