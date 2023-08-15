import os
import json

class FileSaver:
    def save_to_json(self, data, path, filename):
        """_summary_

        Args:
            data (_type_): _description_
            path (_type_): _description_
            filename (_type_): _description_
        """
        os.makedirs(path, exist_ok=True)

        try:
            with open(path+"/"+filename, "w", encoding="utf-8") as jsonfile:
                json.dump(data, jsonfile, ensure_ascii=False, indent=4)
        
            print(f"File {filename} saved in path {path}.")        
        except OSError as e:
            print(f"Error reading the file: {e.strerror}")
