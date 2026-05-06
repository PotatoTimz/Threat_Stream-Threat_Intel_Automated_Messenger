import requests
from bs4 import BeautifulSoup

# This is specifically for techcrunch
def get_article_text_techcruch(html):
    html_parser = BeautifulSoup(html, "html.parser")
 
    article_text = html_parser.find("div", class_="wp-block-post-content")
   
    # print(article_text)
    return article_text.get_text(separator="\n", strip=True).lower()