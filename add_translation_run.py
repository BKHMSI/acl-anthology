import subprocess 
import os
from tqdm import tqdm 

fs=os.listdir('../acl2022')
c=0
unfind=[]
unmatch_key=[]

for f in tqdm(fs):
    if f.startswith('.'):
        continue 
    
    subprocess.run('python map_translation_2022.py {}'.format(f), shell=True)


fs=os.listdir('../acl10k')
c=0
unfind=[]
unmatch_key=[]

for f in tqdm(fs):
    if f.startswith('.'):
        continue 
    
    subprocess.run('python map_translation.py {}'.format(f), shell=True)