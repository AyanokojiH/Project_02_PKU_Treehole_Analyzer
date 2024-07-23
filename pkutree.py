"""
All rights reserved by Ayanokoji.H.
"""
import time
from datetime import datetime, timedelta
import requests
from tqdm import tqdm
import matplotlib.pyplot as plt
import re
from collections import defaultdict
import csv
import argparse
import yaml
import itchat
import itchat.content


def timestamp_to_datetime(timestamp_10):
    timestamp_10 = int(timestamp_10)
    dt_object = datetime.utcfromtimestamp(timestamp_10)
    datetime_str = dt_object.strftime('%Y-%m-%d %H:%M:%S')
    return datetime_str


def is_within_last_24_hours(timestamp_10):
    dt_object = datetime.utcfromtimestamp(int(timestamp_10))
    now = datetime.utcnow()
    twenty_four_hours_ago = now - timedelta(hours=24)
    return twenty_four_hours_ago <= dt_object < now


def write_authorization(token):
    with open('authorization.yaml', 'w') as f:
        yaml.dump(token, f)


class test:
    def __init__(self):
        with open('authorization.yaml', 'r') as f:
            strings = yaml.safe_load(f)
        self.headers_global = {
            'Authorization': strings,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/114.0.5735.289 Safari/537.36',
            'cookie': 'pku_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9'
                      '.eyJpc3MiOiJodHRwOlwvXC90cmVlaG9sZS5wa3UuZWR1LmNuXC9hcGlcL2xvZ2luIiwiaWF0IjoxNzA4Nzc5MjA0LCJleHAiOjE3MDg5NTIwMDQsIm5iZiI6MTcwODc3OTIwNCwianRpIjoiWWc0NzhhOW82VXlOaHFoUyIsInN1YiI6IjIzMDAwMTI5ODIiLCJwcnYiOiIyM2JkNWM4OTQ5ZjYwMGFkYjM5ZTcwMWM0MDA4NzJkYjdhNTk3NmY3In0.3A27mGMt1tV6BT5GgZRzI3Jela2-e00EwbAEM80sDcg; XSRF-TOKEN=eyJpdiI6InpaczBrVXRsdDVvMkYreGpDczl6Rnc9PSIsInZhbHVlIjoieXhBYzR5QWduSk9td1E0ZUQ5TEJ1ZnRwbFRHRjBYZDFVMVJzdmlpVUd1VjJPeCtoMWtyc3J3eUR0Qlp5eVlUT3BNVC9EaC8wVVJNMEw4ZEp6L2xTWXorei9qUmZ0Qk1WdzM3Z2x0RWxNN1lWQlBOOEVBRlN0Znd1aUZmaXNZSk4iLCJtYWMiOiI0N2FkOGY5YmU2MmZmN2I5MzM1MGY3MGFlNTY0MGYyZDEyYzQ5NWIyOWE2M2Y5NDBiMDdiZWM5MmFiM2U4NzVmIn0%3D; _session=eyJpdiI6Imk5TXh5K1oxMmM1ZFFSOThyS0pLR0E9PSIsInZhbHVlIjoibE9xY1JMNEJDZWJGaFZLMEpsS09PQmlwSWxQVUlVdW5kc0dxdk5DVFlHS3F4UCtSdk1tYTUwMWRTWHJBS1JSR3VnMXQ1Skk0ZXQzL2hIdEJGbHhOc2tEZU5sbnhJRzExT0pOYnhjSkpLbWl1Um5zdmVxcjNwUmNCR3g3bzhPcHMiLCJtYWMiOiJkODFiNjllMjIzYjNkMTU1MTUzOGNhOTU5MzRjZWNjY2JkZDE2MjEyN2M0ZjBhZDMyMjM0ZDA2ODNiOWI2ZjUwIn0%3D',
            'X-Xsrf-token': 'eyJpdiI6IkdaZjBUOXlSd2tYeE9Xa1p2dmlUOEE9PSIsInZhbHVlIjoiSFlIYXB6Z2krbytWRjRqMUszTWVIWnZtUVpJdE9zNUM1ZS9YZUV1ZHZRVnd4WGtsQ0dYTlVlanExOEV3RzZ3RXFhSFZPWHZ3RGZ2WENhMTF1OG92OXRUNER5czhQampsZ0U5MFBIZ05NSlVKZERaNmZOL2IySDZBWTNndEFieloiLCJtYWMiOiJmMzQ3ODdiMjdjYTIwYTFmNDY2ZDI1MGM0MDY2MjM4NWY2OWZiYTdmNjRkOWJlODRlNmMyMTg2ODYwMDg3N2FmIn0=',
            'Uuid': 'Web_PKUHOLE_2.0.0_WEB_UUID_ced7890e-6f67-4363-aec1-0d5add1a74aa'
        }

    def testing(self):
        url = "https://treehole.pku.edu.cn/api/pku_hole?page=1&limit=25"
        headers = self.headers_global.copy()

        r = requests.get(url=url, headers=headers)
        if r.status_code != 200:
            print("Authorization failed. Please enter a new Authorization token.")
            new_token = input(
                "When finished, rerun --q1 to see whether the new authorization is available:").strip()
            write_authorization(new_token)
            headers = self.headers_global.copy()  # 更新测试类的headers属性
            r1 = requests.get(url=url, headers=headers)
            if r1.status_code == 200:
                print("Successfully entered the website.")
            else:
                pass
        else:
            print("Successfully entered the website.")


