import urllib.request
from bs4 import BeautifulSoup
import re
import time
import json
from datetime import date
import os


zodiac = [
        'aries',
        'taurus',
        'gemini',
        'cancer',
        'leo',
        'virgo',
        'libra',
        'scorpio',
        'sagittarius',
        'capricorn',
        'aquarius',
        'pisces'
]

site_instances = [['HoroscopeCom',
                    'http://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx?sign=',
                    list(i for i in range(1, 13)),
                    ['div', 'horoscope-content', 0]],
                    
                    ['HoroscopeCoUk',
                    'http://horoscope.co.uk/',
                    zodiac,
                    ['div', 'daily-reading', 0]],
                    
                    ['HoroscopesCoUk',
                    'http://www.horoscopes.co.uk/',
                    list(sign.capitalize() for sign in zodiac),
                    ['p', None, -1]],
                    
                    ['Elle',
                    'http://www.elle.com/horoscopes/daily/',
                    list(sign + '-daily-horoscope' for sign in zodiac),
                    ['p', None, 2]],
]

with open('update_log.json', 'r+') as f: update_log = json.load(f)
f.close()       
    
class HoroscopeParser:
    '''Opens website, reads data and saves horoscopes in txt files sorted by source
    
        self.name -> reference name
        self.url -> full path without the suffix to exact zodiac sign
        self.zodiac_list -> a list of suffixes to the 12 zodiac signs
        self.id_tags -> list of 3 identifiers [HTML tag name, tag id, position]'''
        
    
    def __init__(self, name, url, zodiac_list, id_tags):
        self.name = name
        self.url = url
        self.zodiac_list = zodiac_list
        self.id_tags = id_tags
                       
    def extract_text(self, zodiac):
        '''opens URL, makes the soup, finds, text and
           returns text'''
        
        print('Extracting ' + zodiac + ' from', self.name)
        print(self.url+zodiac)
        
        try:
            html = urllib.request.urlopen(self.url+zodiac)
        except urllib.error.HTTPError:
            print('ERROR! Website currently not available!')
            return
            
        soup = BeautifulSoup(html, 'html.parser')
        try:
            text = soup.findAll(self.id_tags[0], self.id_tags[1])[self.id_tags[2]].get_text()
        except IndexError:
            print('ERROR! Text not found! Please re-check HTML tags.')
            return
             
        html.close()
     
        text = HoroscopeParser.clean_text(self, text)
       
        return text
     
     
    def clean_text(self, text):
        '''removes numbers and zodiac names'''
        
        text = re.sub('[0-9]+', '', text)
        
        for sign in zodiac:
            text = re.sub(sign.capitalize(), '', text)
        
        
    def extract_all(self):
        '''loop to get all 12 signs'''
        
        try:
            if update_log[self.name] == str(date.today()):
                print(self.name + ' has already been extracted today.\nSkipping...\n')
                return
            else:
                update_log[self.name] = str(date.today())
        except KeyError:
            update_log[self.name] = str(date.today())
            
        for sign in self.zodiac_list:
            hcope_text = HoroscopeParser.extract_text(self, str(sign))
            
            fname = str(sign)[:2] + '_' + self.name + '_' + str(date.today()) + '.txt'
            with open(os.path.join('./training_data', fname), 'w+') as f: f.write(str(hcope_text) + '\n')
            f.close()
            
            print("Extraction completed.\nWaiting 5 seconds...")
            time.sleep(5)
        
        
    
####################    

def scrape():
    print('Hello.\nStarting daily scraping...\n\n')

    for site_data in site_instances:
        crawler = HoroscopeParser(site_data[0], site_data[1], site_data[2], site_data[3])
        crawler.extract_all()

    print('\nExtraction finished.')

    with open('update_log.json', 'w+') as f: json.dump(update_log, f)
    f.close()
