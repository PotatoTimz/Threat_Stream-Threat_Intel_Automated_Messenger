from news_rss_feeds.news_rss_feed_class import rss_feed
from misc.response_formats import create_teams_article_notifcation, create_article_postcards
from datetime import datetime as dt
from misc.helpers import extract_txt, update_txt, fetch_filter_list
import hashlib
import ssl

from news_rss_feeds.web_scraping_files.bleeping_computer_scrape import get_article_text_bleeping
from news_rss_feeds.web_scraping_files.hacker_news_scrape import get_article_text_hackernews
from news_rss_feeds.web_scraping_files.security_week_scrape import get_article_text_securityweek
from news_rss_feeds.web_scraping_files.dark_reading_scrape import get_article_text_darkreading
from news_rss_feeds.web_scraping_files.the_register_scrape import get_article_text_theregister
from news_rss_feeds.web_scraping_files.tech_crunch_scrape import get_article_text_techcruch 
from news_rss_feeds.web_scraping_files.security_affairs_scrape import get_article_text_securityaffairs
from news_rss_feeds.web_scraping_files.zero_day_initiative_scrape import get_article_text_zdi


ssl._create_default_https_context = ssl._create_unverified_context

# Paths to Filter List + Last Scan Date
LAST_SCAN_FILEPATH = "./txt_files/last_poll.txt"
FILTER_LIST_FILEPATH = "./txt_files/filter_list.txt"

# Populate postcard template based on gathered article information
def create_notifications(news_articles):
    article_notifications = []
    for article_data in news_articles:
        article_notification = create_article_postcards(article_data)
        article_notifications.append(article_notification)
    
    return article_notifications

# Go through all defined feeds that need to be polled for article info -> returns a list of all postcard text
def poll_news_feeds():
    new_article_notifications = []
    
    # Gather predefined Filter List & Scan Date
    last_scan_date = dt.strptime(extract_txt(LAST_SCAN_FILEPATH), "%Y-%m-%d %H:%M:%S")
    filter_list = fetch_filter_list(FILTER_LIST_FILEPATH)
    
    # List of objects that need to be polled
    feed_objects = []

    # Create Feed Classes for all of the applications -> (link, source, has_tags)
    #Bleeping Computer
    bleeping_computer_feed = rss_feed("https://www.bleepingcomputer.com/feed/", "Bleeping Computer", True, get_article_text_bleeping)
    feed_objects.append(bleeping_computer_feed)
    # Dark Reading 
    dark_reading_feed = rss_feed("https://www.darkreading.com/rss.xml", "Dark Reading", False, get_article_text_darkreading)
    feed_objects.append(dark_reading_feed) 
    # Hacker News
    hacker_news_feed = rss_feed("https://feeds.feedburner.com/TheHackersNews?format=xml", "Hacker News", False, get_article_text_hackernews)
    feed_objects.append(hacker_news_feed)
    # Security Week
    security_week_feed = rss_feed("https://www.securityweek.com/feed/", "Security Week", True, get_article_text_securityweek)
    feed_objects.append(security_week_feed)
    # The Register
    the_register_cybercrime_feed = rss_feed("https://www.theregister.com/security/cyber_crime/headlines.atom", "The Register", True, get_article_text_theregister)
    feed_objects.append(the_register_cybercrime_feed)
    the_register_research_feed = rss_feed("https://www.theregister.com/security/research/headlines.atom", "The Register", True, get_article_text_theregister)
    feed_objects.append(the_register_research_feed)
    the_register_patches_feed = rss_feed("https://www.theregister.com/security/patches/headlines.atom", "The Register", True, get_article_text_theregister)
    feed_objects.append(the_register_patches_feed)
    the_register_cso_feed = rss_feed("https://www.theregister.com/security/cso/headlines.atom", "The Register", True, get_article_text_theregister)
    feed_objects.append(the_register_cso_feed)
    # Tech Crunch
    tech_crunch_feed = rss_feed("https://techcrunch.com/category/security/feed/", "Tech Crunch", True, get_article_text_techcruch)
    feed_objects.append(tech_crunch_feed)
    # Security Affairs
    security_affairs_feed = rss_feed("https://securityaffairs.com/feed", "Security Affairs", True, get_article_text_securityaffairs)
    feed_objects.append(security_affairs_feed)
    # Zero Day Initiative 
    zdi_feed = rss_feed("https://www.thezdi.com/blog?format=rss", "Zero Day Initiative", True, get_article_text_zdi)
    feed_objects.append(zdi_feed)

    # Itterate through all objects to poll feed and generate postcard templates 
    for feed in feed_objects:
        # print(feed)
        news_articles = feed.poll_feed(last_scan_date, filter_list)
        new_article_notifications += create_notifications(news_articles)    
    
    return new_article_notifications