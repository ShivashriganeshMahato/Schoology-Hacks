import requests
from bs4 import BeautifulSoup
import time

def makeSoup(url):
    return BeautifulSoup(s.get(url,timeout=None).text,'html.parser')

def retrieve_emails(identifiers,file):
        for identifier in identifiers:
            req = s.get("https://schoology.hsd.k12.or.us"+identifier["href"]+"/info",timeout=None)
            print(req)
            soup = BeautifulSoup(req.text,'html.parser')
            email_tag = soup.find(class_="admin-val email")
            count=0
            while email_tag==None and count<5:    # for some reason the email may not be noticed, in this case repeat the request until it is
                profile = s.get("https://schoology.hsd.k12.or.us"+identifier["href"]+"/info",timeout=None)
                print(profile)
                soup = BeautifulSoup(profile.text,'html.parser')
                email_tag = soup.find(class_="admin-val email")
                count+=1
            if email_tag!=None:
                print(email_tag.a.text)
                file.write(email_tag.a.text+"\n")


with requests.Session() as s:
    #retrieve the session-unique form_build_id
    soup = makeSoup('https://schoology.hsd.k12.or.us/login/ldap')
    hidden_values = soup.find_all("input",type="hidden")
    form_build_id = hidden_values[1]["value"]

    login = {'mail':'kenei135',             # username
           'pass':'',             # password
           'school_nid':'72935507',         # school-specific number
           'form_id':'s_user_login_form',   # type of form being posted
           'form_build_id':form_build_id}   # unique id
    #send login data to the server
    r = s.post("https://schoology.hsd.k12.or.us/login/ldap",data=login)

    emails_file = open('emails.txt','w')
    for p in range(1,97):
        time.sleep(5)
        soup = makeSoup('https://schoology.hsd.k12.or.us/network?p='+str(p))
        identifiers = soup.find_all("a",title="View user profile.")
        identifiers = identifiers[1:]  # cutting myself out of the list
        
        retrieve_emails(identifiers,emails_file)
        print("Finished writing emails from page",p)
    emails_file.close()
