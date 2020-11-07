# coding=utf-8
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
from collections import defaultdict

browser = webdriver.Firefox()
WAIT = WebDriverWait(browser, 10)
browser.set_window_size(1400, 900)
data = defaultdict(list)
n = 1


def search():
    try:

        browser.get("https://www.bilibili.com/")
        #    #nav_searchform > input为输入框确定元素位置后复制selector
        # 此处EC为expected_conditions，就是找期望的“状态”

        input = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#nav_searchform > input")))
        submit = WAIT.until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div[2]/div/div[1]/div[1]/div/div[2]/div/form/div/button')))

        input.send_keys('iG')
        submit.click()

        # 跳转到新的窗口

        all_h = browser.window_handles
        browser.switch_to.window(all_h[1])
        get_source()

        # 此处css selector对应的是第几页按钮
        total = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                           "#all-list > div.flow-loader > div.page-wrap > div > ul > li.page-item.last > button")))
        return int(total.text)

    except TimeoutException:
        return search()


def next_page(page_num):
    try:

        next_btn = WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                          '#all-list > div.flow-loader > div.page-wrap > div > ul > li.page-item.next > button')))
        next_btn.click()
        WAIT.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,
                                                     '#all-list > div.flow-loader > div.page-wrap > div > ul > li.page-item.active > button'),
                                                    str(page_num)))
        get_source()
    except TimeoutException:
        browser.refresh()
        return next_page(page_num)


def save_to_excel(soup):
    a_list = soup.find(class_='video-list clearfix').find_all(class_='video-item matrix')

    for item in a_list:
        item_title = item.find('a').get('title')
        item_link = item.find('a').get('href')
        item_description = item.find(class_='des hide').text
        item_view = item.find(class_='so-icon watch-num').text
        item_biubiu = item.find(class_='so-icon hide').text
        item_date = item.find(class_='so-icon time').text
        data['title'].append(item_title)
        data['link'].append(item_link)
        data['description'].append(item_description)
        data['view'].append(item_view)
        data['biubiu'].append(item_biubiu)
        data['date'].append(item_date)

        global n

        n = n + 1


def get_source():
    WAIT.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '#all-list > div.flow-loader > div.filter-wrap')))

    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    save_to_excel(soup)


def main():
    try:
        total = search()

        for i in range(2, 10):
            next_page(i)
        #
        # for i in range(2, int(total + 1)):
        #     next_page(i)

    finally:
        with open('iGnb.csv', 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['title','link','description','view','biubiu','date'])
            for i in range(len(data['title'])):
                writer.writerow([data['title'][i],data['link'][i],data['description'][i],data['view'][i],data['biubiu'][i],data['date'][i]])
        browser.close()


if __name__ == '__main__':
    main()
