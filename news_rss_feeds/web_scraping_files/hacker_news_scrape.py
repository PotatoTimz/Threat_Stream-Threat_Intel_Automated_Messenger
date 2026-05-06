import requests
from bs4 import BeautifulSoup

# This is specifically for hacker news
def get_article_text_hackernews(html):
    html_parser = BeautifulSoup(html, "html.parser")
 
    article_text = html_parser.find("div", class_="main-box")
 
    div_classes_delete = ["postmeta", "separator", "pop-article", "note-b", "float-share", "sharebelow", "rightbx", "mobile-share", "tags"]
 
    for style_tag in article_text.find_all("style"):
        style_tag.decompose()
    for style_tag in article_text.find_all("script"):
        style_tag.decompose()
    for class_name in div_classes_delete:
        for style_tag in article_text.find_all("div", class_=class_name):
            style_tag.decompose()
    for style_tag in article_text.find_all("table", class_="tr-caption-container"):
        style_tag.decompose()
   
    # print(article_text)

    return article_text.get_text(separator="\n", strip=True).lower()