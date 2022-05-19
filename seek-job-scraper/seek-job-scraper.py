import requests
import lxml.html as lh
from bs4 import BeautifulSoup
import pandas as pd
import time

'''
job_url -> https://www.seek.com.au/job/56834934?type=promoted

'''


def create_url(page):
    base_url = 'https://www.seek.com.au/'
    return f'{base_url}data-analyst-jobs/in-All-Adelaide-SA?page={page}'


def get_page(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/101.0.4951.67 Safari/537.36'}
    r = requests.get(url, headers)
    return BeautifulSoup(r.content, 'html.parser')


def get_urls_in_page(soup):
    url_list = []
    base_url = 'https://www.seek.com.au/'
    jobs = soup.find_all('article', {'data-automation': ['normalJob', 'premiumJob']})

    for item in jobs:
        a = item.find('a', href=True)
        url_list.append(base_url + a['href'])
    return url_list


def get_all_job_urls(page):
    links = []
    for i in range(1, page):
        page_url = create_url(i)
        page_soup = get_page(page_url)
        links.append(get_urls_in_page(page_soup))
        time.sleep(0.5)
        print(f'getting links from page {i}')
    return links


def main(pages):
    # flatten the 2D list
    job_links = [item for elem in get_all_job_urls(pages) for item in elem]

    df = pd.DataFrame(job_links, columns=['link'])
    df.to_csv('data/job-links.csv', index=False)


if __name__ == '__main__':
    main(5)
