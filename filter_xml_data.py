import os
import json 
from glob import glob 
from tqdm import tqdm 
from bs4 import BeautifulSoup
from xml.etree import ElementTree as ET


def read_jsonl(path):
    with open(path, 'r') as fin:
        data = [json.loads(line) for line in fin.readlines()]
    return data 

def read_file(path):
    with open(path, 'r') as fin:
        data = fin.read()
    return data

if __name__ == "__main__":
    
    paths = ["../acl-data/2022-04-29__00-22-50__10000_title-abs-only.jsonl", "../acl-data/acl2022_title-abs-only.jsonl"]

    for path in paths:
        data = read_jsonl(path)

        dirpath = "./data/xml"
        savepath = "./data/xml_filtered"

        acl_ids = set()
        for row in tqdm(data, total=len(data)):
            acl_ids.add(row["acl_id"]) 

        for row in tqdm(data, total=len(data)):
            venue = row["acl_id"].split("-")[0]
            venpath = os.path.join(dirpath, f"{venue}.xml")
            if os.path.exists(venpath):
                tree = ET.parse(venpath)
                parent_map = {c: p for p in tree.iter() for c in p}
                root = tree.getroot()
                for item in root.findall('./volume/paper/url'):
                    if item.text not in acl_ids:
                        volume = parent_map[parent_map[item]]
                        volume.remove(parent_map[item])

                tree.write(os.path.join(savepath, f"{venue}.xml"))        

            

