import os

def remove_files(directory_path):
    try:
        # List all files in the directory
        files = os.listdir(directory_path)
        
        # Iterate through the files and remove them
        for file in files:
            file_path = os.path.join(directory_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
                # print(f"Removed: {file_path}")
        
        print("All files removed successfully.")
    
    except OSError as e:
        print(f"Error: {e}")

