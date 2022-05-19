from asyncore import write
import json 

def read_jsonl(path):
    with open(path, 'r') as fin:
        data = [json.loads(line.strip()) for line in fin.readlines()]
    return data 

def write_json(path, data):
    with open(path, 'w') as fout:
        json.dump(data, fout)
    

if __name__ == "__main__":

    read_path = "./data/terms.json"
    write_json(read_path, read_jsonl(read_path))

    