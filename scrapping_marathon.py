#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pdb
import pandas as pd
from bs4 import BeautifulSoup
import time
import re

def get_html(url):
    # Open Chrome Driver
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(2)
    htmlSource = driver.page_source
    driver.close()

    return htmlSource

def get_runner_info(bib):
    # Id
    marathon_url = 'https://results.nyrr.org/runner/{bib}/result/M2018'.format(bib=bib)
    runner = dict()

    # Get html source page
    htmlSource = get_html(marathon_url)
    soup = BeautifulSoup(htmlSource, 'lxml')

    # Check if the page returns a runner, if not return empty dictionary
    res = soup.findAll("h1", {"class": "ng-binding"})
    if not res:
        return runner

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
    with open(filename, 'a') as f:
        df.to_csv(f, header=header)

def scrape_all_data(filename):
    # Maximum number of runners + Wheelchair + Handcycles
    total = 52697 + 56 + 52

    # When to initialize bib
    bib = 2301
    csv_len = 0
    d = []
    # Loop
    while csv_len < total:
        # Get dictionary with all runners bib info
        runner_info = get_runner_info(bib)
        # Append dictionary to list
        if runner_info:
            d.append(runner_info)
            csv_len += 1

        bib += 1
        # Verbose
        if bib % 10 == 0:
            print('{}'.format(bib))

        # Save every 100 runners
        if bib % 100 == 0:
            print('{bib} ...'.format(bib=bib))
            print('This many: {csv_len}'.format(csv_len=csv_len))
            print('---------------------------------')
            store_d(d, filename, bib)
            d = []

    store_d(d, filename, bib)

if __name__ == "__main__":
    scrape_all_data('testing_marathon.csv')

