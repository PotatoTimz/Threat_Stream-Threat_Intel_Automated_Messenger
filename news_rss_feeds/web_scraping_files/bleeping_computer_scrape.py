import requests
from bs4 import BeautifulSoup

# This is specifically for bleeping computer
def get_article_text_bleeping(html):
    html_parser = BeautifulSoup(html, "html.parser")

    article_text = html_parser.find("div", class_="article_section")

    for style_tag in article_text.find_all("style"):
        style_tag.decompose() 
    for style_tag in article_text.find_all("div", class_="fs-iai"):
        style_tag.decompose() 
    for style_tag in article_text.find_all("div", class_="ia_rig"):
        style_tag.decompose() 
    for style_tag in article_text.find_all("div", class_="cz-related-article-wrapp"):
        style_tag.decompose() 
    for style_tag in article_text.find_all("div", class_="cz-news-story-title-section"):
        style_tag.decompose() 

    # print_with_indent(article_text)

    return article_text.get_text(separator="\n", strip=True).lower()