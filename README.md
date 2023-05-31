# Guardian
Guardian: A Machine Learning-Based Anti-Phishing Browser Extension

## Objective
This project aims to train machine learning models and deep neural nets on a dataset created to predict phishing websites. Both phishing and benign URLs of websites are gathered to form a dataset and required URL and website content-based features are extracted. The performance level of each model is measured and compared.

## Research Problem
Anti-phishing browser extensions developed to detect and prevent phishing attacks, there is still a lack of understanding of their effectiveness in real-world scenarios. This poses a significant problem for individuals and organizations that rely on such technology to protect themselves from phishing attacks

## Research Objective
1.	Identify the types of phishing attacks that anti-phishing frameworks are most effective in detecting and preventing.
2.	Determine the factors that affect the effectiveness of anti-phishing frameworks in detecting and preventing phishing attacks.
3.	Evaluate the performance of anti-phishing browser frameworks in detecting and preventing different types of phishing attacks, such as email phishing, spear phishing, smishing, vishing, clone phishing, and whaling.
4.	Identify the strengths and weaknesses of existing anti-phishing browser frameworks and develop a effective browser extension,

## Methodology
This project is divide into 3 sprints
1. Data collection and Preprocessing
2. Training Machine Learning Model
3. Develop PoC that can utilize Trained ML model

### Sprint 01: Data Collection and Preprocessing

#### Feature Extraction:

In this step, features are extracted from the URLs dataset.

The extracted features are categorized into:
1. Address Bar based Features
2. Domain based Features
3. HTML & JavaScript based Features

##### Address Bar Based Features:

Many features can be extracted that can be consider as address bar base features. Out of them, below mentioned were considered for this project.

- Domain of URL:
- IP Address in URL: 
- "@" Symbol in URL:
- Length of URL: 
- Depth of URL: 
- Redirection "//" in URL:
- "http/https" in Domain name:
- Using URL Shortening Services “TinyURL”:
- Prefix or Suffix "-" in Domain: 

### 3.1.1. Domain of the URL

Here, we are just extracting the domain present in the URL. This feature doesn't have much significance in the training. May even be dropped while training the model.

```python
# Domain of the URL (Domain)
  parsed_url = urlparse(url)
  domain = parsed_url.netloc
  features['Domain'] = domain
```

### 3.1.2. IP Address in the URL

Checks for the presence of IP address in the URL. URLs may have IP address instead of domain name. If an IP address is used as an alternative of the domain name in the URL, we can be sure that someone is trying to steal personal information with this URL.

If the domain part of URL has IP address, the value assigned to this feature is 1 (phishing) or else 0 (legitimate).

```python
# Checks for IP address in URL (IP_address)
features['IP Address'] = int(bool(re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url)))
```

### 3.1.3. "@" Symbol in URL

Checks for the presence of '@' symbol in the URL. Using “@” symbol in the URL leads the browser to ignore everything preceding the “@” symbol and the real address often follows the “@” symbol.

If the URL has '@' symbol, the value assigned to this feature is 1 (phishing) or else 0 (legitimate).

```python
# Checks the presence of @ in URL
features['@ Symbol'] = int('@' in domain)
```

### 3.1.4. Length of URL

Computes the length of the URL. Phishers can use long URL to hide the doubtful part in the address bar. In this project, if the length of the URL is greater than or equal 62 characters then the URL classified as phishing otherwise legitimate.

If the length of URL >= 62 , the value assigned to this feature is 1 (phishing) or else 0 (legitimate).

```python
# Finding the length of URL and categorizing (URL_Length)
features['URL Length'] = 1 if len(url) >= 62 else 0
```

### 3.1.5. Depth of URL

Computes the depth of the URL. This feature calculates the number of sub pages in the given URL based on the '/'.
The value of feature is a numerical based on the URL.

```python
# Gives number of '/' in URL (URL_Depth)
features['URL Depth'] = url.count('/')
```

### 3.1.6. Redirection "//" in URL

Checks the presence of "//" in the URL. The existence of “//” within the URL path means that the user will be redirected to another website. The location of the “//” in URL is computed. We find that if the URL starts with “HTTP”, that means the “//” should appear in the sixth position. However, if the URL employs “HTTPS” then the “//” should appear in seventh position.

