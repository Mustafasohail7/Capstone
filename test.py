import rasterio
import matplotlib.pyplot as plt

def open_image(image_path):
    with rasterio.open(image_path) as src:
        image = src.read(1)
        meta = src.meta
    return image, meta

def visualize(ndwi,title,gray=False,save=False):
    """
    Visualize NDWI image.
    
    Parameters:
    - ndwi: NDWI array.
    """
    plt.figure()
    if gray:
        plt.imshow(ndwi, cmap='gray')
    else:
        plt.imshow(ndwi, cmap='jet')
    plt.colorbar(label='NDWI')
    plt.title(f'{title}')
    plt.xlabel('Column #')
    plt.ylabel('Row #')
    if save:
        plt.savefig(f'images/{title}.jpg')
    else:
        # plt.show()
        pass

a, a_meta = open_image('downloads/LC09_L2SP_151037_20240319_20240320_02_T1/B7.TIF.tif')
