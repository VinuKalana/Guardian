import re
import whois
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def extract_features(url,label):
    features = {}

    #listing shortening services
    shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                      r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                      r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                      r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                      r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                      r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                      r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                      r"tr\.im|link\.zip\.net"


    # Address Bar Based Features (9)
    parsed_url = urlparse(url)
    # Domain of the URL (Domain)
    domain = parsed_url.netloc
    features['Domain'] = domain
    # Checks for IP address in URL (IP_address)
    features['IP Address'] = int(bool(re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url)))
    # Checks the presence of @ in URL
    features['@ Symbol'] = int('@' in domain)
    # Finding the length of URL and categorizing (URL_Length)
    features['URL Length'] = 0 if len(url) <= 62 else 1
    # Gives number of '/' in URL (URL_Depth)
    features['URL Depth'] = url.count('/')
    # Checking for redirection '//' in the url (Redirection)
    features['Redirection'] = int('//' in domain)
    # Existence of “HTTPS” Token in the Domain Part of the URL (https_Domain)
    features['HTTP/HTTPS in Domain'] = int('http' in domain or 'https' in domain)
    # Checking for Shortening Services in URL (Tiny_URL)
    features['Shortening Service'] = int(bool(re.search(shortening_services, domain)))
    # Checking for Prefix or Suffix Separated by (-) in the Domain (Prefix/Suffix)
    features['Prefix/Suffix - in Domain'] = int('-' in domain)

    # Domain Based Features (4)
    try:
        w = whois.whois(domain)
        # Check for DNS record
        features['DNS Record'] = int(not bool(w.domain_name))
        # Check Web traffic with Alexa (Web_Traffic)
        url = f"https://www.alexa.com/siteinfo/{domain}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        rank_element = soup.select_one(".rank-global")
        rank = rank_element.get_text(strip=True) if rank_element else ''
        if rank == '' or int(rank) > 100000:
            features['Web Traffic'] = 1
        else:
            features['Web Traffic'] = 0
        # Checking for Domain age
        if isinstance(w.creation_date, list) and isinstance(w.updated_date, list):
            domain_age = (w.expiration_date[0] - w.creation_date[0]).days
        else:
            domain_age = 1
        features['Domain Age'] = 0 if domain_age and domain_age >= 365 else 1
        # End time of domain: The difference between termination time and current time (Domain_End)
        if isinstance(w.expiration_date, list) and isinstance(w.updated_date, list):
            end_period = (w.expiration_date[0] - w.updated_date[0]).days
        else:
            end_period = 1
        features['End Period of Domain'] = 0 if end_period and end_period <= 183 else 1
    except:
        features['DNS Record'] = 1
        features['Web Traffic'] = 1
        features['Domain Age'] = 1
        features['End Period of Domain'] = 1

    # HTML and JavaScript based Features
    try:
        response = requests.get(url)
        html = response.text
        # IFrame Redirection (iFrame)
        iframe_found = bool(re.findall(r'<iframe|<frame', html, re.IGNORECASE))
        respond_found = bool(re.findall(r'respond', html, re.IGNORECASE))
        features['IFrame Redirection'] = 1 if not iframe_found or respond_found else 0
        # Checks the effect of mouse over on status bar (Mouse_Over)
        if not html or re.search(r'onmouseover', html, re.IGNORECASE): 
            features['Status Bar Customization'] = 1 
        else: 
            features['Status Bar Customization'] = 0
        # Checks the status of the right click attribute (Right_Click)
        features['Disabling Right Click'] = int(bool(re.search(r'event\.button\s*==\s*2', html, re.IGNORECASE)))
        # Checks the number of forwardings (Web_Forwards)
        forwarding_tags = re.findall(r'<meta\s*http-equiv\s*=\s*["\']?refresh', html, re.IGNORECASE)
        features['Website Forwarding'] = int(len(forwarding_tags) > 1)
    except:
        features['IFrame Redirection'] = 1
        features['Status Bar Customization'] = 1
        features['Disabling Right Click'] = 1
        features['Website Forwarding'] = 1

    # use in feature extraction in ipynb
    # features['Label']=label
    return features
