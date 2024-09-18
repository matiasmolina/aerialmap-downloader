# Matias Molina - molinamatiasd@gmail.com - linkedin.com/in/matiasmolina

from downloader import GoogleMapsDownloader, GOOGLE_MAPTYPES, GOOGLE_ZOOMS
from settings import secret_key

import numpy as np
import argparse
from matplotlib import pyplot as plt

def get_input_args():
    def parse_location(input_string):
        t = tuple(map(float, input_string.split(',')))
        if len(t) != 2:
            raise ValueError('Must be a pair of numbers.')
        return t

    parser = argparse.ArgumentParser()

    help_ = 'Zoom level of satellite image.'
    parser.add_argument('--zoom', type=int, choices=GOOGLE_ZOOMS,
                         help=help_, default=18)

    help_ = 'Map location (latitude, longitude).'
    parser.add_argument('--location', type=float, nargs=2, help=help_, required=True)

    help_ = 'Type of map.'
    parser.add_argument('--maptype', type=str, choices=GOOGLE_MAPTYPES,
                        default=GOOGLE_MAPTYPES[1])

    help_ = 'Image size. It will be a (size0 x size1) image.'
    parser.add_argument('--size', type=int, nargs=2, default=(512,512))

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    # Example
    # python3 main.py --location -31.428489 -64.184853 --maptype satellite --size 512 512 --zoom 15

    args = get_input_args()
    zoom = args.zoom
    location = args.location
    maptype = args.maptype
    size = args.size

    # Image downloader
    downloader = GoogleMapsDownloader(location=location,
                                      zoom=zoom,
                                      secret_key=secret_key,
                                      maptype=maptype,
                                      size=size)

    # Image downloading.
    x = downloader.request(return_as_numpy=True)
    
    # Print size + image visualization.
    print(x.shape)
    
    plt.imshow(x)
    plt.axis('off')
    plt.show()

    plt.imsave('image.png', x)
