import requests
from bs4 import BeautifulSoup
import csv

with open("qiushibaike.csv", 'a+', encoding='utf-8-sig', newline="") as f:
    writer = csv.writer(f)
    writer.writerow(['name', 'level', 'feel funny', 'comment', 'content'])


def request_joker(url):
    try:
        response = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"})
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None


def main(page):
    url = "https://www.qiushibaike.com/text/page/" + str(page) + "/"
    response = request_joker(url)
    soup = BeautifulSoup(response, 'lxml')
    save_data(soup)


def save_data(soup):
    a_list = soup.find_all(class_="article block untagged mb15 typs_hot")
    for item in a_list:
        author = item.find('a').find('img').get('alt')

        try:
            level = item.find(class_='articleGender manIcon').string
        except AttributeError:
            level = item.find(class_="articleGender womenIcon").string

        feel_funny = item.find(class_="stats-vote").find(class_='number').string
        comment = item.find(class_="stats-comments").find(class_='number').string
        content = item.find(class_="content").text
        with open("qiushibaike.csv", 'a+', encoding='utf-8-sig', newline="") as f:
            writer = csv.writer(f)
            writer.writerow([author, level, feel_funny, comment, content])
        print(author, "||", level, "||", feel_funny, "||", comment, "||", content)


if __name__ == '__main__':

    for i in range(1, 10):
        main(i)
