#### insert title and abstract for 60 langs, acl10k
import os
import json 
import xml.etree.ElementTree as ET
from tqdm import tqdm

schema_k=['fr', 'ru', 'aa', 'ab', 'af', 'ak', 'sq', 'ar', 'am', 'an', 'hy', 'as', 'av', 'ae', 'ay', 'az', 'ba', 'bm', 'eu', 'be', 'bn', 'bh', 'bi', 'bo', 'bs', 'br', 'bg', 'my', 'ca', 'cs', 'ch', 'ce', 'zh', 'cu', 'cv', 'kw', 'co', 'cr', 'cy', 'cs', 'da', 'de', 'dv', 'nl', 'dz', 'el', 'en', 'eo', 'et', 'eu', 'ee', 'fo', 'fa', 'fj', 'fi', 'fy', 'ff', 'fl', 'Ga', 'de', 'gd', 'ga', 'gl', 'gv', 'el', 'gn', 'gu', 'ht', 'ha', 'he', 'hz', 'hi', 'ho', 'hr', 'hu', 'hy', 'ig', 'is', 'io', 'ii', 'iu', 'ie', 'ia', 'id', 'ik', 'is', 'it', 'jv', 'ja', 'kl', 'kn', 'ks', 'ka', 'kr', 'kk', 'km', 'ki', 'rw', 'ky', 'kv', 'kg', 'ko', 'kj', 'ku', 'lo', 'la', 'lv', 'li', 'ln', 'lt', 'lb', 'lu', 'lg', 'mk', 'mh', 'ml', 'mi', 'mr', 'ms', 'Mi', 'mk', 'mg', 'mt', 'mn', 'mi', 'ms', 'my', 'na', 'nv', 'nr', 'nd', 'ng', 'ne', 'nl', 'nn', 'nb', 'no', 'oc', 'oj', 'or', 'om', 'os', 'pa', 'fa', 'pi', 'pl', 'pt', 'ps', 'qu', 'rm', 'ro', 'ro', 'rn', 'sg', 'sa', 'si', 'sk', 'sk', 'sl', 'se', 'sm', 'sn', 'sd', 'so', 'st', 'es', 'sq', 'sc', 'sr', 'ss', 'su', 'sw', 'sv', 'ty', 'ta', 'tt', 'te', 'tg', 'tl', 'th', 'bo', 'ti', 'to', 'tn', 'ts', 'tk', 'tr', 'tw', 'ug', 'uk', 'ur', 'uz', 've', 'vi', 'vo', 'cy', 'wa', 'wo', 'xh', 'yi', 'yo', 'za', 'zh', 'zu']
# schema_k = ['zh']

fs=os.listdir('../acl10k')
c=0
unfind=[]
unmatch_key=[]
for f in tqdm(fs):
    if f.startswith('.'):
        continue 
    
    d=json.load(open('../acl10k/'+f))
    acl_id=d["acl_id"]
    f_xml, p_xml=acl_id.split('-')
    # v, pid=p_xml.split('.')

    find=False
    tree = ET.ElementTree(file=os.path.join('data/xml_hyperlinks', f_xml+'.xml'))
    for elem in tree.iter():
        if elem.tag=='paper':
            ##debug
            # if elem.find('url') is not None and elem.find('url').text=='2022.acl-short.1364':
            #     break
            # break
            if elem.find('url')==None:
                continue 
            elif elem.find('url').text==acl_id:
                c+=1
                find=True
                # print('find it')
                break 

    if not find:
        unfind.append(acl_id) 
        continue

    titles=d['translations']['title']
    abstracts=d['translations']['abstract']
    for k in titles:
        if k not in schema_k:
            unmatch_key.append([acl_id, k])
            continue

        t=ET.SubElement(elem, 'title_'+k)
        t.text=titles[k]
        t.tail='\n      '

    for k in abstracts:
        if k not in schema_k:
            unmatch_key.append([acl_id, k])
            continue
        t=ET.SubElement(elem, 'abstract_'+k)
        t.text=abstracts[k]
        t.tail='\n      '

    tree.write(os.path.join('data/xml_test', f_xml+'.xml'), encoding="utf-8", xml_declaration=True)
    c+=1


