import os
import time
import configparser
from datetime import datetime
from urllib.parse import urlparse
from pyutils.mongodb_ops import MongoDB
from pyutils.file_saver import FileSaver
from pyutils.connectors import Connectors
from pyutils.gen_ai_forge import GenAIForge
from pyutils.remove_files import remove_files
from pyutils.web_tag_scraper import WebTagScraper


def main():

    #SETUP
    config = configparser.ConfigParser()
    config.read("../config/config.ini")

    url  = config['urls']['superside']
    domain = urlparse(url).netloc[4:][:-4]

    start_execution = datetime.now()
    curr_dt = start_execution.strftime("%Y_%m_%d_%H_%M_%S")

    directory_path = ["raw/files/img","raw/files/svg","staging/files/img","staging/files/svg","gen_ai/files/img","gen_ai/files/svg"]
    for dir in directory_path:
        remove_files("../data/"+dir)
    
    #OBJECTS INSTANTIATION
    connector = Connectors()
    file_saver = FileSaver()
    web_scraper = WebTagScraper()
    gen_ai = GenAIForge(config['gen_ai']['api_key'])
    mongodb = MongoDB(conn=config['mongodb']["conn"], dbname=config['mongodb']["dbname"], collec=config['mongodb']["collec"])



    mongodb.delete_all_data()

    print(f"\n===========\nConnection\n===========")    
    response = connector.conn_scrap(url) #CONNECTION
    data = web_scraper.scrap_website(response) #SCRAPER

    for tag in data.keys():

        print(f"\n=================\nRaw Layer for {tag}\n=================")    
        raw_data = {domain: data[tag]}
        file_saver.save_to_json(
            raw_data,
            config["path"]["dir"].format(step="raw",folder=tag),
            config["file_name"][tag].format(domain=domain,curr_dt=curr_dt)
        )

        print(f"\n=====================\nStaging Layer for {tag}\n=====================")
        style_attr_data = web_scraper.get_style_attr(raw_data[domain],tag)
        staging_data = {domain: style_attr_data}
        file_saver.save_to_json(
            staging_data,
            config["path"]["dir"].format(step="staging",folder=tag),        
            config["file_name"][tag].format(domain=domain,curr_dt=curr_dt)
        )

        print(f"\n=====================\nGenerative AI for {tag}\n=====================")
        j = 0
        gen_dict = {}
        gen_input = staging_data[domain]
        
        for gen_in_tag,style_attr in gen_input.items():

            if tag == "img":
                prompt = config['prompt']['img_style_prompt'].format(html_parameter=style_attr)
            else:
                prompt = config['prompt']['svg_resp_prompt'].format(html_parameter=gen_in_tag)

            generated_response = gen_ai.get_generated_response(prompt)

            print(f"Resquest {j+1} done")
            time.sleep(60/3)
            gen_dict.__setitem__(prompt, generated_response)
            j+=1
            if j==2:
                break

        conversation_dict = { "conversation":[ {"question":k, "response":v} for k,v in gen_dict.items() ] }
        generated_data = {domain: conversation_dict}

        file_saver.save_to_json(
            generated_data,
            config["path"]["dir"].format(step="gen_ai",folder=tag),
            config["file_name"]["gen_ai"].format(domain=domain,curr_dt=curr_dt)
        )

        print(f"\n=================\n Mongo DB for {tag}\n=================")

        
        mongodb.load_data(generated_data)


    print()
    end_execution = datetime.now()
    print("==============================")
    print(f"Execution time: {end_execution - start_execution}")
    print("==============================")        

if __name__ == "__main__":
    main()

