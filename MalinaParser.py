import requests
from bs4 import BeautifulSoup
import csv


links = []


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

for i in range(1, 4):
    url = f'https://ooomalina.ru/catalog/zhenskij-trikotazh/bryuki-bridzhi-shorty-zhenskie-trikotazhnye/?PAGEN_1={i}'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    items = soup.find_all('div', class_='inner_wrap TYPE_1')
    for item in items:
        a_tag = item.find('a')
        if a_tag:
            links.append(a_tag.get('href'))

result = []

for link in links:
    response = requests.get('https://ooomalina.ru'+link, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    try:
        name = soup.find('div', class_='preview-text').text.strip()
        price = soup.find('meta', itemprop="price")['content']
        description = soup.find('div', itemprop="description").text.strip()
        description = description.replace('\n', ' ').replace('\xa0', ' ').strip()

        result.append({
            'name': name,
            'price': price,
            'description': description,
        })
    except:
        continue

with open('products.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, ('name', 'price', 'description'), delimiter=';')
    writer.writeheader()
    writer.writerows(result)
