from datetime import datetime, timedelta
from searchScene import searchScene

# start_date = datetime.now().strftime('%Y-%m-%d')
start_date = '2022-04-22'
end_date = ''
termination_date = '2022-05-01'
termination_date = datetime.strptime(termination_date, '%Y-%m-%d')
coords_file = 'API/testing_coords.txt'
method = 'NDWI'
cloud_cover = 10
threshold = 0.05


next_date = start_date
next_date = datetime.strptime(next_date, '%Y-%m-%d')
while next_date > termination_date:
    print("sending in",start_date)
    next_date = searchScene(coords_file,cloud_cover,'NDWI',start_date,end_date)
    next_date = datetime.strptime(next_date, '%Y-%m-%d')
    print("next date:",next_date)
    start_date = next_date - timedelta(days=1)
    start_date = start_date.strftime('%Y-%m-%d')
    print("new start date is",start_date)