import json 
from tqdm import tqdm 

def read_jsonl(path):
    with open(path, 'r') as fin:
        data = [json.loads(line.strip()) for line in fin.readlines()]
    return data 

def read_json(path):
    with open(path, 'r') as fin:
        data = json.load(fin)
    return data 

def write_json(path, data):
    with open(path, 'w') as fout:
        json.dump(data, fout)
    

if __name__ == "__main__":

    read_path = "./data/terms.json"
    save_path = "./data/terms_links.json"

    # write_json(read_path, read_jsonl(read_path))

    data = read_json(read_path)
    for i, row in tqdm(enumerate(data), total=len(data)):
        for sent in row["sentences"]:
            if len(sent["wiki"]) == 0:
                data[i]["wiki"] = ""
            else:
                data[i]["wiki"] = sent["wiki"][0][1]
                break
        if data[i]["wiki"] == "":
            print(row["term"])
        
    
    write_json(save_path, data)

    