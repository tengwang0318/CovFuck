import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import csv

data = defaultdict(list)


def request_bilibili_DWG(url):
    try:
        response = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"})
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None


def main(page):
    url = 'https://search.bilibili.com/all?keyword=DWG&from_source=nav_suggest_new&page=' + str(page)
    html = request_bilibili_DWG(url)
    soup = BeautifulSoup(html, 'lxml')
    save_data(soup)


def save_data(soup):
    a_list = soup.find(class_='video-list clearfix').find_all('li')
    for item in a_list:
        item_title = item.find('a').get('title')
        item_url = item.find('a').get('href')[2:]
        item_description = item.find(class_="des hide").text
        item_page_view = item.find(class_='so-icon watch-num').text
        item_barrage = item.find(class_="so-icon hide").text
        item_up = item.find(class_="up-name").text
        data['title'].append(item_title)
        data['url'].append(item_url)
        data['description'].append(item_description)
        data['page_view'].append(item_page_view)
        data['barrage'].append(item_barrage)
        data['up'].append(item_up)


if __name__ == "__main__":
    for i in range(1, 11):
        main(i)
    with open('DWGnb.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['title', 'url', 'description', 'page view', 'barrage', 'up'])
        for i in range(len(data['title'])):
            writer.writerow(
                [data['title'][i], data['url'][i], data['description'][i], data['page_view'][i], data['barrage'][i],
                 data['up'][i]])
