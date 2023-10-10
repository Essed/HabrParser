import csv
import re
import requests
from bs4 import BeautifulSoup
from helpers import repeator

URL = 'https://freelance.habr.com/tasks?categories=development_all_inclusive%2Cdevelopment_backend%2Cdevelopment_frontend%2Cdevelopment_prototyping%2Cdevelopment_ios%2Cdevelopment_android%2Cdevelopment_desktop%2Cdevelopment_bots%2Cdevelopment_games%2Cdevelopment_1c_dev%2Cdevelopment_scripts%2Cdevelopment_voice_interfaces%2Cdevelopment_other'
HEADERS = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36','accept':'*/*'}
HOST='https://freelance.habr.com'
FILE='C:/Users/vipar/OneDrive/Desktop/FData/habrorders.csv'

def get_html(url,params=None):
     r = requests.get(url, headers=HEADERS, params=params)
     return r

def get_content(html):
     soup = BeautifulSoup(html,'html.parser')
     items = soup.find_all('li', class_='content-list__item')
     cards = []
     for item in items:
          price = item.find('span',class_='count')
          link= HOST + item.find('a').get('href')
          if price :
               price = price.get_text()
          else:
               price ='Договорная'
          cards.append({
               'title':item.find('div',class_='task__title').get_text(strip=True),
               'link': link,
               'price':price
          })
     return cards

def save_file(items, path):
     with open(path, 'w', newline='', errors='ignore') as file:
          writer = csv.writer(file, delimiter=';')
          writer.writerow(['Название','Ссылка','Cтоимость'])
          for item in items:
               writer.writerow([item['title'],item['link'],item['price']])


@repeator(30)
def parse():
     html = get_html(URL)
     soup = BeautifulSoup(html.text,'html.parser')
     allpages = soup.find_all('div',class_='page')
     for x in allpages:
          pages=x.find('div',class_='pagination').get_text()
     pages_count= re.findall(r'\d+', pages)
     work=[]
     if html.status_code==200:
          for page in range(1,int(pages_count[-1]) + 1):
               html = get_html(URL,params={'page':page})
               print(f'Парсин страницы: {page}')
               work.extend(get_content(html.text))     
     print(work)
     get_content(html.text)
     save_file(work,FILE)


if __name__ == "__main__":
     parse()  