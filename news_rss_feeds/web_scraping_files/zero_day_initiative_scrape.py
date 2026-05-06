import requests
from bs4 import BeautifulSoup

# This is specifically for dark reading
def get_article_text_zdi(html):
    html_parser = BeautifulSoup(html, "html.parser")
 
    article_text = html_parser.find("div", class_="section")

    for style_tag in article_text.find_all("style"):
        style_tag.decompose() 
    for style_tag in article_text.find_all("img"):
        style_tag.decompose() 
    for style_tag in article_text.find_all("button"):
        style_tag.decompose() 
    for tag in article_text.select("[style]"):
        del tag["style"]

    # The only articles that we want on this website are research blogs
    ul = article_text.find("ul", class_="blog-tags")
    is_research = any(a.get_text(strip=True) == "Research" for a in ul.find_all("a"))
    if not is_research:
        return ""
    
    # print(article_text)
    return article_text.get_text(separator="\n", strip=True).lower()