# hookphish functions

import re
from pprint import pprint
import requests
from bs4 import BeautifulSoup

COUNTRY2_TO_COUNTRYWHOLE = {
    "AF": "Afghanistan",
    "AL": "Albania",
    "DZ": "Algeria",
    "AR": "Argentina",
    "AU": "Australia",
    "AT": "Austria",
    "BD": "Bangladesh",
    "BE": "Belgium",
    "BR": "Brazil",
    "BG": "Bulgaria",
    "CA": "Canada",
    "CL": "Chile",
    "CN": "China",
    "CO": "Colombia",
    "CR": "Costa Rica",
    "HR": "Croatia",
    "CZ": "Czech Republic",
    "DK": "Denmark",
    "EG": "Egypt",
    "FI": "Finland",
    "FR": "France",
    "DE": "Germany",
    "GR": "Greece",
    "HK": "Hong Kong",
    "HU": "Hungary",
    "IN": "India",
    "ID": "Indonesia",
    "IE": "Ireland",
    "IL": "Israel",
    "IT": "Italy",
    "JP": "Japan",
    "KE": "Kenya",
    "LU": "Luxembourg",
    "MY": "Malaysia",
    "MX": "Mexico",
    "NL": "Netherlands",
    "NZ": "New Zealand",
    "NG": "Nigeria",
    "NO": "Norway",
    "PK": "Pakistan",
    "PH": "Philippines",
    "PL": "Poland",
    "PT": "Portugal",
    "RO": "Romania",
    "RU": "Russia",
    "SA": "Saudi Arabia",
    "SG": "Singapore",
    "ZA": "South Africa",
    "KR": "South Korea",
    "ES": "Spain",
    "SE": "Sweden",
    "CH": "Switzerland",
    "TW": "Taiwan",
    "TH": "Thailand",
    "TR": "Turkey",
    "UA": "Ukraine",
    "AE": "United Arab Emirates",
    "GB": "United Kingdom",
    "US": "United States",
    "VN": "Vietnam"
}

# Extract the attacker and victim through regex from article title
def extract_attacker_victim(title: str):
    pattern = r"Ransomware Group\s+(?P<attacker>.*?)\s+Hits:\s+(?P<victim>.*)"
    match = re.search(pattern, title, re.IGNORECASE)

    if match:
        return {
            "attacker": match.group("attacker").strip(),
            "victim": match.group("victim").strip()
        }
    return None

# Extracts and analyzes summary, date of breach, date of discovery and country through webscraping
def analyze_article_text(article_link):
    
    # Get HTML from the article
    html_content = requests.get(article_link, verify=False)
    html_content = html_content.text
    html_parser = BeautifulSoup(html_content, "html.parser")

    # Extract the first paragraph (summary) from the article
    for p in html_parser.find_all("p"):
        p = p.get_text(" ", strip=True)
        # Used to determine which paragraph to grab
        if p.startswith("In the latest cybersecurity news"):
            summary_p = p
            break

    # Extracts country from the summary via regex
    pattern = r"operating\s+in\s+the\s+(?P<country>[^—]+)"
    match = re.search(pattern, summary_p, re.IGNORECASE)
    country = match.group("country").strip()

    # Extract Data Table from the article 
    # Data Table Array Info
    # 0:MISC, 1:Target Organization, 2:Target Group, 3:Summary, 4:Date of Breach, 5:Discovery Date, 6:Region, 7:Target Domaim. 8:Business Sector
    table = html_parser.find("table")
    rows = table.find_all("tr")
    table_data = []
    for row in rows:
        cells = row.find_all(["td", "th"])
        table_data.append(str(cells[1].get_text().replace("\n", "")))

    # Returns list of extracted data
    return {
        "summary" : summary_p,
        "date_of_breach" : table_data[4] if table_data[4] != None else "Not Provided",
        "discovery_date": table_data[5] if table_data[5] != None else "Not Provided",
        "country" : COUNTRY2_TO_COUNTRYWHOLE.get(country, country)
    }

def extract_hookphish_data(rss_data, published_date, source_name):
    breach_data = {}

    # Get Attacker and Breached Company data from data["title"]
    attacker_victim_data = extract_attacker_victim(rss_data["title"])
    breach_data["attacker"] = attacker_victim_data["attacker"]
    breach_data["victim"] = attacker_victim_data["victim"]

    # Get article publish date
    breach_data["date"] = str(published_date)

    # Get artucke link and source
    breach_data["link"] = rss_data["link"]
    breach_data["source"] = source_name

    # Get date_of_breach, discovery_date, summary, country via webscraping
    breach_data.update(analyze_article_text(rss_data["link"]))
    
    # Return hashmap of all data
    return breach_data