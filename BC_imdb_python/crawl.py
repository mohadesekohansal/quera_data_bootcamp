# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.5
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time
import json
import csv

options = Options()

driver = webdriver.Chrome(chrome_options=options)

url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'

driver.get(url)
time.sleep(10)

title = []
year = []
parental_guide = []
runtime = []
genre = []
person = []
story_line = []
gross_us_canada = []

all_links = driver.find_elements(By.XPATH,'//td[contains(@class ,"titleColumn")]/a')


def crawl(first_rank , last_rank):     
    all_links = driver.find_elements(By.XPATH,'//td[contains(@class ,"titleColumn")]/a')
    for rank in range(first_rank,last_rank+1):
        movie_id_data = all_links[rank-1].get_attribute("href").split('/tt')[1].split('/')[0]
        all_links[rank-1].click()
        title_data = driver.find_element(By.XPATH,'//span[@class = "sc-afe43def-1 fDTGTb"]')
        details = driver.find_elements(By.XPATH,'//ul[@class = "ipc-inline-list ipc-inline-list--show-dividers sc-afe43def-4 kdXikI baseAlt"]/li')
        if len(details)==3:
            year_data = details[0]
            parental_guide_data = details[1]
            runtime_data = details[2]
        else:
            year_data = details[0]
            parental_guide_data = 'NULL'
            runtime_data = details[1]
        
        
        genres_data = driver.find_elements(By.XPATH,'//a[@class = "ipc-chip ipc-chip--on-baseAlt"]/span[@class = "ipc-chip__text"]')
        try:
            gross_us_canada_data = driver.find_element(By.XPATH,'//div[@data-testid = "title-boxoffice-section"]/ul/li[@data-testid = "title-boxoffice-grossdomestic"]/div/ul/li/span')
        except:
            gross_us_canada_data = 'NULL'
        crews_for_count = driver.find_elements(By.XPATH,'//div[@class="sc-52d569c6-3 jBXsRT"]/div/ul/li/div')
        crews = driver.find_elements(By.XPATH,'//div[@class="sc-52d569c6-3 jBXsRT"]/div/ul/li/div/ul/li/a')
        director_count = len(crews_for_count[0].get_attribute("innerHTML").split('<a'))-1
        writer_count = len(crews_for_count[1].get_attribute("innerHTML").split('<a'))-1
        star_count = len(crews_for_count[2].get_attribute("innerHTML").split('<a'))-1
        directors_data = []
        writers_data = []
        stars_data = []
        for i in range(director_count):
            id = crews[i].get_attribute("href").split('/nm')[1].split('/')[0]
            directors_data.append((crews[i].text,id))
        for i in range(writer_count):
            id = crews[i+director_count].get_attribute("href").split('/nm')[1].split('/')[0]
            writers_data.append((crews[i+director_count].text,id))
        for i in range(star_count):
            id = crews[i+director_count+writer_count].get_attribute("href").split('/nm')[1].split('/')[0]
            stars_data.append((crews[i+director_count+writer_count].text,id))

        

        title.append((title_data.text,movie_id_data,rank))
        year.append((year_data.text,rank))
        try:
            parental_guide.append((parental_guide_data.text,rank))
        except:
            parental_guide.append((parental_guide_data,rank))

        runtime.append((runtime_data.text,rank))
        for item in genres_data:
            genre.append((item.text,rank))
        for person_data in directors_data:
            person.append((person_data, 0,rank))
        for person_data in writers_data:
            person.append((person_data, 1,rank))
        for person_data in stars_data:
            person.append((person_data,2,rank))
        try:
            gross_us_canada.append((gross_us_canada_data.text,rank))
        except:
            gross_us_canada.append((gross_us_canada_data,rank))
        driver.back()
        all_links = driver.find_elements(By.XPATH,'//td[contains(@class ,"titleColumn")]/a')


# # Output

data = {
    'title':title,
    'year':year,
    'parental_guide':parental_guide,
    'runtime':runtime,
    'genre':genre,
    'person':person,
    'story_line':story_line,
    'gross_us_canada':gross_us_canada
};

with open("imdb_data.txt", "w") as fp:
    json.dump(data, fp) 

with open("imdb_data.csv", "w", newline="") as fp:
    writer = csv.DictWriter(fp, fieldnames=data.keys())
    writer.writeheader()
    writer.writerow(data)
