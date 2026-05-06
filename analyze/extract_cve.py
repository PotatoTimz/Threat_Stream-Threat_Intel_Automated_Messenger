import requests
from bs4 import BeautifulSoup
from misc.helpers import cve_list_update
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

FILENAME = "./txt_files/cves_list.txt"

def extract_cve_from_article(url, summary):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/140.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.google.com/"
    }

    try:
        res=  requests.get(url, headers=headers, verify=False)
        article_html = BeautifulSoup(res.text, "html.parser")

        cve_pattern = r'CVE-\d{4}-\d{4,7}'
        cves_found_article = re.findall(cve_pattern, str(article_html))
        cves_found_summary = re.findall(cve_pattern, summary)
        cves_found = set(cves_found_article + cves_found_summary)

        if not cves_found:
            return "There were no CVEs associated to this article"
        
        cve_list_update(FILENAME, cves_found)
        
        return list(cves_found)
    except:
        return "There was an issue extracting the CVEs from the article"