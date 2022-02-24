# 1st step install and import modules 
import requests
import csv 
from bs4 import BeautifulSoup
from itertools import zip_longest

job_title = []
company_name = []
location_name = []
job_skill = []
links = []
requirement = []
responsibilitie = []
date = []
page_nb = 0

while True:
    # 2nd step use requests to store the url
    try:
        result = requests.get("https://wuzzuf.net/search/jobs/?q=python&a=hpbhttps://wuzzuf.net/search/jobs/?a=hpb&q=python&start="+{page_nb})

        #3nd step save page content/markup
        src = result.content
        #print(src)

        #4nd step create soup object to parse content
        soup = BeautifulSoup(src,"lxml")
        #print(soup)
        
        page_limit = int(soup.find("span",{"class":"css-12razwi"}).text)
        
        if (page_nb > page_limit // 15):
            print("pages ended,terminate")
            break

        #5nd step
        job_titles = soup.find_all("h2",{"class":"css-m604qf"})
        company_names = soup.find_all("div",{"class":"css-d7j1kk"}) 
        location_names = soup.find_all("span",{"class":"css-5wys0k"})
        job_skills = soup.find_all("div",{"class":"css-y4udm8"})
        links =soup.find("div",{"class":"css-laomuu"}).find("a",href=True)
        posted_new = soup.find_all("div",{"class":"css-4c4ojb"})
        posted_old = soup.find_all("div",{"class":"css-do6t5g"})
        posted = [*posted_new,*posted_old]
        #6th step loop over returened lists to extract needed info ontro other lists
        for i in range(len(job_titles)):
            job_title.append(job_titles[i].text)
            links.append("https://wuzzuf.net" + job_titles[i].find("a").attrs['href'])
            company_name.append(company_names[i].text)
            location_name.append(location_names[i].text)
            job_skill.append(job_skills[i].text)
            date.append(posted[i].text.replace("-", "").strip())
            
        page_nb +=1
        print("page switched")
    except:
        print("error")
        break
    
#7th step create csv file and fill it with values
file_list = [job_title, company_name, location_name, job_skill, links, requirement, date]
exported = zip_longest(*file_list)

with open("C:/Users/LENOVO/OneDrive/Bureau/learn/python/webscraping/webscraping.csv", "w") as myfile:
    writer_object = csv.writer(myfile)
    writer_object.writerow(["job title", "company", "location", "skills", "links", "requirements", "date"])
    writer_object.writerows(exported)
    
    for link in links:
        result_link = requests.get(link)
        src_link = result_link.content
        soup_link = BeautifulSoup(src_link,"lxml")
        requirements = soup.find("section",{"class":"css-ghicub"}).find("div",{"class":"css-1t5f0fr"}).ul
        responsibilities = soup.find("section",{"class":"css-ghicub"}).find("div",{"class":"css-1uobp1k"}).ul
        response_text_requirment = ""
        response_text_resposibilitie = ""
        for li_req in requirements.find_all("li"):
            response_text_requirment += li_req.text+" | "
            response_text_requirment = response_text_requirment[:-2]
        requirement.append(response_text_requirment)
        for li in responsibilities.find_all("li"):
            response_text_responsibilitie += li.text+" | "
            response_text_responsibilitie = response_text_responsibilitie[:-2]
        responsibilitie.append(response_text_responsibilitie)
        

