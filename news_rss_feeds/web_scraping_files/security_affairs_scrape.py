import requests
from bs4 import BeautifulSoup

# This is specifically for security affairs
def get_article_text_securityaffairs(html):
    html_parser = BeautifulSoup(html, "html.parser")
    
    article_text = html_parser.find("div", class_="category-section")

    for style_tag in article_text.find_all("style"):
        style_tag.decompose() 
    for style_tag in article_text.find_all("img"):
        style_tag.decompose() 
    for style_tag in article_text.find_all("div", class_="social-media"):
        style_tag.decompose() 
    for style_tag in article_text.find_all("div", class_="cta-tags"):
        style_tag.decompose() 
    for style_tag in article_text.find_all("div", class_="recommended-post"):
        style_tag.decompose() 
    for style_tag in article_text.find_all("div", class_="right-sidebar"):
        style_tag.decompose() 
    for style_tag in article_text.find_all("div", class_="post-time"):
        style_tag.decompose() 
        
    # print(article_text)
    return article_text.get_text(separator="\n", strip=True).lower()