from bs4 import BeautifulSoup
import requests
import pandas as pd
for i in range(2016, 2021):
    url1 = "https://summerofcode.withgoogle.com"
    url2 = url1 + "/archive/"+str(i)+"/organizations/"
    page = requests.get(url2)

    divsoup = BeautifulSoup(page.content, "lxml")
    org_cards = divsoup.find_all('li',class_="organization-card__container")

    org_details = {"Organisation Name":[] ,"Organisation Tagline":[], "Technologies Used":[], "GSOC Organisation Link":[]}

    for org in org_cards:
        org_name = org.find('h4', class_="organization-card__name font-black-54").text
        org_tagline = org.find('div', class_="organization-card__tagline font-black-54").text
        url3 = url1 + org.a['href']
        org_page = requests.get(url3)
        org_page = BeautifulSoup(org_page.content, 'lxml')
        org_techs = org_page.find_all('ul', class_="org__tag-container")
        tech_list = ""
        for tech in org_techs:
            if not len(tech_list):
                tech_list = tech_list + tech.li.text.strip()
                continue
            tech_list = tech_list +",  " + tech.li.text.strip()
        org_details["Organisation Name"].append(org_name)
        org_details["Organisation Tagline"].append(org_tagline)
        org_details["Technologies Used"].append(tech_list)
        org_details["GSOC Organisation Link"].append(url3)

    df = pd.DataFrame(org_details)
    df.to_csv('Gsoc-'+str(i)+'.csv')