import requests
from bs4 import  BeautifulSoup
import pandas as pd


topics_url = "https://github.com/topics"

# Fetching the html content

responce_object = requests.get(topics_url)

soup_object = BeautifulSoup(responce_object.text, "html.parser")

topics_p_tag = soup_object.find_all('p', {"class": "f3 lh-condensed mb-0 mt-1 Link--primary"})
description_p_tag = soup_object.find_all('p', {"class": "f5 color-fg-muted mb-0 mt-1"})
topics_a_links = soup_object.find_all('a', {"class": "no-underline flex-1 d-flex flex-column"})


topics_titles = []
topics_descriptions =[]
topics_links = []




for topic in topics_p_tag:
    topics_titles.append(topic.text.strip())

for descriotion in description_p_tag:
    topics_descriptions.append(descriotion.text.strip())


for link in topics_a_links:
    topics_links.append("https://github.com" + link['href'])


topics_dictionary = {
    "title": topics_titles,
    "description": topics_descriptions,
    "links": topics_links
}

data_frame = pd.DataFrame(topics_dictionary)

# saving the dataframe to the csv file.

data_frame.to_csv('git_hub_topics_data.csv', index=None)

# Extracting the data for each topic
# To reduce the execution time we are using the sesssion class in the requests module.

session  = requests.session()

for each_topic in topics_links:
     each_topic_session = session.get(each_topic)
     topic_soup_object = BeautifulSoup(each_topic_session.text, "html.parser")
     topic_heading = topic_soup_object.find_all('h1', {"class": "h1"})[0].text.strip()
     file_name = topic_heading + "_top_repos_data.csv"
     topics_repos = topic_soup_object.find_all("h3",{"class": "f3 color-fg-muted text-normal lh-condensed"} )#[0].find_all("a")
     user_name_list = []
     repo_name_list = []
     repo_url_list = []
     star_rating_list =[]
     star_ratings = topic_soup_object.find_all("span", {"class": "Counter js-social-count"})

     for topics_repo in topics_repos:
         user_name = topics_repo.find_all("a")[0].text.strip()
         repo_name = topics_repo.find_all("a")[1].text.strip()
         repo_url = "https://github.com" + topics_repo.find_all("a")[1]['href'].strip()
         user_name_list.append(user_name)
         repo_name_list.append(repo_name)
         repo_url_list.append(repo_url)
     for star_rating in star_ratings:
         star_rating_list.append(star_rating.text.strip())

     topic_repos_data = {
         "repo_user_name":  user_name_list,
        "repo_name": repo_name_list,
         "repo_url": repo_url_list,
         "repo_rating": star_rating_list
     }

     topic_repo_data_frame = pd.DataFrame(topic_repos_data)
     topic_repo_data_frame.to_csv(file_name, index=None)













