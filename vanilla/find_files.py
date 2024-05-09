import os

def find_subdirectories(parent_dir):
    subdirectories = []
    for item in os.listdir(parent_dir):
        item_path = os.path.join(parent_dir, item)
        if os.path.isdir(item_path):
            subdirectories.append(item_path)
    return subdirectories

def find_file_paths(base_dir):
    downloads_dir = os.path.join(base_dir, 'downloads')
    subdirectories = find_subdirectories(downloads_dir)
    if len(subdirectories) >= 2:
        return subdirectories[:2]
    else:
        return None

def find(base_dir=''):
    # Assuming your notebook is in '/content'
    file_paths = find_file_paths(base_dir)
    if file_paths:
        print("Found two subdirectories in the downloads folder.")
    else:
        print("Couldn't find two subdirectories in the downloads folder.")

    return file_paths
