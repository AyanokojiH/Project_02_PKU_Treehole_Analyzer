import requests
import time
import csv
from urllib.parse import quote

pages = 1
way = None
method = None
user_want = int(input('输入爬取页数：'))
while method !=1 and method != 2:
    print("需要关键词吗？1：需要      2：不需要")
    method = int(input())
if method == 1:
    original_keyword = input('输入关键词：')
    keyword = quote(original_keyword, 'utf-8')
while way != 1 and way != 2:
    print('输入排序方式：1.按评论数降序     2.按收藏数降序')
    way = int(input())

treehole_list = []
treehole_reply_list = []
filepath = "C:\\Users\\10744\Desktop\\treeholebug\\treeholeinfo.csv"
filepath1 = "C:\\Users\\10744\Desktop\\treeholebug\\treeholeinfo.csv"
nume = 0

start_time = time.time()
while pages <= user_want:
    print(f'Dealing{pages}/{user_want}...')
    if method == 1:
        url = f"https://treehole.pku.edu.cn/api/pku_hole?page={pages}&limit=25&keyword={keyword}"
    else:
        url = f"https://treehole.pku.edu.cn/api/pku_hole?page={pages}&limit=25"
    headers = {
        #如果报错401，优先修改authorizition
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC90cmVlaG9sZS5wa3UuZWR1LmNuXC9hcGlcL2xvZ2luIiwiaWF0IjoxNzA4Nzc5MjA0LCJleHAiOjE3MDg5NTIwMDQsIm5iZiI6MTcwODc3OTIwNCwianRpIjoiWWc0NzhhOW82VXlOaHFoUyIsInN1YiI6IjIzMDAwMTI5ODIiLCJwcnYiOiIyM2JkNWM4OTQ5ZjYwMGFkYjM5ZTcwMWM0MDA4NzJkYjdhNTk3NmY3In0.3A27mGMt1tV6BT5GgZRzI3Jela2-e00EwbAEM80sDcg',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.289 Safari/537.36',
        'cookie':#素什么呢？ '',
        'X-Xsrf-token': 'eyJpdiI6IkdaZjBUOXlSd2tYeE9Xa1p2dmlUOEE9PSIsInZhbHVlIjoiSFlIYXB6Z2krbytWRjRqMUszTWVIWnZtUVpJdE9zNUM1ZS9YZUV1ZHZRVnd4WGtsQ0dYTlVlanExOEV3RzZ3RXFhSFZPWHZ3RGZ2WENhMTF1OG92OXRUNER5czhQampsZ0U5MFBIZ05NSlVKZERaNmZOL2IySDZBWTNndEFieloiLCJtYWMiOiJmMzQ3ODdiMjdjYTIwYTFmNDY2ZDI1MGM0MDY2MjM4NWY2OWZiYTdmNjRkOWJlODRlNmMyMTg2ODYwMDg3N2FmIn0=',
        'Uuid': 'Web_PKUHOLE_2.0.0_WEB_UUID_ced7890e-6f67-4363-aec1-0d5add1a74aa'
    }
    r=requests.get(url=url,headers=headers)
    if r.status_code == 200:
        pass
    else:
        print(f'访问网站时出现异常，报错码：{r.status_code}')
        break
    json_data = r.json()
    for c in json_data['data']['data']:
        content = c['text']
        being_followed = c['likenum']
        pid=c['pid']
        reply=c['reply']
        treehole_list.append({'content': content, 'being_followed': being_followed, 'pid': pid,'reply':reply})
        nume+=1
    if reply!=0:
        url1 = f"https://treehole.pku.edu.cn/api/pku_comment_v3/{pid}?limit=10"
        r1 = requests.get(url=url1,headers=headers)
        json_data1 = r1.json()
        try:
            for c in json_data1['data']['data']:
                content = c['text']
                name = c['name']
                treehole_reply_list.append({'content':content, 'author':name, 'source':pid})
        except Exception as e:
            print(f'An error occured：{e}')
            time.sleep(20)

    pages += 1
if way == 2:
    sorted_treehole_list = sorted(treehole_list, key=lambda x: x['being_followed'], reverse=True)
if way == 1:
    sorted_treehole_list = sorted(treehole_list, key=lambda x: x['reply'], reverse=True)
end_time = time.time()
print(f'共{nume}条数据,用时{-start_time+end_time:.3f}秒')
time.sleep(1)

for treehole in sorted_treehole_list:
    print(f"树洞编号{treehole['pid']}，收藏数{treehole['being_followed']}，回复数{treehole['reply']}")
    print(treehole['content'])
    print('')

with open(filepath, 'w', newline='', encoding='utf-8-sig') as csvfile:
    fieldnames = ['pid', 'being_followed', 'content','reply']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for treehole in sorted_treehole_list:
        writer.writerow(
            {'pid': treehole['pid'], 'being_followed': treehole['being_followed'], 'content': treehole['content'],'reply':treehole['reply']})

with open(filepath1, 'w', newline='', encoding='utf-8-sig') as csvfile:
    fieldnames = ['pid', 'content', 'author']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for treehole in treehole_reply_list:
        writer.writerow(
            {'pid': treehole['source'], 'content': treehole['content'], 'author': treehole['author']})

print(f"树洞数据已保存至文件：{filepath}")
print(f"各树洞回复数据已保存至文件:{filepath1}")