'''
功能1：统分洞查询器
'''


class TreeHoleAnalyzer:
    def __init__(self):
        self.setmax = 100
        self.setmin = 35
        self.totalholenum = 0
        self.totalholescore = 0
        self.upperbound = 0
        self.yearly_scores = defaultdict(list)

    @staticmethod
    def extract_score(text, max_score, min_score):
        if '正太' in text or '正态' in text:
            return 84
        numbers = re.findall(r'\d+', text)
        if not numbers:
            return None
        scores = [int(num) for num in numbers]
        valid_scores = []
        for score in scores:
            if score > max_score or score < min_score:
                continue
            match = re.search(r'\d+[+\-]', text)
            if match and match.start() > text.index(str(score)) + len(str(score)):
                continue
            valid_scores.append(score)
        if not valid_scores:
            return None
        return valid_scores[0]

    def run_analysis(self):
        print("请输入您想查询的科目（多个关键词之间用空格连接），与树洞查询格式相同")
        print("示例1： 高数A")
        print("示例2： 高数A zzn")
        print("示例3： 高数A zzn 期中")
        print("")
        query = input() + " 统分"

        print("如果您查询的科目是高数线代一类的数学课，则可能会有很多“钓鱼”成绩。为此，您需要设置可置信的分数区间。")
        print("请您输入置信分数区间（示例：40 98）：")
        ans = input().strip()
        self.setmin, self.setmax = map(int, ans.split())
        assert type(self.setmin) is int
        assert type(self.setmax) is int

        print("您想统计多少条树洞？")
        ans2 = input().strip()
        self.upperbound = int(ans2)

        curpage = 1
        treeholenum = 0
        while curpage <= 100 and treeholenum < self.upperbound:
            url1 = f"https://treehole.pku.edu.cn/api/pku_hole?page={curpage}&limit=25&keyword={query}"
            t = test()
            r2 = requests.get(url=url1, headers=t.headers_global)
            json_data = r2.json()

            for c in json_data['data']['data']:
                thisholenum = 0
                thisholescore = 0
                pid = c['pid']

                try:
                    nowpage = 1
                    while nowpage <= 10:
                        urlthis = f"https://treehole.pku.edu.cn/api/pku_comment_v3/{pid}?page={nowpage}&limit=10"
                        t = test()
                        r3 = requests.get(url=urlthis, headers=t.headers_global)
                        json_data2 = r3.json()

                        for d in json_data2['data']['data']:
                            content = d['text']
                            timestamp = d['timestamp']
                            date = timestamp_to_datetime(timestamp)
                            year = date[:4]

                            curscore = self.extract_score(content, max_score=self.setmax, min_score=self.setmin)
                            if curscore is not None:
                                self.yearly_scores[year].append(curscore)
                                thisholenum += 1
                                thisholescore += curscore
                                self.totalholenum += 1
                                self.totalholescore += curscore

                        nowpage += 1
                except Exception:
                    print(f"树洞{pid}的回复加载完毕。")

                    try:
                        treeholenum += 1
                        print(f"树洞{pid}里的平均统分结果为{thisholescore / thisholenum:.3f}")
                    except Exception:
                        pass

                print("")

            curpage += 1

        print(f"在您查询的时间之内，所有树洞的平均统分结果为{self.totalholescore / self.totalholenum:.3f}")

    def plot_yearly_scores(self):
        average_scores = {year: sum(scores) / len(scores) for year, scores in self.yearly_scores.items()}
        years = list(average_scores.keys())
        scores = list(average_scores.values())

        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        plt.figure(figsize=(10, 6))
        plt.bar(years, scores, color='skyblue')
        plt.xlabel('年份')
        plt.ylabel('平均统分')
        plt.title('树洞统分平均值按年份分布')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


