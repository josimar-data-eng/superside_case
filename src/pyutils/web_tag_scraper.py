from bs4 import BeautifulSoup

class WebTagScraper:

    def scrap_website(self, response):
        """_summary_

        Args:
            url (_type_): _description_

        Returns:
            _type_: _description_
        """
        # response = conn_scrap(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            data = {"img": self.get_tag(soup,"img"), "svg": self.get_tag(soup,"svg")}
            print("Data scrapped!")
            return data
        else:
            print("Failed to fetch data. Status Code:", response.status_code)
    

    def get_tag(self, soup, tag):
        """_summary_

        Args:
            soup (_type_): _description_

        Returns:
            _type_: _description_
        """
        tags = [str(i) for i in soup.find_all(tag)]

        return tags


    def get_style_attr(self, data, tag):
        """_summary_

        Args:
            data (_type_): _description_

        Returns:
            _type_: _description_
        """
        dict_style_attr = {}
        if len(data) == 0:
            print("Empty data")
        else:
            for i in data:
                try:
                    soup = BeautifulSoup(i, 'html.parser')
                    _tag = soup.find(tag)
                    if _tag:
                        dict_style_attr.__setitem__(str(_tag),_tag.get("style"))
                    else:
                        print(f"Error: {tag} not found in the HTML")
                except Exception as e:
                    print(f"An error occurred: {e}")
        return dict_style_attr