import re
from datetime import datetime as dt

def check_valid_domain(domain):
    print(domain)
    regex = r"^(https?:\/\/)?([\da-z\.-]+)\.([a-z]{2,})(\/[\w\.-]*)*\/?$"
    match = re.fullmatch(regex, domain)
    if match:
        return True
    else:
        return False

# Gets time
def extract_txt(filename):
    last_poll = ""
    with open(filename, "r") as f:
        for line in f:
            last_poll = line.strip()
    return last_poll

# Updates time 
def update_txt(filename, last_poll):
    with open(filename, "w") as f:
        print("Updating Time To: ", last_poll)
        f.write(last_poll)

# Gets filter list from text file
def fetch_filter_list(filename):
    filter_list = set()
    with open(filename, "r") as f:
        for line in f:
            filter_list.add(line.strip())
    return filter_list

# Check string formatted date and converts to datetime type variable
def parse_date(date_str):
    formats = [
        "%a, %d %b %Y %H:%M:%S %z",   
        "%Y-%m-%dT%H:%M:%S.%fZ",      
        "%Y-%m-%dT%H:%M:%SZ",         
    ]

    # Loops through multiple formats to see which one is correct. Invalid formats...
    for fmt in formats:
        try:
            return dt.strptime(date_str, fmt)
        except ValueError:
            continue
    
    # If correct format has not been listed then raise error and end task
    raise ValueError(f"Unknown date format: {date_str}")

# Adds newly found cves to list
def cve_list_update(filename, new_cves):
    cve_list = set()
    
    with open(filename, "r") as f:
        for line in f:
            cve_list.add(line.strip())
    
    for cve in new_cves:
        if cve not in cve_list:
            print("Adding CVE", cve, "to list...")
            cve_list.add(cve)

    with open(filename, "w") as f:
        for cve in cve_list:
            f.write(cve + "\n")
    
        f.close()
        
# Text Cleaners
def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def remove_summary_cut_off(text):
    clean = re.compile(r'\[&#8230;\]')
    return re.sub(clean, '...', text)

# Date Cleaner
def replace_string_date(date):
    # Replaces GMT Time
    date = date.replace("GMT", "+0000")
    
    return date

US_STATES_SET = {
    "alabama", "alaska", "arizona", "arkansas", "california",
    "colorado", "connecticut", "delaware", "florida", "georgia",
    "hawaii", "idaho", "illinois", "indiana", "iowa",
    "kansas", "kentucky", "louisiana", "maine", "maryland",
    "massachusetts", "michigan", "minnesota", "mississippi", "missouri",
    "montana", "nebraska", "nevada", "new hampshire", "new jersey",
    "new mexico", "new york", "north carolina", "north dakota", "ohio",
    "oklahoma", "oregon", "pennsylvania", "rhode island", "south carolina",
    "south dakota", "tennessee", "texas", "utah", "vermont",
    "virginia", "washington", "west virginia", "wisconsin", "wyoming"
}

CANADA_PROVINCES_TERRITORIES_SET = {
    "alberta",
    "british columbia",
    "manitoba",
    "new brunswick",
    "newfoundland and labrador",
    "nova scotia",
    "ontario",
    "prince edward island",
    "quebec",
    "saskatchewan",
    "northwest territories",
    "nunavut",
    "yukon"
}

ALL_COUNTRY_SET = {
    "afghanistan", "albania", "algeria", "andorra", "angola",
    "antigua and barbuda", "argentina", "armenia", "australia", "austria",
    "azerbaijan", "bahamas", "bahrain", "bangladesh", "barbados",
    "belarus", "belgium", "belize", "benin", "bhutan",
    "bolivia", "bosnia and herzegovina", "botswana", "brazil", "brunei",
    "bulgaria", "burkina faso", "burundi", "cabo verde", "cambodia",
    "cameroon", "canada", "central african republic", "chad", "chile",
    "china", "colombia", "comoros", "congo", "costa rica",
    "côte d’ivoire", "croatia", "cuba", "cyprus", "czech republic",
    "denmark", "djibouti", "dominica", "dominican republic", "ecuador",
    "egypt", "el salvador", "equatorial guinea", "eritrea", "estonia",
    "eswatini", "ethiopia", "fiji", "finland", "france",
    "gabon", "gambia", "georgia", "germany", "ghana",
    "greece", "grenada", "guatemala", "guinea", "guinea-bissau",
    "guyana", "haiti", "honduras", "hungary", "iceland",
    "india", "indonesia", "iran", "iraq", "ireland",
    "israel", "italy", "jamaica", "japan", "jordan",
    "kazakhstan", "kenya", "kiribati", "kuwait", "kyrgyzstan",
    "laos", "latvia", "lebanon", "lesotho", "liberia",
    "libya", "liechtenstein", "lithuania", "luxembourg", "madagascar",
    "malawi", "malaysia", "maldives", "mali", "malta",
    "marshall islands", "mauritania", "mauritius", "mexico", "micronesia",
    "moldova", "monaco", "mongolia", "montenegro", "morocco",
    "mozambique", "myanmar", "namibia", "nauru", "nepal",
    "netherlands", "new zealand", "nicaragua", "niger", "nigeria",
    "north korea", "north macedonia", "norway", "oman", "pakistan",
    "palau", "panama", "papua new guinea", "paraguay", "peru",
    "philippines", "poland", "portugal", "qatar", "romania",
    "russia", "rwanda", "saint kitts and nevis", "saint lucia",
    "saint vincent and the grenadines", "samoa", "san marino",
    "sao tome and principe", "saudi arabia", "senegal", "serbia",
    "seychelles", "sierra leone", "singapore", "slovakia", "slovenia",
    "solomon islands", "somalia", "south africa", "south sudan", "spain",
    "sri lanka", "sudan", "suriname", "sweden", "switzerland",
    "syria", "tajikistan", "tanzania", "thailand", "timor-leste",
    "togo", "tonga", "trinidad and tobago", "tunisia", "turkey",
    "turkmenistan", "tuvalu", "uganda", "ukraine",
    "united arab emirates", "united kingdom", "united states",
    "uruguay", "uzbekistan", "vanuatu", "vatican city",
    "venezuela", "vietnam", "yemen", "zambia", "zimbabwe"
},