# import requests
# from bs4 import BeautifulSoup
# import pandas as  pd
#
#
#
#
#
# HEADERS = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
#         "Accept-Language": "en-US,en;q=0.5",
#         "Accept-Encoding": "gzip, deflate",
#         "Connection": "keep-alive",
#         "Upgrade-Insecure-Requests": "1",
#         "Sec-Fetch-Dest": "document",
#         "Sec-Fetch-Mode": "navigate",
#         "Sec-Fetch-Site": "none",
#         "Sec-Fetch-User": "?1",
#         "Cache-Control": "max-age=0",
#     }
#
# #headers={"User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"}
# #headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
# HEADERS ={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
#
# #url to scrap
#
# #url = "https://www.indeed.com/jobs?q=data+scientist+%2420%2C000&l=New+York&start=1"
#
# url = "https://www.indeed.com/jobs?q=data+scientist+%2420%2C000&l=New+York&start=1"
#
# # Creating a session object to perform optimized requests
#
# session = requests.Session()
#
# html_text = requests.get(url,headers=HEADERS)
#
# print(html_text.status_code)
#
# # parsed_html_text = BeautifulSoup(html_text, "html.parser")
# # print(parsed_html_text)
#
# #company_name = parsed_html_text.find_all("a", {"data-tn-element": "companyName"})
#
# #print(company_name)
#
#
#
# ----------------------------------------------------------------------------
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Establish chrome driver and go to report site URL
def get_data_each_city(city):
    url = f"https://www.indeed.com/jobs?q=data+scientist+%2420%2C000&l={city}&start=2"
    driver = webdriver.Chrome()
    driver.get(url)
    #company_names = driver.find_element(By.CLASS_NAME,'turnstileLink companyOverviewLink')


    #company_names = driver.find_elements(By.TAG_NAME,'a')

    HTML_content = driver.find_element(By.XPATH,'/html/body')


    html_content = HTML_content.get_attribute("innerHTML")
    soup = BeautifulSoup(html_content, "html.parser")

    overal_company_list = soup.find_all("div", {"class": "mosaic mosaic-provider-jobcards mosaic-provider-hydrated"})

    #company_names = soup.find_all("a", {"class": "turnstileLink companyOverviewLink"})
    #job_titles = soup.find_all("a", {"class": "jcs-JobTitle css-jspxzf eu4oa1w0"})
    print(url)
    print(len(overal_company_list))


    for j in overal_company_list:
        company_names = j.find_all("span", {"class": "companyName"})
        job_titles = j.find_all("div", {"class": "css-1m4cuuf e37uo190"})
        location = j.find_all("div", {"class": "companyLocation"})
        salary = j.find_all("div", {"class": "heading6 tapItem-gutter metadataContainer noJEMChips salaryOnly"})
    print(len(company_names), len(job_titles), len(location), len(salary) )
    print("----------------------------------------------------------------------")
    print([title.text for title in job_titles])
    job_data_frame = {
        "company name": [company.text for company in company_names],
        "job title": [title.text for title in job_titles],
        "location": [loc.text for loc in location],
        "salary": [sa.text for sa in salary]

    }

    #converting the data in to data frame

    data_frame = pd.DataFrame(job_data_frame)


    #Storing the data in the csv file

    return data_frame


#city_data = ['New+York','Chicago','San+Francisco', 'Austin', 'Seattle', 'Los+Angeles', 'Philadelphia', 'Atlanta', 'Dallas', 'Pittsburgh', 'Portland', 'Phoenix', 'Denver', 'Houston', 'Miami', 'Washington+DC', 'Boulder']

city_data = ['New+York', 'San+Francisco', 'Austin', 'Los+Angeles', 'Atlanta', 'Dallas', 'Pittsburgh', 'Portland', 'Phoenix', 'Denver', 'Houston', 'Miami', 'Washington+DC']

for city in city_data:
    city_job_data = get_data_each_city(city)
    #sleep(5)

    #Converting the data in to csv file
    print("pass")
    city_job_data.to_csv(f"{city}_data.csv")