If the "//" is anywhere in the URL apart from after the protocol, thee value assigned to this feature is 1 (phishing) or else 0 (legitimate).

```python
# Checking for redirection '//' in the url (Redirection)
features['Redirection'] = int('//' in parsed_url.path)
```

### 3.1.7. "http/https" in Domain name

Checks for the presence of "http/https" in the domain part of the URL. The phishers may add the “HTTPS” token to the domain part of a URL in order to trick users.

If the URL has "http/https" in the domain part, the value assigned to this feature is 1 (phishing) or else 0 (legitimate).

```python
# Existence of “HTTPS” Token in the Domain Part of the URL (https_Domain)
features['HTTP/HTTPS in Domain'] = int('http' in domain or 'https' in domain)
```

### 3.1.8. Using URL Shortening Services “TinyURL”

URL shortening is a method on the “World Wide Web” in which a URL may be made considerably smaller in length and still lead to the required webpage. This is accomplished by means of an “HTTP Redirect” on a domain name that is short, which links to the webpage that has a long URL.

If the URL is using Shortening Services, the value assigned to this feature is 1 (phishing) or else 0 (legitimate).

```python
#listing shortening services
shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
r"tr\.im|link\.zip\.net"
```

```python
# Checking for Shortening Services in URL (Tiny_URL)
features['Shortening Service'] = int(bool(re.search(shortening_services, domain)))
```

### 3.1.9. Prefix or Suffix "-" in Domain

Checking the presence of '-' in the domain part of URL. The dash symbol is rarely used in legitimate URLs. Phishers tend to add prefixes or suffixes separated by (-) to the domain name so that users feel that they are dealing with a legitimate webpage.

If the URL has '-' symbol in the domain part of the URL, the value assigned to this feature is 1 (phishing) or else 0 (legitimate).

```python
# Checking for Prefix or Suffix Separated by (-) in the Domain (Prefix/Suffix)
features['Prefix/Suffix - in Domain'] = int('-' in domain)
```

## 3.2. Domain Based Features:

Many features can be extracted that come under this category. Out of them, below mentioned were considered for this project.

* DNS Record
* Website Traffic
* Age of Domain
* End Period of Domain

### 3.2.1. DNS Record

For phishing websites, either the claimed identity is not recognized by the WHOIS database or no records founded for the hostname. If the DNS record is empty or not found then, the value assigned to this feature is 1 (phishing) or else 0 (legitimate).

```python
# Check for DNS record
try:
    w = whois.whois(domain)
    features['DNS Record'] = int(not bool(w.domain_name))
except:
    features['DNS Record'] = 1
```

### 3.2.2. Web Traffic

This feature measures the popularity of the website by determining the number of visitors and the number of pages they visit. However, since phishing websites live for a short period of time, they may not be recognized by the Alexa database (Alexa the Web Information Company., 1996). By reviewing our dataset, we find that in worst scenarios, legitimate websites ranked among the top 100,000. Furthermore, if the domain has no traffic or is not recognized by the Alexa database, it is classified as “Phishing”.

If the rank of the domain > 100000 or no rank, the value of this feature is 1 (phishing) else 0 (legitimate).

```python
# Check Web traffic with Alexa (Web_Traffic)
try:
  url = f"https://www.alexa.com/siteinfo/{domain}"
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')
  rank_element = soup.select_one(".rank-global")
  rank = rank_element.get_text(strip=True) if rank_element else ''
  if rank == '' or int(rank) > 100000:
     features['Web Traffic'] = 1
  else:
     features['Web Traffic'] = 0
except:
  features['Web Traffic'] = 1
```

### 3.2.3. Age of Domain

This feature can be extracted from WHOIS database. Most phishing websites live for a short period of time. The minimum age of the legitimate domain is considered to be 12 months for this project. Age here is nothing but different between creation and expiration time.

If age of domain > 12 months, the value of this feature is 1 (phishing) else 0 (legitimate).

