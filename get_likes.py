import json
import math
import requests
import tqdm
import time
import bs4

TOKEN = ''  # SET your token

def get_likes(content_id, token):
    headers = {'Authorization': f'Bearer {token}'}
    per_page = 100
    
    ret = requests.get(f'https://qiita.com/api/v2/items/{content_id}', headers=headers)
    if ret.status_code != 200:
        print(f'https://qiita.com/api/v2/items/{content_id}')
        raise requests.ConnectionError("Expected status code 200, but got {}".format(ret.status_code))
    likes_count = json.loads(ret.content.decode('utf-8'))['likes_count']
    nb_pages = math.ceil(likes_count / per_page)
    #time.sleep(3)
    
    likes = []
    for p in range(nb_pages):
        params = {'page': 1 + p, 'per_page': per_page}
        ret = requests.get(f'https://qiita.com/api/v2/items/{content_id}/likes', params=params, headers=headers)
        if ret.status_code != 200:
            raise requests.ConnectionError("Expected status code 200, but got {}".format(ret.status_code))
        likes.extend(json.loads(ret.content.decode('utf-8')))
        #time.sleep(3)
        
    return likes

def get_likes_direct(url):
    page = 1
    likes = []
    while True:
        ret = requests.get(f'{url}/likers?page={page}')
        soup = bs4.BeautifulSoup(ret.text, "html.parser")
        users = soup.find_all("li", class_="GridList__user")
        local_likes = []
        if users is not None:
            local_likes = [u.find('h4', class_='UserInfo__name').find('a')['href'][1:] for u in users]
        if len(local_likes) == 0:
            break
        local_likes = [{'user': {'id': ll}} for ll in local_likes]
        likes.extend(local_likes)
        page += 1
    return likes

with open('companies_info.json', 'r') as f:
    companies_info = json.load(f)

for company in companies_info:
    for item in company['items']:
        if 'href' in item and 'id' not in item:
            id = item['href'].split('/')[-1]
            item['id'] = id

for company in tqdm.tqdm(companies_info):
    for item in company['items']:
        if 'id' in item and 'likes' not in item:
            if len(item['id']) == 0:
                continue
           
            content_id = item['id'].split('?')[0]
            print(content_id)
            likes = get_likes_direct(item['href'])
            #likes = get_likes(content_id, token=TOKEN)
            like_ids = [lk['user']['id'] for lk in likes]
            item['likes'] = like_ids

    with open('companies_info2.json', 'w') as f:
        json.dump(companies_info, f)
