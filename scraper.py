import requests
from bs4 import BeautifulSoup
import os

def get_html(url):
    headers = {
         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    return response.text

def get_all_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.findAll('div', {'class': 'grid-x grid-margin-x grid-margin-y small-up-1 bp740-up-2 medium-up-2 large-up-2 bp1200-up-3'})
    results = results[0].findAll('a')
    links = []
    for result in results:
        links.append(result['href'])
    return set(links)

def get_all_pdfs(links):
    pdfs = []
    for link in links:
        html = get_html(link)
        soup = BeautifulSoup(html, 'html.parser')
        result = soup.find('a', {'class': 'btn btn-blue'})
        if result['href'].endswith('.pdf'):
            pdfs.append(result['href'])
    return pdfs

def download_pdf(url):
    headers = {
         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    response = requests.get(url, stream=True, headers=headers)  # Enable streaming for large files
    if response.status_code == 200:  # Check for a successful response
        path = os.path.join('data', url.split('/')[-1])
        if not os.path.exists('data'):
            os.makedirs('data')
        with open(path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:  # Filter out keep-alive new chunks
                    file.write(chunk)
        print(f"Downloaded: {path}")
    else:
        print(f"Failed to download PDF, status code: {response.status_code}")

links = get_all_links(get_html('https://www.muscleandstrength.com/workout-routines'))
pdfs = get_all_pdfs(links)
for pdf in pdfs:
    download_pdf(pdf)