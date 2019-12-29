import json

with open('companies_info2.json', 'r') as f:
    companies_info = json.load(f)

def get_companies_user(company):
    user_liset = [item['user'] for item in company['items']]
    return list(set(user_liset))

def get_like_user(company):
    like_users = []
    for item in company['items']:
        if 'likes' in item:
            like_users.extend(item['likes'])
    like_users = list(set(like_users))
    return like_users

def get_prob(user, company):
    count = 0
    max_count = 0
    for item in company['items']:
        if 'likes' in item:
            if item['user'] != user:
                max_count += 1
            if user in item['likes']:
                count += 1
    return count, max_count

result = []
for company in companies_info:
    company_users = get_companies_user(company)
    like_users = get_like_user(company)
    users = list(set(company_users + like_users))

    probs = []
    for u in users:
        c, mc = get_prob(u, company)
        if mc > 5:
            probs.append(c / mc)

    count = len(list(filter(lambda x: x > 0.25, probs)))
    result.append({'name': company['name'], 'count': count})

result = sorted(result, key=lambda x: x['count'], reverse=True)

print(result[:30])
