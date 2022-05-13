import os
import json 
from glob import glob 
from tqdm import tqdm 
from shutil import copy, copytree

def read_jsonl(path):
    with open(path, 'r') as fin:
        data = [json.loads(line) for line in fin.readlines()]
    return data 

if __name__ == "__main__":

    path = "../acl-data/2022-04-29__00-22-50__10000_title-abs-only.jsonl"
    data = read_jsonl(path)

    readpath = "./build/website/{}"
    savepath = "./build_small/website/{}"
    count = 0

    for row in tqdm(data, total=len(data)):
        if os.path.exists(readpath.format(row["acl_id"])):
            srcpath = readpath.format(row["acl_id"])
            tgtpath = savepath.format(row["acl_id"])
            copytree(srcpath, tgtpath)
            count += 1
    print(f"Successfully Copied {count}/{len(data)} Papers")

    for dir in ["css", "events", "images", "fonts"]:
        copytree(readpath.format(dir), savepath.format(dir))

    copy(readpath.format("index.html"), savepath.format("index.html"))
    copy(readpath.format("404.html"), savepath.format("404.html"))
    




    