```python
# Checking for Domain age
try:
    w = whois.whois(domain)
    if isinstance(w.creation_date, list) and isinstance(w.updated_date, list):
      domain_age = (w.expiration_date[0] - w.creation_date[0]).days
    else:
      domain_age = 1
    features['Domain Age'] = 0 if domain_age and domain_age >= 365 else 1
except:
    features['Domain Age'] = 1
```

### 3.2.4. End Period of Domain

This feature can be extracted from WHOIS database. For this feature, the remaining domain time is calculated by finding the different between expiration time & current time. The end period considered for the legitimate domain is 6 months or less for this project.

If end period of domain > 6 months, the value of this feature is 1 (phishing) else 0 (legitimate).

```python
# End time of domain: The difference between termination time and current time (Domain_End)
try:
    w = whois.whois(domain)
    if isinstance(w.expiration_date, list) and isinstance(w.updated_date, list):
      end_period = (w.expiration_date[0] - w.updated_date[0]).days
    else:
      end_period = 1
    features['End Period of Domain'] = 0 if end_period and end_period <= 183 else 1
except:
    features['End Period of Domain'] = 1
```

## 3.3. HTML and JavaScript based Features

Many features can be extracted that come under this category. Out of them, below mentioned were considered for this project.
* IFrame Redirection
* Status Bar Customization
* Disabling Right Click
* Website Forwarding

### 3.3.1. IFrame Redirection

Iframe is an HTML tag used to display an additional webpage into one that is currently shown. Phishers can make use of the “iframe” tag and make it invisible i.e. without frame borders. In this regard, phishers make use of the “frameBorder” attribute which causes the browser to render a visual delineation.

If the iframe is empty or response is not found then, the value assigned to this feature is 1 (phishing) or else 0 (legitimate).

```python
# IFrame Redirection (iFrame)
try:
    response = requests.get(url)
    html = response.text
    iframe_found = bool(re.findall(r'<iframe|<frame', html, re.IGNORECASE))
    respond_found = bool(re.findall(r'respond', html, re.IGNORECASE))
    features['IFrame Redirection'] = 1 if not iframe_found or respond_found else 0
except:
    features['IFrame Redirection'] = 1
```

### 3.3.2. Status Bar Customization

Phishers may use JavaScript to show a fake URL in the status bar to users. To extract this feature, we must dig-out the webpage source code, particularly the “onMouseOver” event, and check if it makes any changes on the status bar

If the response is empty or onmouseover is found then, the value assigned to this feature is 1 (phishing) or else 0 (legitimate).

```python
# Checks the effect of mouse over on status bar (Mouse_Over)
try:
    response = requests.get(url)
    html = response.text
    if not html or re.search(r'onmouseover', html, re.IGNORECASE):
      features['Status Bar Customization'] = 1
    else:
      features['Status Bar Customization'] = 0
except:
    features['Status Bar Customization'] = 1
```

### 3.3.3. Disabling Right Click

Phishers use JavaScript to disable the right-click function, so that users cannot view and save the webpage source code. This feature is treated exactly as “Using onMouseOver to hide the Link”. Nonetheless, for this feature, we will search for event “event.button\==2” in the webpage source code and check if the right click is disabled.

```python
# Checks the status of the right click attribute (Right_Click)
try:
    response = requests.get(url)
    html = response.text
    features['Disabling Right Click'] = int(bool(re.search(r'event\.button\s*==\s*2', html, re.IGNORECASE)))
except:
    features['Disabling Right Click'] = 1
```

### 3.3.4. Website Forwarding

The fine line that distinguishes phishing websites from legitimate ones is how many times a website has been redirected. In our dataset, we find that legitimate websites have been redirected one time max. On the other hand, phishing websites containing this feature have been redirected at least 4 times.

```python
# Checks the number of forwardings (Web_Forwards)
try:
    response = requests.get(url)
    html = response.text  
    forwarding_tags = re.findall(r'<meta\s*http-equiv\s*=\s*["\']?refresh', html, re.IGNORECASE)
    features['Website Forwarding'] = int(len(forwarding_tags) > 1)
except:
    features['Website Forwarding'] = 1
```

### Sprint 02: Training Machine Learning Model

### Sprint 03: Develop PoC that can utilize Trained ML model