'''
功能2：课程测评查询器
'''


class commentcollector:
    def __init__(self):
        self.csv_file = None
        self.keyword = None
        self.upperbound = None
        self.needcsv = False
        self.csvfile = None

    def run_collector(self):
        print("请输入您想测评的课程的名称（按照树洞tag输入，示例：高数A1）")
        ans = input()
        self.keyword = ans + " 课程测评"
        print("您想查询多少页课程测评？每页最多有25条")
        ans3 = input()
        self.upperbound = int(ans3)
        print("需要excel记录吗？（yes/no）")
        ans2 = input()
        assert ans2 == "yes" or ans2 == "no"
        self.needcsv = True if ans2 == "yes" else False

        if self.needcsv:
            self.csv_file = open('kccp.csv', 'w', newline='', encoding='utf-8-sig')
            csv_writer = csv.writer(self.csv_file)
            csv_writer.writerow(['Date', 'PID', 'Content'])

        curpage = 1
        while curpage <= self.upperbound:
            url1 = f"https://treehole.pku.edu.cn/api/pku_hole?page={curpage}&limit=25&keyword={self.keyword}"
            t = test()
            r1 = requests.get(url=url1, headers=t.headers_global)
            json_data = r1.json()

            for c in json_data['data']['data']:
                pid = c['pid']
                date = timestamp_to_datetime(c['timestamp'])
                try:
                    t = test()
                    nowpage = 1
                    while nowpage < 100:
                        urlthis = f"https://treehole.pku.edu.cn/api/pku_comment_v3/{pid}?page={nowpage}&limit=10"
                        r2 = requests.get(url=urlthis, headers=t.headers_global)
                        json_data1 = r2.json()
                        for d in json_data1['data']['data']:
                            content = d['text']
                            name = d['name']
                            if name == "洞主" and re.search(ans, content, re.IGNORECASE):
                                print(f"At {date}, in {pid} writes: ")
                                print(content)
                                print('')

                                if self.needcsv:
                                    csv_writer = csv.writer(self.csv_file)
                                    csv_writer.writerow([date, pid, content])  # 写入CSV文件

                        nowpage += 1

                except Exception:
                    pass

            curpage += 1

        if self.needcsv:
            self.csv_file.close()


'''
功能3：按照评论数或回复数降序排列树洞内容
'''


