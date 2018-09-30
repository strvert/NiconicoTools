import requests
from bs4 import BeautifulSoup


class MyLists:

    def __init__(self, url, base_url='http://www.nicovideo.jp'):
        self.url = url
        self.base_url = base_url
        self.html = self.get_html()
        self.soup = BeautifulSoup(self.html, 'html5lib')
        self.mylist_tags = self.get_mylist_html_tags()

        self.mylist_titles = self.get_mylist_titles(self.mylist_tags)
        self.mylist_urls = self.get_mylist_urls(self.mylist_tags)

    def get_html(self):
        try:
            text = requests.get(self.url).text
            return text

        except requests.exceptions.ConnectionError:
            print('ページへ接続できませんでした。')
            return ''

    def get_mylist_html_tags(self):
        return self.soup.select('#mylist > div > div > div.section.full > h4 > a')

    def get_mylist_titles(self, mylist_tags):
        video_titles = []
        for tag in mylist_tags:
            video_titles.append(tag.get_text())
        return video_titles

    def get_mylist_urls(self, mylist_tags):
        video_urls = []
        for tag in mylist_tags:
            video_urls.append('{0}/{1}'.format(self.base_url, tag.attrs['href']))
        return video_urls

    def get_videos(self):
        return dict(zip(self.get_mylist_titles(self.mylist_tags), self.get_mylist_urls(self.mylist_tags)))


def main():
    my_lists = MyLists('http://www.nicovideo.jp/user/21514289/mylist')
    print(my_lists.get_videos())


if __name__ == "__main__":
    main()
