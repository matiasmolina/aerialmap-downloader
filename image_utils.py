# Matias Molina - molinamatiasd@gmail.com - linkedin.com/in/matiasmolina

from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

def overlay_image_mask(rgb_image: np.ndarray, colormap_image: np.ndarray,
                       alpha: float = 0.5, colormap: str = 'jet') -> np.ndarray:
    '''
    Overlays two images using alpha blending.
    
    Rarameters
    ----------
    rgb_image: ndarray
        The RGB image as a NumPy array.
    colormap_image: ndarray
        The colormap image as a NumPy array.
    alpha: float
        The alpha blending factor.
    
    Returns
    -------
    The resulting image as a NumPy array.
    '''

    norm = Normalize(vmin=0, vmax=1)
    mapper = ScalarMappable(norm=norm, cmap=colormap)
    colormap_image = mapper.to_rgba(colormap_image, bytes=True)  # Convert to 0-255 uint8

    blended_image = alpha * colormap_image[:,:,:3] + (1-alpha) * rgb_image
    
    blended_image = np.clip(blended_image, 0, 255).astype(np.uint8)

    return blended_image


# Display/Save image with its original size
# Adapted from:
# https://stackoverflow.com/questions/28816046/displaying-different-images-with-actual-size-in-matplotlib-subplot
def display_image_in_actual_size(im_data, mask=None, output_path='./', cmap='jet', alpha=0.5):

    dpi = mpl.rcParams['figure.dpi']
    height, width, depth = im_data.shape

    # What size does the figure need to be in inches to fit the image?
    figsize = width / float(dpi), height / float(dpi)

    # Create a figure of the right size with one axes that takes up the full
    # figure
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])

    # Hide spines, ticks, etc.
    ax.axis('off')

    # Display the image.
    ax.imshow(im_data)
    if mask is not None:
        ax.imshow(mask, alpha=alpha, cmap=cmap)
    if output_path != '':
        plt.savefig(output_path, pad_inches=0)
    plt.show()

def image_bytes_to_numpy(image_bytes: bytes) -> np.ndarray:
    image = Image.open(io.BytesIO(image_bytes))
    image = image.convert('RGB')
    image = np.array(image)
    return image