class TreeholeSorter:
    def __init__(self):
        self.way = None
        self.upperbound = 10
        self.keyword = None
        self.url = None
        self.pages = 1
        self.treeholelist = []
        self.nume = 0
        self.needcsv = False
        self.csv_file = None

    def sorter(self):
        print("您可以选择按照评论数或者收藏数降序排列指定区间内的树洞内容。")
        print("输入1：按照评论数降序      输入2：按照收藏数降序")
        self.way = int(input())
        assert self.way == 1 or self.way == 2
        print("请输入您希望爬取的页码数量（每页有25条树洞）：")
        self.upperbound = int(input())
        print("请输入关键词，如没有请输入no")
        ans = input()
        print("需要excel记录吗？(yes/no)")
        ans2 = input()
        assert ans2 == "yes" or ans2 == "no"
        self.needcsv = True if ans2 == "yes" else False

        if ans != "no":
            self.keyword = ans
            self.url = f"https://treehole.pku.edu.cn/api/pku_hole?page={self.pages}&limit=25&keyword={self.keyword}"
        else:
            self.url = f"https://treehole.pku.edu.cn/api/pku_hole?page={self.pages}&limit=25"

        sorted_treehole_list = []
        progress_bar = tqdm(total=self.upperbound)
        while self.pages <= self.upperbound:
            t = test()
            if ans != "no":
                self.keyword = ans
                self.url = f"https://treehole.pku.edu.cn/api/pku_hole?page={self.pages}&limit=25&keyword={self.keyword}"
            else:
                self.url = f"https://treehole.pku.edu.cn/api/pku_hole?page={self.pages}&limit=25"
            r = requests.get(url=self.url, headers=t.headers_global)
            json_data = r.json()
            current_page_progress = (self.pages / self.upperbound) * 100
            progress_bar.set_description(f"Page {self.pages}/{self.upperbound} ({current_page_progress:.2f}%)")
            for c in json_data['data']['data']:
                content = c['text']
                being_followed = c['likenum']
                pid = c['pid']
                reply = c['reply']
                timess = timestamp_to_datetime(c['timestamp'])
                self.treeholelist.append({
                    'times': timess,
                    'content': content,
                    'being_followed': being_followed,
                    'pid': pid,
                    'reply': reply
                })
                self.nume += 1
                progress_bar.update(1)
            self.pages += 1
        progress_bar.close()

        if self.way == 2:
            sorted_treehole_list = sorted(self.treeholelist, key=lambda x: x['being_followed'], reverse=True)
        elif self.way == 1:
            sorted_treehole_list = sorted(self.treeholelist, key=lambda x: x['reply'], reverse=True)

        if self.needcsv:
            self.csv_file = open('sdpx.csv', 'w', newline='', encoding='utf-8-sig')
            csv_writer = csv.writer(self.csv_file)
            csv_writer.writerow(['Treehole ID', 'Post Time', 'Favorites', 'Replies', 'Content'])
            for treehole in sorted_treehole_list:
                csv_writer.writerow([treehole['pid'], treehole['times'], treehole['being_followed'], treehole['reply'],
                                     treehole['content']])
            self.csv_file.close()

        print(f"Total {self.nume} treeholes.")
        for treehole in sorted_treehole_list:
            print(
                f"Treehole ID: {treehole['pid']}, Post Time: {treehole['times']}, "
                f"Favorites: {treehole['being_followed']}, Replies: {treehole['reply']}")
            print(treehole['content'])
            print('')

        if self.needcsv:
            self.csv_file.close()  # 关闭CSV文件


'''
功能4：将指定的树洞以csv形式记录内容
'''


class treeholecatcher:
    def __init__(self):
        self.pid = 0
        self.address = "zdsd.csv"
        self.needcsv = False

    def catcher(self):
        print('请输入您想爬取的树洞号（示例：6125565）：')
        self.pid = int(input())
        print("需要excel记录吗？（yes/no）")
        ans = input()
        assert ans == "yes" or ans == "no"
        self.needcsv = True if ans == "yes" else False

        nowpage = 1
        if self.needcsv:
            with open(self.address, 'w', newline='', encoding='utf-8-sig') as csvfile:
                fieldnames = ['Timestamp', 'Name', 'Content']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

        while nowpage <= 1000:
            urlthis = f"https://treehole.pku.edu.cn/api/pku_comment_v3/{self.pid}?page={nowpage}&limit=10"
            t = test()
            r3 = requests.get(url=urlthis, headers=t.headers_global)
            json_data2 = r3.json()

            try:
                for d in json_data2['data']['data']:
                    content = d['text']
                    timestamp = d['timestamp']
                    name = d['name']
                    date = timestamp_to_datetime(timestamp)
                    print(f"At {date},{name} said {content} ")
                    if self.needcsv:
                        writer.writerow({'Timestamp': date, 'Name': name, 'Content': content})

                nowpage += 1
            except Exception:
                print(f"内容爬取完毕。")
                break
        if self.needcsv:
            print(f"数据已保存至 {self.address}")


