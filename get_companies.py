import json
import requests
import tqdm
import bs4

# アドベントカレンダーに参加している会社リストの取得
ret = requests.get('https://qiita.com/advent-calendar/2019/categories/company')

soup = bs4.BeautifulSoup(ret.text, "html.parser")
companies = soup.find_all("a", class_="ac-Item_name")
companies = [{'name': c.text.strip(), 'href': c['href']} for c in companies]

# 各会社の記事リストの取得
target_list = []
for company in tqdm.tqdm(companies):
    ret = requests.get('https://qiita.com' + company['href'])

    soup = bs4.BeautifulSoup(ret.text, "html.parser")
    contents = soup.find_all("div", class_="adventCalendarItem")
    
    data = []
    for content in contents:
        d = {}
        author = content.find("a", class_='adventCalendarItem_author')
        user_name = author['href'][1:]

        d['user'] = user_name
        entry = content.find("div", class_="adventCalendarItem_entry")
        if entry is not None:
            item = entry.find('a')
            if item is not None and 'https://qiita.com' in item['href']:
                d['href'] = item['href']
                d['title'] = item.text.strip()
        data.append(d)

    target_list.append({'name': company['name'], 'items': data})

with open('companies_info.json', 'w') as f:
    json.dump(target_list, f)
