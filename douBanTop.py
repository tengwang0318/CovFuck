import requests
from bs4 import BeautifulSoup
import lxml
import csv
from collections import defaultdict
import time

info = defaultdict(list)


def request_douBan(url):
    try:
        response = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"})
        print(response.status_code)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None


def main(page):
    url = 'https://movie.douban.com/top250?start=' + str(page * 25) + '&filter='
    html = request_douBan(url)

    soup = BeautifulSoup(html, 'lxml')
    save_data(soup)


def save_data(soup):
    a_list = soup.find(class_='grid_view').find_all('li')
    for item in a_list:
        item_name = item.find(class_='title').string
        item_img = item.find('a').find('img').get('src')
        item_index = item.find(class_='').string
        item_score = item.find(class_='rating_num').string
        item_author = item.find('p').text
        try:
            item_intro = item.find(class_='inq').string
        except AttributeError:
            item_intro = "None"
        print('爬取电影：' + item_index + ' | ' + item_name + ' | ' + item_score + ' | ' + item_intro)
        info['name'].append(item_name)
        info['img'].append(item_img)
        info['index'].append(item_index)
        info['score'].append(item_score)
        info['author'].append(item_author)
        info['intro'].append(item_intro)
    # with open('douBanTop.csv', 'w', newline='', encoding='utf-8-sig') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(['name', 'img', 'index', 'score', 'author', 'intro'])
    #
    #     a_list = soup.find(class_='grid_view').find_all('li')
    #
    #     for item in a_list:
    #         item_name = item.find(class_='title').string
    #         item_img = item.find('a').find('img').get('src')
    #         item_index = item.find(class_='').string
    #         item_score = item.find(class_='rating_num').string
    #         item_author = item.find('p').text
    #         try:
    #             item_intro = item.find(class_='inq').string
    #         except AttributeError:
    #             item_intro = "None"
    #
    #         # print('爬取电影：' + item_index + ' | ' + item_name +' | ' + item_img +' | ' + item_score +' | ' + item_author +' | ' + item_intr )
    #         print('爬取电影：' + item_index + ' | ' + item_name + ' | ' + item_score + ' | ' + item_intro)
    #         writer.writerow([item_name, item_img, item_index, item_score, item_author, item_intro])
    # a_list = soup.find(class_='grid_view').find_all('li')

    # print('爬取电影：' + item_index + ' | ' + item_name +' | ' + item_img +' | ' + item_score +' | ' + item_author +' | ' + item_intr )


# def save_to_excel(soup):
if __name__ == "__main__":
    for i in range(10):
        main(i)
        time.sleep(10)
    print(info['intro'])
    with open('douBanTop.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['name', 'img', 'index', 'score', 'author', 'intro'])
        for i in range(len(info['name'])):
            writer.writerow([info['name'][i], info['img'][i], info['index'][i], info['score'][i], info['author'][i],
                             info['intro'][i]])
