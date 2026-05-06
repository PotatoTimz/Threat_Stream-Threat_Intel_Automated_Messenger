import requests
from bs4 import BeautifulSoup

# This is specifically for dark reading
def get_article_text_darkreading(html):
    html_parser = BeautifulSoup(html, "html.parser")
 
    article_text = html_parser.find("div", class_="ArticleBase-BodyContent")
 
    for style_tag in article_text.find_all("style"):
        style_tag.decompose()
    for style_tag in article_text.find_all("p", class_="RelatedArticle"):
        style_tag.decompose()
   
    # print(article_text)
    return article_text.get_text(separator="\n", strip=True).lower()