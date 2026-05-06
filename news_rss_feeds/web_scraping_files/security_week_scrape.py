import requests
from bs4 import BeautifulSoup

# This is for security week
def get_article_text_securityweek(html):
    html_parser = BeautifulSoup(html, "html.parser")
 
    article_text = html_parser.find("div", class_="zox-post-body-wrap")
 
    for style_tag in article_text.find_all("style"):
        style_tag.decompose()
    for strong in article_text.find_all("strong"):
        if "Related:" in strong.get_text():
            # Remove <strong> and its next sibling <a>
            next_sib = strong.find_next_sibling("a")
            if next_sib:
                next_sib.decompose()
            strong.decompose()  # remove the <strong> itself
    for style_tag in article_text.find_all("div", class_="zox-post-body-bot"):
        style_tag.decompose()
    for style_tag in article_text.find_all("div", class_="zox-post-ad-wrap"):
        style_tag.decompose()
 
    # print(article_text)
    return article_text.get_text(separator="\n", strip=True).lower()