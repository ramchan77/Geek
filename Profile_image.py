import urllib2
import json
import pandas as pd
import time
import glob
import string
import re
import requests

csv_files=glob.glob('*.csv')
count=0
input_file=string.replace(csv_files[0], '.csv', '')
input_data=pd.read_csv(str(input_file)+'.csv',encoding='utf-8',error_bad_lines=False,sep=';')
for index,link,image_link in input_data.itertuples():
    link1=link
    link=link.split('/in/')[1]
    count+=1
    print(str(count)+' '+str(link))
    try:
        f = open(str(link)+'.jpg','wb')
        f.write(requests.get(image_link).content)
        f.close()
    except Exception as e:
        print(e)
        
