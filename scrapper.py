import re
import json
import cv2

from requests import get
from bs4 import BeautifulSoup as soup
from concurrent.futures import ThreadPoolExecutor

from pydotmap import DotMap


class PinterestImageScraper:
    def __init__(self):
        self.json_data_list = []
        self.unique_img = []
        
    @staticmethod
    def get_pinterest_links(body, max_images):
        searched_urls = []
        html = soup(body, 'html.parser')
        links = html.select('#main > div > div > div > a')
        for link in links:
            link = link.get('href')
            link = re.sub(r'/url\?q=', '', link)
            if link[0] != "/" and "pinterest" in link:
                searched_urls.append(link)
                #stops adding links if the limit has been reached
                if max_images is not None and max_images == len(searched_urls):
                    break

        return searched_urls 
    
    def get_source(self, url, proxies):
        try:
            res = get(url, proxies=proxies)
        except Exception as e:
            return
        html = soup(res.text, 'html.parser')
        json_data = html.find_all("script", attrs={"id": "__PWS_DATA__"})
        for a in json_data:
            self.json_data_list.append(a.string)

    def save_image_url(self, max_images):
        url_list = [i for i in self.json_data_list if i.strip()]
        if not len(url_list):
            return url_list
        url_list = []
        for js in self.json_data_list:
            try:
                data = DotMap(json.loads(js))
                urls = []
                for pin in data.props.initialReduxState.pins:
                    if isinstance(data.props.initialReduxState.pins[pin].images.get("orig"), list):
                        for i in data.props.initialReduxState.pins[pin].images.get("orig"):
                            urls.append(i.get("url"))
                    else:
                        urls.append(data.props.initialReduxState.pins[pin].images.get("orig").get("url"))

                for url in urls:
                    url_list.append(url)

                    #if the maximum has been achieved, return early
                    if max_images is not None and max_images == len(url_list):
                        return list(set(url_list))
                    

            except Exception as e:
                continue
        
        return list(set(url_list))

    # ------------------------------ image hash calculation -------------------------
    def dhash(self, image, hashSize=8):
        resized = cv2.resize(image, (hashSize + 1, hashSize))
        diff = resized[:, 1:] > resized[:, :-1]
        return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])

    # -------------------------- get user keyword and google search for that keywords ---------------------
    @staticmethod
    def start_scraping(max_images, key=None, proxies={}):
        assert key != None, "Please provide keyword for searching images"
        keyword = key + " pinterest"
        keyword = keyword.replace("+", "%20")
        url = f'http://www.google.co.in/search?hl=en&q={keyword}'
        res = get(url, proxies=proxies)
        searched_urls = PinterestImageScraper.get_pinterest_links(res.content,max_images)

        return searched_urls, key.replace(" ", "_")


    def scrape(self, key=None, output_folder="", proxies={}, threads=10, max_images: int = None):
        extracted_urls, keyword = PinterestImageScraper.start_scraping(max_images,key, proxies)
        return_data = {}
        self.unique_img = []
        self.json_data_list = []

        for i in extracted_urls:
            self.get_source(i, proxies)

        # get all urls of images and save in a list
        url_list = self.save_image_url(max_images)

        return_data = {
            "isDownloaded": False,
            "url_list": url_list,
            "extracted_urls": extracted_urls,
            "keyword": key
        }
        return return_data
