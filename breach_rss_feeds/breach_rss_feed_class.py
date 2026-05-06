import feedparser, ssl, urllib3
from datetime import datetime as dt
from misc.helpers import replace_string_date
from zoneinfo import ZoneInfo
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class breach_rss_feed:
    def __init__(self, feed_link, source_name, data_extraction_function):
        self.feed_link = feed_link
        self.source_name = source_name
        self.data_extraction_function = data_extraction_function

    def __str__(self):
        return f"""
        Breach RSS Info:
        Sorce Name: {self.source_name}
        Feed Link: {self.feed_link}
        """

    def article_has_been_seen(self, last_scan_date, published_date):
        est = ZoneInfo("EST")
    
        # Converts the published time into something usable for comparisons"
        published_date = replace_string_date(published_date)
        published_date = dt.strptime(published_date, "%a, %d %b %Y %H:%M:%S %z")
        published_date = published_date.astimezone(est)
        published_date = published_date.strftime("%Y-%m-%d %H:%M:%S")
        published_date = dt.strptime(published_date, "%Y-%m-%d %H:%M:%S")

        return published_date > last_scan_date, published_date

    def poll_feed(self, last_scan_date):
        ssl._create_default_https_context = ssl._create_unverified_context
        feed = feedparser.parse(self.feed_link)
        articles = []
        for f in feed["entries"]:
            try:
                is_new, published_date = self.article_has_been_seen(last_scan_date, f["published"]) 
                if not is_new:
                    break
                breach_data = self.data_extraction_function(f, published_date, self.source_name)
                articles.append(breach_data)
            except:
                continue
        
        return articles