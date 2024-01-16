from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup
from tinydb import TinyDB, Query
from datetime import datetime
import time
import json
from urllib3.exceptions import NameResolutionError
import hashlib
from tqdm import tqdm

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

db = TinyDB('ar_com_pelucadorada_data/website_content.json')
query = Query()

def load_json_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

websites_to_scrape = load_json_from_file('ar_com_pelucadorada_data/websites_to_scrape.json')
news_categories = load_json_from_file('ar_com_pelucadorada_data/keywords_categories.json')

def is_news_link(url, base_url):
    if not url.startswith('http'):
        return True
    base_domain = urlparse(base_url).netloc
    link_domain = urlparse(url).netloc
    return base_domain == link_domain

def determine_category(url, categories):
    url_lower = url.lower()
    for category in categories:
        if category in url_lower:
            return category
    return "home_page"

def extract_title(news_soup):
    return news_soup.title.string.strip() if news_soup.title else 'No Title'

def extract_body(news_soup):
    return news_soup.get_text().strip()

def fetch_news_content(news_url, delay_between_visits=0):
    time.sleep(delay_between_visits)
    response = requests.get(news_url, headers=headers)
    if response.status_code == 200 and 'text/html' in response.headers.get('Content-Type', ''):
        news_soup = BeautifulSoup(response.text, 'html.parser')
        title = extract_title(news_soup)
        body = extract_body(news_soup)
        unique_id = hashlib.md5(news_url.encode()).hexdigest()
        return {'id': unique_id, 'title': title, 'body': body, 'url': news_url}
    return None

def scrape_website(url):
    try:
        today_date = datetime.now().strftime('%d/%m/%Y')

        # Check if the website has already been scraped today
        if db.search((query.newspaper == url) & (query.date == today_date)):
            print(f"Website {url} has already been scraped today.")
            return

        response = requests.get(url, headers=headers)
        if response.status_code == 200 and 'text/html' in response.headers.get('Content-Type', ''):
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Collect all news links
            news_links = [(urljoin(url, tag['href']), determine_category(tag['href'], news_categories['es']))
                          for tag in soup.find_all(['a'], href=True) if is_news_link(urljoin(url, tag['href']), url)]

            # Initialize progress bar
            with tqdm(total=len(news_links), desc=f"Scraping {url}", unit='link') as pbar:
                category_dict = {}
                for link, category in news_links:
                    news_content = fetch_news_content(link)
                    if news_content:
                        if category not in category_dict:
                            category_dict[category] = []
                        category_dict[category].append(news_content)

                    # Update the progress bar
                    pbar.update(1)

            # Construct the newspaper record
            newspaper_record = {
                'date': today_date,
                'newspaper': url,
                'categories': [{'category_name': cat, 'news': news_list} for cat, news_list in category_dict.items()]
            }

            # Insert the record into the database
            db.insert(newspaper_record)

    except Exception as e:
        print(f"An error occurred while processing {url}: {str(e)}")

for website_url in websites_to_scrape:
    print('Processing: ' + website_url)
    scrape_website(website_url)
