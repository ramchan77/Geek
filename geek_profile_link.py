import urllib2
import json
import pandas as pd
import time
import glob
import string
import re

csv_files=glob.glob('*.csv')
input_file=string.replace(csv_files[0], '.csv', '')
input_data=pd.read_csv(str(input_file)+'.csv',encoding='utf-8',error_bad_lines=False,sep=';')
count=0
name_match=0
company_match=0
fd = open(str(input_file)+'_output.csv','a')
fd.write('Given Link;Fullname;Title;Role;Organization;Profile Link;profile Image\n')
fd.close()
api_token='AKaTTZjraOSzKylqFujXEpnEo9Mn:1544842417038'
for index,link in input_data.itertuples():
    outcheck=0
    profile_link1=''
    link1=link
    link=link.split('/in/')[1]
    try:
        count+=1
        print(str(count)+' '+str(link.encode("utf-8")))
        #print("Before")
        def reload_json(link):
            data=''
            try:
            	url_link="https://cse.google.com/cse/element/v1?rsz=filtered_cse&num=5&hl=en&source=gcsc&gss=.com&sig=76c37a052829ad2c9825658fbbc50bce&cx=011658049436509675749:gkuaxghjf5u&q="+str(link.encode("utf-8"))+"&safe=off&cse_tok="+api_token+"&sort=&exp=csqr,4200995&googlehost=www.google.com&oq="+str(link.encode("utf-8"))+"&gs_l=partner-generic.3...25463.33220.2.33524.0.0.0.0.0.0.0.0..0.0.gsnos%2Cn%3D13...0.7760j8723106j16..1ac.1.25.partner-generic..0.0.0.&callback=google.search.Search.csqr9114"
            	#print(url_link)
                data = urllib2.urlopen(url_link,timeout=15)
                return data
            except Exception as e:
                print(str(e))
                if str(e)=='<urlopen error [Errno 11001] getaddrinfo failed>':
                    time.sleep(25)
                    reload_json(link)
                return data
        data=reload_json(link)
        #print("After")
        dd=data.read()
        dd=dd.replace('/*O_o*/\ngoogle.search.Search.csqr9114(','')
        dd=dd.replace(');','')
        #filename = "jj.json"
        #file_ = open(filename, 'w')
        #file_.write(dd)
        #file_.close()
        #with open('jj.json') as f:
        data1 = json.loads(dd)
        for results in data1['results']:
            if outcheck==0:
                profile_link=results["url"]
                try:
                    profile_link1=profile_link.split('/in/')[1]
                    profile_link1=re.sub('/.*$','',profile_link1)
                except:
                    continue
                if link==profile_link1:
                    print('link_match')
                    fullname=results["richSnippet"]["hcard"]['fn']
                    try:
                        title=results["richSnippet"]["hcard"]["title"]
                    except:
                        title=''
                    try:
                        role=results["richSnippet"]["person"]["role"]
                    except:
                        role=''
                    try:
                        organization=results["richSnippet"]["person"]["org"]
                    except:
                        organization=''
                    try:
                        profile_image=results["richSnippet"]["cseImage"]["src"]
                    except:
                        profile_image=''
                    outcheck=1
            else:
                break
            #profile_link=results["url"]
##        try:
##            if fullname.encode("utf-8").lower()==name.encode("utf-8").lower():
##                name_match=1
##                c1=company.encode("utf-8")
##                c2=organization.encode("utf-8")
##                list_remove=['services','international',' (s)',' (sea)',' (singapore)',' (pte)','(s)','(sea)','(singapore)','singapore','(pte)',' pte',' ltd','pte','ltd',' private',' limited','private','limited',',','.',' ']
##                for li in list_remove:
##                    c1=c1.lower().replace(li,'')
##                    c2=c2.lower().replace(li,'')
##                if c1==c2:
##                    company_match=1
##                else:
##                    company_match=0
##            else:
##                name_match=0
##                company_match=0 
##        except:
##            pass
        if outcheck==1:
            try:   
                fd = open(str(input_file)+'_output.csv','a')
                fd.write('"'+str(link1.encode("utf-8"))+'";"'+str(fullname.encode("utf-8"))+'";"'+str(title.encode("utf-8"))+'";"'+str(role.encode("utf-8"))+'";"'+str(organization.encode("utf-8"))+'";"'+str(profile_link.encode("utf-8"))+'";"'+str(profile_image.encode("utf-8"))+'"\n')
                fd.close()
            except Exception as e:
                    print(str(e))
    except Exception as e:
        print(str(e))
        if str(e)=="'hcard'":
        	try:
				fd = open('need_to_run_test.csv','a')
				fd.write('"'+str(name.encode("utf-8"))+'";"'+str(company.encode("utf-8"))+'";"'+str(email.encode("utf-8"))+'"\n')
				fd.close()
		except:
				pass
