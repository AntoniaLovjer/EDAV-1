#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pdb
from joblib import Parallel, delayed
import pandas as pd
from bs4 import BeautifulSoup
import time
import re

def get_html(url):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', options=options)
    # Open Chrome Driver
    driver.get(url)
    time.sleep(3)
    htmlSource = driver.page_source
    driver.close()

    return htmlSource

def get_runner_info(bib):
    # Id
    marathon_url = 'https://results.nyrr.org/runner/{bib}/result/M2017'.format(bib=bib)
    runner = dict()

    # Get html source page
    htmlSource = get_html(marathon_url)
    soup = BeautifulSoup(htmlSource, 'lxml')

    # Check if the page returns a runner, if not return empty dictionary
    res = soup.findAll("h1", {"class": "ng-binding"})
    if not res:
        return runner
    try:
        # Add bib id
        runner['bib'] = bib

        # Get Name
        res = soup.findAll("h1", {"class": "ng-binding"})[0]
        runner['name'] = res.text

        # Get Gender / Age
        res = soup.findAll("span", {"ng-if": "runnerInfo.age > 0"})
        if res:
            runner['gender_age'] = res[0].text.strip().split()[0]
        else:
            runner['gender_age'] = ''

        # Get Place
        res = soup.findAll("span", {"class": "gotham-book-font ng-binding"})
        if res:
            runner['place'] = res[0].text
        else:
            runner['place'] = ''

        # Get Team info
        res = soup.findAll("span", {"ng-if": "runnerInfo.teamName"})
        if res:
            runner['team'] = res[0].text.replace('|','').strip()
        else:
            runner['team'] = 0

        # General Metrics
        metric_names = ['official_time', 'pace_per_mile', 'place_overall',
                    'place_gender', 'place_age-group','place_age-graded',
                    'time_age-graded', 'percentile_age-graded', 'gun_time',
                    'gun_place']
        # Splint names from html
        res_splint = soup.findAll("label", {"class": "ng-binding"})
        splint_names = ['splint_{}'.format(res_i.text.lower())
                        for res_i in res_splint[1:]]
        # Combine metric names
        all_metric_names = metric_names + splint_names

        # Get values for all metric names
        res = soup.findAll("span", {"class": "label-value ng-binding"})
        res_text = [res_i.text for res_i in res]
        for i in range(len(all_metric_names)):
            runner[all_metric_names[i]] = res_text[i]

        # Metrics of
        metric_of_names = ['place_overall_of', 'place_gender_of',
                           'place_age-group_of', 'place_age-graded_of']
        res = soup.findAll("span", {"class": "label-value-of ng-binding"})
        res_text = [re.findall(r'\d+(?:,\d+)?', res_i.text)[0] for res_i in res]
        for i in range(len(metric_of_names)):
            runner[metric_of_names[i]] = res_text[i]

    except:
        pass

    return runner

def store_d(d, filename, bib):
    """
    Stores dictionary into filename

    d: list of dictionaries with runners information
    filename: name of the file
    bib: last bib id
    """
    header = False
    # If it is the first chunk to save keep header
    if bib == 100:
        header = True

    df = pd.DataFrame(d)
    df.dropna(inplace=True)
    with open(filename, 'a') as f:
        df.to_csv(f, header=header, index=False)


if __name__ == "__main__":
    #scrape_all_data('testing_marathon.csv')
    # When to initialize bib
    filename = 'marathon_2017.csv'
    bib_start = 0
    bib_end = 100
    # Loop
    total = 70000

    while bib_start < total:
        res = Parallel(n_jobs=5)(delayed(get_runner_info)(bib)
            for bib in range(bib_start, bib_end))
        store_d(res, filename, bib_end)
        print('bib_end {}'.format(bib_end))
        bib_start = bib_end
        bib_end += 100

