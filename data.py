from bs4 import BeautifulSoup
import requests


class Scraping:
    def __init__(self):
        self.url = ''
        self.links = []
        self.links_dict = {}

    def check_if_is_blogger(self):
        self.url = input("Enter url to take posts:   ")
        page = requests.get(self.url.strip())
        soup = BeautifulSoup(page.text, 'lxml')

        if soup.html.has_attr("xmlns"):
            self.request_sitemap()
            print(self.links_dict)
        else:
            print("You are not searching for a blog.")

    # finds all tags in sitemaps that contain links of posts
    def request_sitemap(self):
        site = "sitemap.xml"
        page = requests.get(self.url.strip() + site.strip())
        soup = BeautifulSoup(page.text, 'lxml')
        post_list = soup.find_all("loc")
        self.fill_list(post_list)
        self.request_links()

    # takes links of posts from sitemap and append them to list
    def fill_list(self, post_list):
        for classes in post_list:
            page2 = classes.text
            self.links.append(page2)

    def request_links(self):
        for links in self.links:
            page = requests.get(links)
            soup = BeautifulSoup(page.text, 'lxml')
            h1_el = soup.body.h1.text
            self.post_content_to_dict(h1_el, links, soup)

    # takes text of posts and add it to dict
    def post_content_to_dict(self, h1_el, links, soup):
        post_content = soup.find_all(class_="post-body-inner")
        for content in post_content:
            contents = content.text.encode('utf-8')
            self.get_dict_posts(h1_el, links, contents)

    # generate dictionary of links and posts's title and content
    def get_dict_posts(self, h1_el, links, contents):
        self.links_dict.update(
            {
                links: {
                    h1_el: contents
                }
            })