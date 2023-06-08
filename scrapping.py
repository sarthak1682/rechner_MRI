 
import requests
from bs4 import BeautifulSoup
import json

def scrape_data(year):

    normal_url = 'https://oeffentlicher-dienst.info/c/t/rechner/tv-l/west?id=tv-l-' + str(year) + '&matrix=1'
    doctor_url = 'https://oeffentlicher-dienst.info/c/t/rechner/aerzte/uniklinik?id=tv-aerzte-' + str(year) + '&matrix=1'
    normal_url_year = normal_url + '2'
    doctor_url_year = doctor_url +  '2'

    urls_year = [normal_url_year, doctor_url_year]
    urls_month = [normal_url, doctor_url]
    # create empty dictionary to store data
    a_links_month = []
    a_links_year = []

    for url in urls_month:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        # extract data from soup and add to dictionary
        for link in soup.find_all('a'):
            a_links_month.append(link)

    for url in urls_year:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        # extract data from soup and add to dictionary
        for link in soup.find_all('a'):
            a_links_year.append(link)

    a_links_month = [link for link in a_links_month if str(link).startswith('<a href="/c/t/rechner/tv-l/west?id=') or str(link).startswith('<a href="/c/t/rechner/aerzte/uniklinik?id=')]
    a_links_year = [link for link in a_links_year if str(link).startswith('<a href="/c/t/rechner/tv-l/west?id=') or str(link).startswith('<a href="/c/t/rechner/aerzte/uniklinik?id=')]
    table_month = {}
    table_year = {}
    for link in a_links_month:
        #Find string between g= and &s
        key = link.get('href').split('g=')[1].split('&s')[0]
        stufe = int(link.get('href').split('s=')[1].split('&')[0])
        #Find string between <span style="white-space:nowrap;"> and </span> and delete whitespaces
        value = link.find('span').text.strip()
        substring_to_remove = '\u2009'
        if substring_to_remove in value:
            value = value.replace(substring_to_remove, '')
        # Create new dictionary if key is not in table
        if key not in table_month:
            table_month[key] = dict()
        table_month[key][stufe] = float(value)

    for link in a_links_year:
        #Find string between g= and &s
        key = link.get('href').split('g=')[1].split('&s')[0]
        stufe = int(link.get('href').split('s=')[1].split('&')[0])
        #Find string between <span style="white-space:nowrap;"> and </span> and delete whitespaces
        value = link.find('span').text.strip()
        # Create new dictionary if key is not in table
        substring_to_remove = '\u2009'
        if substring_to_remove in value:
            value = value.replace(substring_to_remove, '')
        if key not in table_year:
            table_year[key] = dict()

        table_year[key][stufe] = float(value)
    return table_month, table_year