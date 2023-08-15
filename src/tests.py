import os
import sys
import json
import unittest
import configparser
from bs4 import BeautifulSoup
from unittest.mock import patch, Mock
from pyutils.file_saver import FileSaver
from pyutils.connectors import Connectors
from pyutils.gen_ai_forge import GenAIForge
from pyutils.web_tag_scraper import WebTagScraper

config = configparser.ConfigParser()
config.read("../config/config.ini")


url = config['urls']['superside']
api_key = config['gen_ai']['api_key']

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)


class TestCases(unittest.TestCase):

    def setUp(self):
        self.connector = Connectors()
        self.file_saver = FileSaver()
        self.gen_ai = GenAIForge(api_key)
        self.web_scraper = WebTagScraper()        
        
    def test_conn_scrap(self):
        with patch('pyutils.connectors.requests.get') as mock:
            #Testing successfull connection
            mock.return_value.status_code = 200
            result = self.connector.conn_scrap(url)
            self.assertEqual(result.status_code, 200,f"equal {result.status_code}")

            url_error = "https://www.superside./"
            mock.return_value.status_code = 404
            result = self.connector.conn_scrap(url_error)
            self.assertEqual(result.status_code, 404, f"not equal {result.status_code}")

    def test_get_tag(self):
        self.html = """
                    <html>
                        <body>
                            <p>This is a paragraph.</p>
                            <div>This is a div.</div>
                            <p>Anotherparagraph.</p>
                        </body>
                    </html>
                    """
        self.soup = BeautifulSoup(self.html, 'html.parser')
        
        tags         = self.web_scraper.get_tag(self.soup, 'p')
        nonexist_tag = self.web_scraper.get_tag(self.soup, 'h3')
        invalid_tag  = self.web_scraper.get_tag(self.soup, 'invalid')
        self.assertEqual(tags        , ['<p>This is a paragraph.</p>','<p>Anotherparagraph.</p>'])
        self.assertEqual(nonexist_tag, [])
        self.assertEqual(invalid_tag , [])

    def test_get_style_attr(self):
        data = [
            '<div style="color: red;"></div>',
            '<div style="color: blue;"></div>'
        ]
        tag = 'div'
        output = {'<div style="color: red;"></div>': 'color: red;'
                 ,'<div style="color: blue;"></div>': 'color: blue;'
                 }
        result = self.web_scraper.get_style_attr(data, tag)
        self.assertEqual(result, output)
        
        #tag not found
        tag = 'p'
        output = {}
        result = self.web_scraper.get_style_attr(data, tag)
        self.assertEqual(result, output)

        #empty data
        data = []
        tag = 'div'
        output = {}
        result = self.web_scraper.get_style_attr(data, tag)
        self.assertEqual(result, output)

    def test_save_to_json(self):
        
        data = {"name": "John", "age": 30}
        path = "unit_test"
        filename = "unit_test.json"        

        #Testing if the file is being saved in the path defined
        self.file_saver.save_to_json(data, path, filename)
        self.assertTrue(os.path.exists(os.path.join(path, filename)))

        #Testing if the content of the output is the same of the input
        with open(os.path.join(path, filename), "r") as jsonfile:
            saved_data = json.load(jsonfile)
            self.assertEqual(saved_data, data)

        #Removing unit test json file and path
        os.remove(os.path.join(path, filename))
        os.rmdir(path)

    def test_generate_response(self):
        prompt = "What do I need to do to get hired from Superside?"
        answer = "Make a good tech assesment and show a real desire to enter."
        
        with patch("pyutils.gen_ai_forge.openai.ChatCompletion.create") as mock:
            mock.return_value = {
                "choices": [{"message": {"content": answer}}]
            }
            result = self.gen_ai.get_generated_response(prompt)
            self.assertEqual(result, answer)

            mock.side_effect = Exception("API error")            
            with self.assertRaises(Exception):
                self.gen_ai.get_generated_response(prompt)                

if __name__ == '__main__':
    unittest.main()