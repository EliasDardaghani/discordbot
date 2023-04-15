import requests
import logging
import re
from models import Adealsweden, Swedroid
import os

ADEALSWEDEN = 'https://www.adealsweden.com/deals/8/'
SWEDROID_USERNAME = 'SWEDROID_USERNAME'
SWEDROID_PASSWORD = 'SWEDROID_PASSWORD'
SWEDROID_LOGIN = 'https://swedroid.se/forum/login/login'
SWEDROID = 'https://swedroid.se/forum/threads/fyndtipstraden-amazon-se-inga-diskussioner.186347/'

class Scrapers():

    def __init__(self):
        self.logger = logging.getLogger('discord')
        self.adealsweden = []
        self.adealsweden_old = None
        self.swedroid = []
        self.swedroid_old = None

    def scrape_adealsweden(self):
        self.logger.info('Scraping adealsweden')
        self.adealsweden.clear()
        response = requests.get(ADEALSWEDEN)
        response_text = response.text
        name_pattern = r'<a\shref\=\"https\:\/\/www\.adealsweden\.com\/[\w\S]+\/\d+\/\"\starget.*>(.*)<'
        price_pattern = r'\<em\>(.*)\<\/em\>\<\/strong\>(.*)\<\/p\>'
        url_pattern = r'\"(https://amzn\.to.*)\"\s'
        name_matches = re.findall(name_pattern, response_text, re.MULTILINE)
        prices_matches = re.findall(price_pattern, response_text, re.MULTILINE)
        url_matches = re.findall(url_pattern, response_text, re.MULTILINE)
        if name_matches and prices_matches and url_matches:
            if self.adealsweden_old:
                tmp = None
                for i, n in enumerate(name_matches):
                    real_url = requests.get(url_matches[i]).url.split('?')[0]
                    if real_url == 'https://www.amazon.se/s':
                        real_url = requests.get(url_matches[i]).url
                    name_match = n
                    if '&#038;' in name_match:
                        name_match = name_match.replace('&#038;', '&')
                    if '&#8211;' in name_match:
                        name_match = name_match.replace('&#8211;', '-')
                    ad = Adealsweden(name_match, ''.join(prices_matches[i]).strip(), real_url)
                    if i == 0:
                        tmp = ad
                    if self.adealsweden_old.name == name_match:
                        break
                    self.adealsweden.append(ad)
                self.adealsweden_old = tmp
            else:
                real_url = requests.get(url_matches[0]).url.split('?')[0]
                if real_url == 'https://www.amazon.se/s':
                    real_url = requests.get(url_matches[0]).url
                name_match = name_matches[0]
                if '&#038;' in name_match:
                    name_match = name_match.replace('&#038;', '&')
                if '&#8211;' in name_match:
                    name_match = name_match.replace('&#8211;', '-')
                ad = Adealsweden(name_match, ''.join(prices_matches[0]).strip(), real_url)
                self.adealsweden_old = ad
        self.logger.info(f'Scraped adealsweden.com: {self.adealsweden}')
        return self.adealsweden

    def scrape_swedroid(self):
        self.logger.info('Scraping swedroid')
        self.swedroid.clear()
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        session = requests.Session()
        session.get('https://swedroid.se/forum/login')
        response = session.post(url=SWEDROID_LOGIN, headers=headers, data=f'login={os.getenv(SWEDROID_USERNAME)}&register=0&password={os.getenv(SWEDROID_PASSWORD)}&remember=1&cookie_check=1&_xfToken=&redirect=https%3A%2F%2Fswedroid.se%2Fforum%2F')
        response = session.get(SWEDROID)
        response_text = response.text
        last_pattern = r'data\-last\=\"(\d+)\"'
        last_matches = re.findall(last_pattern, response_text, re.MULTILINE)
        if last_matches:
            response = session.get(SWEDROID + f'page-{last_matches[0]}')
            response_text = response.text
            url_pattern = r'\<a\shref\=\"(https://www\.amazon\.se.*)\"\starget'
            url_matches = re.findall(url_pattern, response_text, re.MULTILINE)
            if url_matches:
                if self.swedroid_old:
                    tmp = None
                    for i, u in reversed(list(enumerate(url_matches))):
                        droid = Swedroid(url=url_matches[i])
                        if i == len(url_matches)-1:
                            tmp = droid
                        if self.swedroid_old.url == u:
                            break
                        self.swedroid.append(droid)
                    self.swedroid_old = tmp
                else:
                    droid = Swedroid(url=url_matches[-1])
                    self.swedroid_old = droid
        self.logger.info(f'Scraped swedroid.se: {self.swedroid}')
        return self.swedroid
