import requests 
from bs4 import BeautifulSoup 
import urllib
import re


def get_latest_movirulz_url(keyword, n_results=1):
    headers = {"User-Agent": "Mozilla/5.0"}
    cookies = {"CONSENT": "YES+cb.20210720-07-p0.en+FX+410"}
    query = keyword
    query = urllib.parse.quote_plus(query)
    number_result = n_results
    google_url = "https://www.google.com/search?q=" + query + "&num=" + str(number_result)
    response = requests.get(google_url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(response.text, "html.parser")
    result = soup.find_all('div')
    results=[re.search('\/url\?q\=(.*)\&sa',str(i.find('a', href = True)['href'])) for i in result if "url" in str(i)]
    links=[i.group(1) for i in results if i != None]
    return links[0]