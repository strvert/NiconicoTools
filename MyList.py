import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


class MyList:

    def __init__(self, url, base_url='http://http://www.nicovideo.jp'):
        options = Options()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=options)

        self.url = url
        self.base_url = base_url
        self.html = self.get_html()
        self.soup = BeautifulSoup(self.html, 'html5lib')
        self.page_count = self.get_page_count()
        self.current_page = self.get_current_page()
        self.video_tags = self.get_video_html_tags()
        self.video_titles = self.get_video_titles(self.video_tags)
        self.video_urls = self.get_video_urls(self.video_tags)

    def get_html(self):
        try:
            self.driver.get(self.url)
            time.sleep(1)
            html = self.driver.page_source
            return html

        except requests.exceptions.ConnectionError:
            print('ページへ接続できませんでした。')
            return ''

    def get_page_count(self):
        temp_tag = self.soup.find(id='SYS_box_mylist_body').table.tbody.tr.find('form', class_='SYS_box_pager')
        temp_tag = temp_tag.table.tbody.tr.td
        count = len(temp_tag.find_all('span')) + len(temp_tag.find_all('a', class_='SYS_btn_pager'))
        return count

    def get_current_page(self):
        temp_tag = self.soup.find(id='SYS_box_mylist_body').table.tbody.tr.find('form', class_='SYS_box_pager')
        temp_tag = temp_tag.table.tbody.tr.td
        page = temp_tag.find('span').get_text()
        return int(page)

    def get_video_html_tags(self):
        return self.soup.select('#SYS_page_items > div > table > tbody > tr > td.SYS_box_item_data > p.font16 > a')

    def get_video_titles(self, tags):
        video_titles = []
        for tag in tags:
            video_titles.append(str(tag.get_text()).translate(str.maketrans({' ': '_', '　': '_'})))
        return video_titles

    def get_video_urls(self, tags):
        video_urls = []
        for tag in tags:
            video_urls.append('{0}/{1}'.format(self.base_url, tag.attrs['href']))
        return video_urls

    def get_videos(self):
        return dict(zip(self.get_video_titles(self.video_tags), self.get_video_urls(self.video_tags)))


def main():
    my_list = MyList('http://www.nicovideo.jp/mylist/60628711#+page=3')
    print(my_list.get_videos())
    print(my_list.page_count)
    print(my_list.current_page)


if __name__ == "__main__":
    main()