# Matias Molina - molinamatiasd@gmail.com - linkedin.com/in/matiasmolina

from downloader import GoogleMapsDownloader, GOOGLE_MAPTYPES, GOOGLE_ZOOMS
from settings import secret_key

import numpy as np
import argparse
from matplotlib import pyplot as plt
import pandas as pd
import os

def get_input_args():
    parser = argparse.ArgumentParser()

    help_ = 'Output directory to save the images.'
    parser.add_argument('--output_dir', type=str, help=help_, default='./output')
   
    help_ = 'CSV file with longitude and latitude information.'
    parser.add_argument('--file', type=str, help=help_, required=True)

    help_ = 'Zoom level of satellite image.'
    parser.add_argument('--zoom', type=int, choices=GOOGLE_ZOOMS,
                         help=help_, default=18)

    help_ = 'Type of map.'
    parser.add_argument('--maptype', type=str, choices=GOOGLE_MAPTYPES,
                        default=GOOGLE_MAPTYPES[1])

    help_ = 'Image size. It will be a (size0 x size1) image.'
    parser.add_argument('--size', type=int, nargs=2, default=(512,512))


    args = parser.parse_args()
    return args

if __name__ == '__main__':
    # Example
    # python3 download_bulk.py --file data/public_locations.csv --zoom 17 --output_dir data/images/zoom17

    args = get_input_args()
    file_name = args.file
    zoom = args.zoom
    maptype = args.maptype
    size = args.size
    output_dir = args.output_dir

    os.makedirs(output_dir, exist_ok=True) 

    # Read CSV
    df = pd.read_csv(file_name)
    for i, row in df.iterrows():
        location = (row['latitude'], row['longitude'])
        id_ = int(row['id'])
        group = int(row['group'])
        public = int(row['is_public'])

        # Image downloader
        downloader = GoogleMapsDownloader(location=location,
                                      zoom=zoom,
                                      secret_key=secret_key,
                                      maptype=maptype,
                                      size=size)

        # Image downloading.
        x = downloader.request(return_as_numpy=True)
        try:
            output_path = os.path.join(output_dir, f'id{id_}_group{group}_public{public}.png')
            plt.imsave(output_path, x)
            print('Image saved in', output_path)
        except:
            print('Error when saving', output_path)

