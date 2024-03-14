import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import time

# Webpage to scrape
url = 'https://logos.fandom.com/wiki/Microsoft_Windows/Logo_Variations/'
dest_path = '/Users/miethe/Downloads/windows-logos'

restart_name = ''
restart_breakout = False

# Make request and parse HTML
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find links ending in .svg or .ai
svg_links = [a['href'] for a in soup.find_all('a', href=True) if '.svg' in a['href']]
ai_links = [a['href'] for a in soup.find_all('a', href=True) if '.ai' in a['href']]
target_links = svg_links + ai_links

# Iterate through links
for link in target_links:
    if restart_breakout and restart_name in link:
        restart_breakout = False
    if restart_breakout:
        continue

    dl_url = link.replace('?dl=0','?dl=1')
    filename = dl_url.split('/')[-1].split('?dl')[0]
    filename = filename.replace('%20','-')

    # Go to Dropbox URL
    #response = requests.get(dl_url)

    if '.svg' in filename:
        full_file_path = dest_path+'svgs/'+filename
    else:
        full_file_path = dest_path+filename

    # clean-up local filename
    try:
        urlretrieve(dl_url,full_file_path)
    except:
        print(f'Could not download: {filename}')
        continue
    print(f'Downloaded image: {filename}')

    # Find and click download button
    #soup = BeautifulSoup(response.text, 'html.parser')
    #download_btn = soup.find('div', class_='action-bar-action-DOWNLOAD_ACTION')
    #download_url = download_btn.a['href']

    # Go to download URL to trigger download
    #requests.get(download_url)

    # Delay to avoid overloading server
    time.sleep(1)

print('Done!')