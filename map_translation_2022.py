#### insert title and abstract for 60 langs, acl2022
import os
import json 
import xml.etree.ElementTree as ET
import copy
import sys


schema_k=['aa', 'ab', 'af', 'ak', 'sq', 'am', 'ar', 'an', 'hy', 'as', 'av', 'ae', 'ay', 'az', 'ba', 'bm', 'eu', 'be', 'bn', 'bh', 'bi', 'bo', 'bs', 'br', 'bg', 'my', 'ca', 'cs', 'ch', 'ce', 'zh', 'cu', 'cv', 'kw', 'co', 'cr', 'cy', 'cs', 'da', 'de', 'dv', 'nl', 'dz', 'el', 'en', 'eo', 'et', 'eu', 'ee', 'fo', 'fa', 'fj', 'fi', 'fy', 'ff', 'fl', 'Ga', 'de', 'gd', 'ga', 'gl', 'gv', 'el', 'gn', 'gu', 'ht', 'ha', 'he', 'hz', 'hi', 'ho', 'hr', 'hu', 'hy', 'ig', 'is', 'io', 'ii', 'iu', 'ie', 'ia', 'id', 'ik', 'is', 'it', 'jv', 'ja', 'kl', 'kn', 'ks', 'ka', 'kr', 'kk', 'km', 'ki', 'rw', 'ky', 'kv', 'kg', 'ko', 'kj', 'ku', 'lo', 'la', 'lv', 'li', 'ln', 'lt', 'lb', 'lu', 'lg', 'mk', 'mh', 'ml', 'mi', 'mr', 'ms', 'Mi', 'mk', 'mg', 'mt', 'mn', 'mi', 'ms', 'my', 'na', 'nv', 'nr', 'nd', 'ng', 'ne', 'nl', 'nn', 'nb', 'no', 'oc', 'oj', 'or', 'om', 'os', 'pa', 'fa', 'pi', 'pl', 'pt', 'ps', 'qu', 'rm', 'ro', 'ro', 'rn', 'sg', 'sa', 'si', 'sk', 'sk', 'sl', 'se', 'sm', 'sn', 'sd', 'so', 'st', 'es', 'sq', 'sc', 'sr', 'ss', 'su', 'sw', 'sv', 'ty', 'ta', 'tt', 'te', 'tg', 'tl', 'th', 'bo', 'ti', 'to', 'tn', 'ts', 'tk', 'tr', 'tw', 'ug', 'uk', 'ur', 'uz', 've', 'vi', 'vo', 'cy', 'wa', 'wo', 'xh', 'yi', 'yo', 'za', 'zh', 'zu']

#fs=os.listdir('../acl2022')
#c=0
#unfind=[]
#unmatch_key=[]
#for f in tqdm(fs):
#    if f.startswith('.'):
#        continue 

def modify(f):   
    c=0
    unfind=[]
    unmatch_key=[]

    d=json.load(open('../acl2022/'+f))
    acl_id=d["acl_id"]
    f_xml, p_xml=acl_id.split('-')
    v, pid=p_xml.split('.')

    tree = ET.ElementTree(file=os.path.join('data/xml_test', f_xml+'.xml'))
    root = tree.getroot()
    volume=root.find('volume[@id="{}"]'.format(v))
    paper=volume.find('paper[@id="{}"]'.format(pid))
    if paper==None:
        unfind.append(acl_id)
        return c, acl_id
        #continue
    
    titles=d['translations']['title']
    abstracts=d['translations']['abstract']
    for k in titles:
        if k not in schema_k:
            unmatch_key.append([acl_id, k])
            continue
        t=ET.SubElement(paper, 'title_'+k)
        t.text=titles[k]
        t.tail='\n      '

    for k in abstracts:
        if k not in schema_k:
            unmatch_key.append([acl_id, k])
            continue
        t=ET.SubElement(paper, 'abstract_'+k)
        t.text=abstracts[k]
        t.tail='\n      '

    tree.write(os.path.join('data/xml_test', f_xml+'.xml'), encoding="utf-8", xml_declaration=True)
    c+=1
    #print(acl_id)
    #if c == 3:
    #    break

    return c, acl_id


if __name__ =='__main__':
    fn=sys.argv[1]
    modify(fn)

    