'''
功能5：生成当日树洞热榜
'''


class getbest:
    def __init__(self):
        self.date = None
        self.url = None
        self.pages = 1

    def run(self):
        date = datetime.now()
        self.date = date.strftime("%Y-%m-%d %H:%M")

        sorted_treehole_list = []
        max_pages = 75
        self.pages = 1
        with tqdm(total=max_pages, desc="Fetching Pages") as pbar:
            while self.pages <= max_pages:
                self.url = f"https://treehole.pku.edu.cn/api/pku_hole?page={self.pages}&limit=25"
                r = requests.get(url=self.url, headers=test().headers_global)
                json_data = r.json()
                # 处理页面数据
                for c in json_data['data']['data']:
                    being_followed = c['likenum']
                    pid = c['pid']
                    reply = c['reply']
                    content = c['text']
                    if is_within_last_24_hours(c['timestamp']):
                        sorted_treehole_list.append({
                            'pid': pid,
                            'value': being_followed * 1.2 + reply * 1.8,
                            'content': content
                        })
                pbar.update(1)
                self.pages += 1
                pbar.set_postfix(page=self.pages)

        print("")
        sorted_treehole_list = sorted(sorted_treehole_list, key=lambda x: x['value'], reverse=True)
        print("今日树洞热榜前十：")
        for iteration, treehole in enumerate(sorted_treehole_list[:10], start=1):  # 使用enumerate遍历前十项
            print("")
            print(f"第{iteration}名：树洞号{treehole['pid']}, 热度{treehole['value']:.1f}")
            print(f"{treehole['content']}")

class send_wechat_message:
    def __init__(self):
        self.kw = None
        self.refresh = 30
        self.num = 1
        self.url = f"https://treehole.pku.edu.cn/api/pku_hole?page={self.num}&limit=25"

    def run(self):
        print('请输入关键词：')
        self.kw = input()
        sender = input("请输入你所要发送给好友的备注（注意，是你给好友的备注，如果你想发送给自己就输入文件传输助手）：")
        print('请设置监听时长（分钟）：')
        self.num = int(input())
        itchat.auto_login(hotReload=True)
        friends = itchat.search_friends(sender)
        num = 0

        sended_list = []

        while num<self.num*2:
            t = test()
            r = requests.get(url = self.url,headers = t.headers_global)
            json_data = r.json()

            for c in json_data['data']['data']:
                content = c['text']
                pid = c['pid']
                timess = timestamp_to_datetime(c['timestamp'])
                if self.kw in content:
                    if pid not in sended_list:
                        itchat.send(f"At {timess},in {pid} said {content} ", toUserName=friends[0]['UserName'])
                        sended_list.append(pid)

            num+=1
            print(f"已经监听第{num}次")
            time.sleep(self.refresh)

        print('监听结束。')




def main():
    parser = argparse.ArgumentParser(description="选择要运行的功能")
    parser.add_argument('--q1', action='store_true', help="测试是否联通网站")
    parser.add_argument('--q2', action='store_true', help="统分洞统计")
    parser.add_argument('--q3', action='store_true', help="课程测评总结")
    parser.add_argument('--q4', action='store_true', help="降序排列树洞")
    parser.add_argument('--q5', action='store_true', help="爬取指定树洞")
    parser.add_argument("--q6", action='store_true', help="树洞热榜前十")
    parser.add_argument('--q7', action='store_true', help="树洞关键词监听")
    args = parser.parse_args()

    if args.q1:
        t1 = test()
        t1.testing()
    elif args.q2:
        t2 = TreeHoleAnalyzer()
        t2.run_analysis()
        t2.plot_yearly_scores()
    elif args.q3:
        t3 = commentcollector()
        t3.run_collector()
    elif args.q4:
        t4 = TreeholeSorter()
        t4.sorter()
    elif args.q5:
        t5 = treeholecatcher()
        t5.catcher()
    elif args.q6:
        t6 = getbest()
        t6.run()
    elif args.q7:
        t7 = send_wechat_message()
        t7.run()
    else:
        print("Please insert correct commands.")


if __name__ == "__main__":
    main()