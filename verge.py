from bs4 import BeautifulSoup
import requests
import csv
from datetime import date
import json

header = ['id','url','headline','author','date']
all_info = []


def save_file():
    today = date.today().strftime("%d%m%Y")
    with open(today + '_verge.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(all_info)


def store_info(link, title, author, date):
    ll = []
    ll.append(all_info.__len__())
    ll.append(link)
    ll.append(title)
    ll.append(author)
    ll.append(date)
    all_info.append(ll)


def preload():
    html_text = requests.get('https://www.theverge.com/').text
    # print(html_text)

    soup = BeautifulSoup(html_text, 'lxml')
    # print(soup)


    the_script = soup.find('script', attrs={'id':'__NEXT_DATA__'}).text

    with open('script.json', 'w') as f:
        f.write(the_script)


def extraction():
    ff = open('script.json')
    data = json.load(ff)

    props = data['props']
    pageProps = props['pageProps']
    hydration = pageProps['hydration']
    mostpopularData = pageProps['mostPopularData']

    # =================================================================================

    # for hydation data
    hyd_res = hydration['responses'][0]
    hyd_data = hyd_res['data']

    frontPage_plc = hyd_data['community']['frontPage']['placements']

    for x in frontPage_plc:
        if x['placeable'] is not None:
            y = x['placeable']
            store_info(y['url'], y['title'], y['author']['fullName'], y['publishDate'][0:10])


    # =================================================================================
    rec_entries = hyd_data['entryGroup']['recentEntries']['results']
    for x in rec_entries:
        store_info(x['url'], x['title'], x['author']['fullName'], x['publishDate'][0:10])

    # =================================================================================
    hubpages = hyd_data['hubPages']

    for x in hubpages:
        for y in x['placeables']:
            store_info(y['url'], y['title'], y['author']['fullName'], y['publishDate'][0:10])

    # =================================================================================
    # for most popular data
    # print(mostpopularData)
    for x in mostpopularData:
        store_info(x['url'], x['title'], x['author']['fullName'], x['publishDate'][0:10])



# data -> community ->frontPage -> entryGroup, community, placements

# props -> pageProps -> hydration
if __name__ == "__main__":
    preload()
    extraction()
    save_file()