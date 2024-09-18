# Matias Molina - molinamatiasd@gmail.com - linkedin.com/in/matiasmolina

import io
from typing import Union, Optional, Tuple
from PIL import Image
import numpy as np
import requests

GOOGLE_MAPTYPES = ['roadmap', 'satellite', 'hybrid', 'terrain']

MAX_ZOOM = 22
GOOGLE_ZOOMS = list(range(0, MAX_ZOOM + 1))

class GoogleMapsDownloader():
    '''
    A class to download and process static map images from Google Maps API.

    Attributes:
    -----------
        center (Tuple[float, float]): The latitude and longitude of the map's center.
        zoom (int): The zoom level of the map. Defaults to 18.
        size (Tuple[int, int]): The dimensions of the map image in pixels. Defaults to (512, 512).
        maptype (str): The type of map to retrieve. Defaults to 'satellite'.
        key (str): Your Google Maps API key.
        base_url (constant str): The base URL for the Google Maps Static API.

    '''
    def __init__(self, location: Tuple[float, float],
                       zoom: int = 18,
                       size: Tuple[int, int] = (512, 512),
                       maptype: str = 'satellite',
                       secret_key: str = ''):

        self.center = location
        self.zoom = zoom
        self.size = size
        self.maptype = maptype
        self.key = secret_key

        self.base_url = 'https://maps.googleapis.com/maps/api/staticmap?'

        self.validate_parameters()

    def _set_secret_key(self, value: str):
        self.key = value
    
    def image_bytes_to_numpy(self, image_bytes: bytes) -> np.ndarray:
        image = Image.open(io.BytesIO(image_bytes))
        image = image.convert('RGB')
        image = np.array(image)
        return image

    def validate_parameters(self):
        if self.zoom not in GOOGLE_ZOOMS:
            msg = f'Zoom level {self.zoom} is not valid. '
            msg += f'Must be between {GOOGLE_ZOOMS[0]} and {GOOGLE_ZOOMS[-1]}.'
            raise ValueError(msg)

        if self.maptype not in GOOGLE_MAPTYPES:
            msg = f'Map type {self.maptype} is not valid. '
            msg = f'Choose from {GOOGLE_MAPTYPES}.'
            raise ValueError(msg)
        
        if not (0 < self.size[0] <= 640 and 0 < self.size[1] <= 640):
            msg = f'Size {self.size} is not valid. '
            msg += f'Width and height must be between 1 and 640 pixels.'
            raise ValueError(msg)
        
        lat, lon = self.center
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            msg = f'Location coordinates {self.center} are not valid. '
            msg += f'Latitude must be between -90 and 90, longitude between -180 and 180.'
            raise ValueError(msg)
        
        # Check if the API key is provided
        if not self.key:
            msg = 'API key is required. '
            msg += 'Please provide a valid Google Maps API key.'
            raise ValueError(msg)

    def generate_url(self) -> str:          
        center = ','.join(tuple(map(str, self.center)))

        url = self.base_url
        url += f'center={center}'
        url += f'&zoom={self.zoom}'
        url += f'&size={self.size[0]}x{self.size[1]}'
        url += f'&maptype={self.maptype}'
        url += f'&key={self.key}'

        self.url = url
        return url

    def request(self, return_as_numpy=True):
        url = self.generate_url()        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                if return_as_numpy:
                    return self.image_bytes_to_numpy(response.content)
                else:
                    return response.content
            else:
                raise Exception('Error when getting the image. Code: ', 
                                 response.status_code)
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
