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
    directories = []
    for i in range(len(subdirectories)):
        sub_downloads_dir = os.path.join(base_dir, subdirectories[i])
        subsubdirectories = find_subdirectories(sub_downloads_dir)
        directories.extend(subsubdirectories)
    if len(directories) >= 2:
        return directories
    else:
        return None

def find(base_dir=''):
    # Assuming your notebook is in '/content'
    file_paths = find_file_paths(base_dir)
    if file_paths:
        print(f"Found {len(file_paths)} subdirectories in the downloads folder.")
    else:
        print("Couldn't find two subdirectories in the downloads folder.")

    return file_paths
