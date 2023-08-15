import requests

class Connectors:
    
    def conn_scrap(self, url):
        try:
            response = requests.get(url, timeout=5)
            # returns an HTTPError object if an error has occurred
            response.raise_for_status()
            print(f"Web scrapper connetion ok with code {response.status_code}.")
        except requests.exceptions.HTTPError as errh:
            print("HTTP Error")
            print(errh.args[0])
        return response