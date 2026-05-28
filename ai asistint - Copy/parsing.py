from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://www.vesty.co.il/main/news'

def get_news():

  response = requests.get(url)

  bs = BeautifulSoup(response.text,"lxml")


  temp = bs.find_all('div', 'slotView')


  dict_news = {"news": [], "links": []}

  for i in temp:
    dict_news["news"].append(i.text)
    dict_news["links"].append(i.find('a').get('href'))


  return dict_news
