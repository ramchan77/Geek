import urllib2
import json
import pandas as pd
import time
import glob
import string

csv_files=glob.glob('*.csv')
input_file=string.replace(csv_files[0], '.csv', '')
input_data=pd.read_csv(str(input_file)+'.csv',encoding='utf-8',error_bad_lines=False,sep=';')
count=0
name_match=0
company_match=0
fd = open(str(input_file)+'_output.csv','a')
fd.write('Given Name;Given company;Email;Fullname;Title;Role;Organization;Profile Link;Name Match;Company Match\n')
fd.close()
api_token='AKaTTZiNwbfI2l8s3GSt8vaIuUYM:1543494310481'
for index,name,company,email in input_data.itertuples():
    try:
        count+=1
        print(str(count)+' '+str(email.encode("utf-8")))
        #print("Before")
        given_name=name.encode("utf-8").lower()
        given_company=company.encode("utf-8")
        list_remove=['services','international',' (s)',' (sea)',' (singapore)',' (pte)','(s)','(sea)','(singapore)','singapore','(pte)',' pte',' ltd','pte','ltd',' private',' limited','private','limited',',','.']
        for li in list_remove:
        	given_company=given_company.lower().replace(li,'')
        given_company=given_company.lower().replace(' ','%20')
        given_name=given_name.lower().replace(' ','%20')
        search_query=given_company+'%2C'+given_name+'%2Csingapore'
        def reload_json(email):
            data=''
            try:
            	url_link="https://cse.google.com/cse/element/v1?rsz=filtered_cse&num=1&hl=en&source=gcsc&gss=.com&sig=76c37a052829ad2c9825658fbbc50bce&cx=011658049436509675749:gkuaxghjf5u&q="+search_query+"&safe=off&cse_tok="+api_token+"&sort=&exp=csqr,4200995&googlehost=www.google.com&oq="+search_query+"&gs_l=partner-generic.3...25463.33220.2.33524.0.0.0.0.0.0.0.0..0.0.gsnos%2Cn%3D13...0.7760j8723106j16..1ac.1.25.partner-generic..0.0.0.&callback=google.search.Search.csqr9114"
            	#print(url_link)
                fd = open('url_output.csv','a')
                fd.write(url_link+'\n')
                fd.close()        	
                data = urllib2.urlopen(url_link,timeout=15)
                return data
            except Exception as e:
                print(str(e))
                if str(e)=='<urlopen error [Errno 11001] getaddrinfo failed>':
                    time.sleep(25)
                    reload_json(email)
                return data
        data=reload_json(email)
        #print("After")
        dd=data.read()
        dd=dd.replace('/*O_o*/\ngoogle.search.Search.csqr9114(','')
        dd=dd.replace(');','')
        filename = "jj.json"
        file_ = open(filename, 'w')
        file_.write(dd)
        file_.close()
        with open('jj.json') as f:
            data1 = json.load(f)
        fullname=data1['results'][0]["richSnippet"]["hcard"]['fn']
        try:
            title=data1['results'][0]["richSnippet"]["hcard"]["title"]
        except:
            title=''
        try:
            role=data1['results'][0]["richSnippet"]["person"]["role"]
        except:
            role=''
        try:
            organization=data1['results'][0]["richSnippet"]["person"]["org"]
        except:
            organization=''
        profile_link=data1['results'][0]["url"]
        try:
            if fullname.encode("utf-8").lower()==name.encode("utf-8").lower():
                name_match=1
                c1=company.encode("utf-8")
                c2=organization.encode("utf-8")
                list_remove1=['services','international',' (s)',' (sea)',' (singapore)',' (pte)','(s)','(sea)','(singapore)','singapore','(pte)',' pte',' ltd','pte','ltd',' private',' limited','private','limited',',','.',' ']
                for li1 in list_remove1:
                    c1=c1.lower().replace(li1,'')
                    c2=c2.lower().replace(li1,'')
                if c1==c2:
                    company_match=1
                else:
                    company_match=0
            else:
                name_match=0
                company_match=0 
        except:
            pass   
        try:   
            fd = open(str(input_file)+'_output.csv','a')
            fd.write('"'+str(name.encode("utf-8"))+'";"'+str(company.encode("utf-8"))+'";"'+str(email.encode("utf-8"))+'";"'+str(fullname.encode("utf-8"))+'";"'+str(title.encode("utf-8"))+'";"'+str(role.encode("utf-8"))+'";"'+str(organization.encode("utf-8"))+'";"'+str(profile_link.encode("utf-8"))+'";"'+str(name_match)+'";"'+str(company_match)+'"\n')
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
