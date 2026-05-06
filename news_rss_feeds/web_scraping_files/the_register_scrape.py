import requests
from bs4 import BeautifulSoup

# This is specifically for the register
def get_article_text_theregister(html):
    html_parser = BeautifulSoup(html, "html.parser")
 
    article_text = html_parser.find("div", class_="article_wrap")

    for style_tag in article_text.find_all("noscript"):
        style_tag.decompose() 
    for style_tag in article_text.find_all("img"):
        style_tag.decompose() 
    for style_tag in article_text.find_all("ul", class_="listinks"):
        style_tag.decompose() 
    
    removed_classes = ["left_col", "article_body_btm", "right_col", "comments", "similar_topics", "child_topics", "parent_topics", "more_topics"]
    for class_name in removed_classes:
        for style_tag in article_text.find_all("div", class_=class_name):
            style_tag.decompose() 

    # print(article_text)
    return article_text.get_text(separator="\n", strip=True).lower()