start_date = ''
end_date = ''
coords_file = 'API/testing_coords.txt'
method = 'NDWI'
cloud_cover = 10
threshold = 0.05
from searchScene import searchScene

searchScene(coords_file,cloud_cover,start_date,end_date)