import rasterio

def open_image(image_path):
    with rasterio.open(image_path) as src:
        image = src.read(1)
        meta = src.meta
    return image, meta

a, a_meta = open_image('shifted_and_padded_image.tif')