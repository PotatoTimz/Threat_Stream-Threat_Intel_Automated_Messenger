from bs4 import BeautifulSoup
import feedparser
from datetime import datetime as dt
from playwright.sync_api import sync_playwright
from analyze.extract_cve import extract_cve_from_article
from misc.helpers import remove_html_tags, remove_summary_cut_off, replace_string_date, parse_date
from zoneinfo import ZoneInfo
import urllib.parse
import re
import time

"""
A class for ingesting rss feed and filtering based on prerequsite list of items

Attributs:
----------
feed: link to the rss feed of the new soruce
source_name: name of source
has_tags | boolean : does rss feed include self defined tags
scraping_function | func : predefined scraping function (created every source /web_scraping_files)
"""
class rss_feed:
    
    def __init__(self, link, source, has_tags, scraping_function):
        # Source Information
        self.feed = link
        self.source_name = source
        self.has_tags = has_tags
        self.scraping_function = scraping_function
    
    def __str__(self):
        return f"""
              RSS Feed Info:
              Source Name: {self.source_name}
              Source Feed: {self.feed}
              Has Tags: {self.has_tags}
              """
    
    # Checks article publish date and compares to last scan date -> Returns boolean and Reformatted publish date
    def article_has_been_seen(self, last_scan_date, published_date):
        est = ZoneInfo("EST")
    
        # Reformats provided published time to python time format
        published_date = replace_string_date(published_date)
        published_date = parse_date(published_date)
        published_date = published_date.astimezone(est)
        published_date = published_date.strftime("%Y-%m-%d %H:%M:%S")
        published_date = dt.strptime(published_date, "%Y-%m-%d %H:%M:%S")

        # Compares previous scan time
        return published_date > last_scan_date, published_date
    
    def get_article_contents(self, url):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)

            context = browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/122.0.0.0 Safari/537.36"
                ),
                viewport={"width": 1920, "height": 1080},
                locale="en-US",
                timezone_id="America/Toronto"
            )

            def block_heavy(route):
                if route.request.resource_type in ["image", "font", "media"]:
                    route.abort()
                else:
                    route.continue_()

            context.route("**/*", block_heavy)

            page = context.new_page()

            page.goto(url, wait_until="domcontentloaded", timeout=60000)

            # give Cloudflare time to pass JS checks
            page.wait_for_timeout(5000)

            html = page.content()

            browser.close()

            return html

    # Extracts the image from found as metadata inside of the article
    def article_extract_image(self, html):
        html_parser = BeautifulSoup(html, "html.parser")
        img = html_parser.find("meta", property="og:image")
        if img:
            return img["content"]
        else:
            # returns Image Not Found picture
            return "https://upload.wikimedia.org/wikipedia/commons/a/a3/Image-not-found.png" 

    # Performs regex check for all key words inside of the article contents -> returns list of key words contained in the article
    def article_filter(self, article_link, filter_list):
        # Gets article HTML
        html = self.get_article_contents(article_link)

        # Gets article image link
        image = self.article_extract_image(html)

        # Scrape article text (omitts ads, headers, etc)
        article_text = self.scraping_function(html)

        found_words = set()

        # regex check
        for word in filter_list:
            if re.search(rf"\b{re.escape(word)}\b", article_text, re.IGNORECASE):
                found_words.add(word)

        # turn article text into chatgpt prompt
        encoded_article_text = urllib.parse.quote(article_text)
        chatgpt_link = f"https://chatgpt.com/g/g-69d8eaa6dc508191ac9c547d31308c27-threat-intel-explainer/?prompt={encoded_article_text}"

        return found_words, chatgpt_link, article_text, image

    # Polls RSS feed one article at a time and returns list of relevent articles with their information
    def poll_feed(self, last_scan_date, filter_list):
        # Extracts article XML file
        feed = feedparser.parse(self.feed)
        news_articles = []

        # print(len(feed["entries"]))
        # Loops through every article inside of the XML file
        for f in feed["entries"]:
            try:
                # Checks if current article is older then last poll date (entries are itterated in publish order)
                is_new, published_date = self.article_has_been_seen(last_scan_date, f["published"]) 
                # print(f["title"], is_new, self.source_name)
                if not is_new:
                    break # If article is older then last poll date then stop 

                # Loops through all flagged words to see if there has been any changes
                flagged_words, chatgpt_link, article_text, image = self.article_filter(f["link"], filter_list)
                if len(flagged_words) == 0:
                    continue
                
                # Summary cleaing (remove html tags, etc.)
                summary =  remove_summary_cut_off(remove_html_tags(f["summary"]))

                # Populate hashmap based on RSS feed info + web scraping
                news_articles.append(
                    {
                        "title": f["title"],
                        "date": str(published_date),
                        "link": f["link"],
                        "tags": [word for word in flagged_words],
                        "summary": summary if len(summary) <= 500 else "Summary was not provided...",
                        "source": self.source_name,
                        "cves": extract_cve_from_article(f["link"], f["summary"]),
                        "chatgpt_link": chatgpt_link,
                        "article_text": article_text,
                        "image": image
                    }
                )
                time.sleep(3)
            except Exception as e:
                print(e, f"SOURCE: {self.source_name}")
                continue
            
        return news_articles