import json
import requests
import time
import csv
import re
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
import jieba
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning, module="matplotlib")
plt.rcParams['font.sans-serif'] = ['SimHei']
#预置cookies
cookies = "abRequestId=6515634b-350c-5439-ae32-926b7e07f6b0; a1=18d5fce5f605lykcampn49nbv6hwepoj7e7496kok50000287870; webId=12ed4c6fce7e3a9a196de13f17f79d9e; gid=yYf2iSd2dKWWyYf2iSd2idKTK821vTS06UI4WlTjIDhKx428EdUlVj888JYWYW88dj42Dd2K; xsecappid=xhs-pc-web; webBuild=4.1.6; acw_tc=1dce50b9481ce53ffebc8c259dd71696141787593bb07ec8bfc8bf7875348692; web_session=040069b1a2f857564de195008a374b0cc51899; unread={%22ub%22:%226598a565000000001101d7e4%22%2C%22ue%22:%2265bf01be000000002c0286c2%22%2C%22uc%22:15}; websectiga=7750c37de43b7be9de8ed9ff8ea0e576519e8cd2157322eb972ecb429a7735d4; sec_poison_id=d4635067-381e-4714-b89e-453f7aabc519"
content_list = []
name_list = []
liked_list = []
ip_list = []
sub_content_list = []
sub_name_list = []
sub_liked_list =[]
scount = 0
csv_file = "C:\\Users\\10744\\Desktop\\小红书舆情分析app\\LRBMain.csv"
csv_file1 = "C:\\Users\\10744\\Desktop\\小红书舆情分析app\\LRBSub.csv"
csv_file2 = "C:\\Users\\10744\\Desktop\\小红书舆情分析app\\LRBBad.csv"
file_path = "C:\\Users\\10744\\Desktop\\小红书舆情分析app\\LRB1.csv"
#以下是面向用户设置的语言
print('欢迎使用（未完全开发好的）小红书评论区舆情监测系统。本程序只需要您提供笔记id即可批量爬取所有评论内容并结合随机森林算法实现情感分析。')
print('请设置自定义选项：')
print("1.是否需要将主评论和回复评论一并录入csv? ")
print("1：均要录入     2：仅录入主评论      3：均不录入")
for i in range (1000):
    ans1 = input()
    if ans1 == "1":
        getmain = getsub = True
        break
    elif ans1 == "2":
        getmain = True
        getsub = False
        break
    elif ans1 == "3":
        getmain = getsub = False
        break
    else:
        print('Invalid input. Please try again!')

print('2.您希望恶评抓取更仔细还是更宽泛？')
print('请输入1-5之内的一个数。若该数越接近1，则恶评抓取将非常宽泛；若该数越接近5，则恶评抓取将非常仔细。我们建议您输入2-3.5之内的数。')
for i in range(1000):
    ans2 = input()
    if 1<float(ans2)<5:
        limits = float(ans2)
        break
    else:
        print('Invalid input. Please try again!')

print('3.您希望抓取回复评论中的疑似恶评吗？')
print('1:希望   2：不希望')
for i in range(1000):
    ans3 = input()
    if ans3 == "1":
        getsubbad = True
        break
    elif ans3 == "2":
        getsubbad = False
        break
    else:
        print('Invalid input. Please try again!')

print('4.您希望将疑似恶评信息保存至csv文件吗？')
print('1:希望   2：不希望')
for i in range(1000):
    ans4 = input()
    if ans4 == "1":
        savebad = True
        break
    elif ans4 == "2":
        savebad = False
        break
    else:
        print("Invalid input. Please try again!")

print('5.您希望生成情感得分直方图吗？')
print('1:希望   2：不希望')
for i in range(1000):
    ans5 = input()
    if ans5 == "1":
        draw = True
        break
    elif ans5 == "2":
        draw = False
        break
    else:
        print("Invalid input. Please try again!")

print('6.您希望爬取多少页评论？（请输入不大于500的正数）：')
for i in range(1000):
    try:
        userwant = int(input())
        break
    except Exception as e:
        print(f'An error occured: {e}')
        print('请重新输入')

print('初始化完成。数秒后程序将开始运行。')

time.sleep(3)

for i in range (1000):
    print('请输入24位的小红书id:(示例：62861bff0000000021035fe8)')
    note_id = input()
    #这段爬取指定笔记小红书的所有评论
    page = 1#起始页码
    count = 1#起始数量
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
        "cookie": cookies
    }
    
    url = 'https://edith.xiaohongshu.com/api/sns/web/v2/comment/page?note_id={}&top_comment_id=&image_scenes=FD_WM_WEBP,CRD_WM_WEBP'.format(
        note_id)
    response = requests.get(url=url,headers=headers)
    if response.status_code == 200 and len(note_id)==24:
        print('访问网站正常，程序继续进行。')
        time.sleep(1)
        break
    else:
        print('访问网站出现异常，如果报错404，请重新检查并输入note_id。')
        print(f'报错码：{response.status_code}')

# Assuming you have defined variables like note_id, headers, userwant, etc.

page = 1  # Assuming you have initialized the page variable
count = 1  # Assuming you have initialized the count variable
climb = 1
print(f'下面程序将爬取所有评论内容。预计用时{0.009*userwant*10:.3f}秒。')
time.sleep(1)
start_time = time.time()
while page < userwant:
    if page == 1:
        url = 'https://edith.xiaohongshu.com/api/sns/web/v2/comment/page?note_id={}&top_comment_id=&image_scenes=FD_WM_WEBP,CRD_WM_WEBP'.format(
            note_id)
    else:
        url = 'https://edith.xiaohongshu.com/api/sns/web/v2/comment/page?note_id={}&top_comment_id=&image_scenes=FD_WM_WEBP,CRD_WM_WEBP&cursor={}'.format(
            note_id, next_cursor)

    r = requests.get(url=url, headers=headers)

    try:
        json_data = r.json()
        for c in json_data['data']['comments']:
            content = c['content']
            content_list.append(content)
            name = c['user_info']['nickname']
            name_list.append(name)
            liked = c['like_count']
            liked_list.append(liked)
            sub_comment_count = c['sub_comment_count']

            print(f'正在爬取第{count}条评论')
            count += 1

            if sub_comment_count is not None:
                
                if sub_comment_count != 0:
                    
                    for sub_comment in c['sub_comments']:
                        sub_content = sub_comment['content']
                        sub_content_list.append(sub_content)
                        sub_name = sub_comment['user_info']['nickname']
                        sub_name_list.append(sub_name)
                        sub_liked = sub_comment['like_count']
                        sub_liked_list.append(sub_liked)
                        scount += 1
            else:
                print('该评论无回复。')

        next_cursor = json_data['data']['cursor']
        if not json_data['data']['has_more']:
            print('No more data. Analyst ends!')
            break  # This will break out of the while loop

        page += 1

    except Exception as e:
        print(f'解析网站json出现问题: {e}。很有可能是备用的cookies出现了异常或是没有登录。请登录后重新在网页上捕捉cookies并且输入。')
        new_cookies = input()
        cookies = new_cookies
end_time = time.time()
print(f'爬取完毕，总耗时{end_time-start_time:.3f}秒。')
time.sleep(1)
# 这段尝试将所爬取的评论保存至csv

comments_data = {
    'Content': content_list,
    'Name': name_list,
    'Liked': liked_list,
    'IP': ip_list
}
sub_comments_data = {
    'Content': sub_content_list,
    'Name': sub_name_list,
    'Liked': sub_liked_list
}
fieldnames = ['Content', 'Name', 'Liked']

if getmain:
    with open(csv_file, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        # 写入表头
        writer.writeheader()
        # 写入评论数据
        for content, name, liked in zip(content_list, name_list, liked_list):
            writer.writerow({
                'Content': content,
                'Name': name,
                'Liked': liked
            })

    print('主评论数据已成功保存到 CSV 文件: ', csv_file)
    print('')
    time.sleep(3)
if getsub:
    with open(csv_file1, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        # 写入表头
        writer.writeheader()
        # 写入评论数据
        for content, name, liked in zip(sub_content_list, sub_name_list, sub_liked_list):
            writer.writerow({
                'Content': content,
                'Name': name,
                'Liked': liked
            })
    print('回复评论数据已成功保存到 CSV 文件: ', csv_file1)
    print('')
    time.sleep(3)
maxi = 0
mini = 5
score_list = []
#这是舆情分析环节
print(f'下面准备进行舆情分析，用时可能较长（预计用时{0.007*count:.3f}秒）')
time.sleep(1)
print('下面进行程序自训练：')
print('')
time.sleep(1)
#这段是程序训练过程
data = pd.read_csv(file_path)
print('Successfully loaded the data.Now processing.')
time.sleep(0.5)
# 3. 数据预处理
# 对中文评论进行分词
data['tokenized_content'] = data['Content'].apply(
    lambda x: ' '.join(jieba.cut(x)))
data.dropna(subset=['tokenized_content', 'Score'], inplace=True)
# 4. 划分数据集
X = data['tokenized_content']
y = data['Score']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
print('Successfully divided the data.Now capting features.')
time.sleep(0.5)
# 5. 特征工程
tfidf_vectorizer = TfidfVectorizer(max_features=5000)  # 调整 max_features
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
X_test_tfidf = tfidf_vectorizer.transform(X_test)

# 6. 选择模型
model = RandomForestRegressor(n_estimators=100, random_state=42)

# 7. 训练模型
model.fit(X_train_tfidf, y_train)

# 8. 评估模型
y_pred = model.predict(X_test_tfidf)

# 评估回归模型
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print('模型自训练完毕。')
print(f'Mean Squared Error: {mse}')
print(f'R^2 Score: {r2}')
time.sleep(2)
done = 0
total = 0
##这段尝试进行舆情分析
negative_comments = []
comment_sentiment = None
def analyze_sentiment(content):
    s = SnowNLP(content)
    return s.sentiments
# Iterate through comments and perform sentiment analysis
for i in range(len(content_list)):
    content = content_list[i]
    name = name_list[i]
    liked = liked_list[i]

    # Perform sentiment analysis on the comment
    try:
        if content == "":
            done+1
            pass
        else:
            tokenized_new_comment = ' '.join(jieba.cut(content))
            new_comment_tfidf = tfidf_vectorizer.transform([tokenized_new_comment])
            comment_sentiment = model.predict(new_comment_tfidf)[0]
            if comment_sentiment > maxi:
                maxi = comment_sentiment
            if comment_sentiment <mini:
                mini = comment_sentiment
            total += comment_sentiment
            score_list.append(comment_sentiment)
            done+=1
    except Exception as e:
        print(f'An error occured: {e}')
        time.sleep(10)
    print(f'正在分析第{done}条主评论,进度{done}/{count}') 
    # Check if sentiment score is less than 0.5 and store in the negative_comments list
    try:
        if comment_sentiment < limits:
            negative_comments.append({
                'content': content,
                'username': name,
                'sentiment_score': comment_sentiment
            })
    except Exception as e:
        print(f'An error occured: {e}')
        time.sleep(10)
if getsubbad:
        subdone = 1
        for i in range(len(sub_content_list)):
            content = sub_content_list[i]
            name = sub_name_list[i]
            liked = sub_liked_list[i]

            # Perform sentiment analysis on the comment
            try:
                if content == "":
                    done+1
                    pass
                else:
                    tokenized_new_comment = ' '.join(jieba.cut(content))
                    new_comment_tfidf = tfidf_vectorizer.transform(
                        [tokenized_new_comment])
                    comment_sentiment = model.predict(new_comment_tfidf)[0]
                    if comment_sentiment > maxi:
                        maxi = comment_sentiment
                    if comment_sentiment <mini:
                        mini = comment_sentiment
                    total += comment_sentiment
                    score_list.append(comment_sentiment)
                    done += 1
            except Exception as e:
                print(f'An error occured: {e}')
                time.sleep(10)
            print(f'正在分析第{subdone}条回复评论：进度{subdone}/{scount}')
            subdone+=1
            # Check if sentiment score is less than 0.5 and store in the negative_comments list
            try:
                if comment_sentiment < limits:
                    negative_comments.append({
                        'content': content,
                        'username': name,
                        'sentiment_score': comment_sentiment
                    })
            except:
                print(f'An error occured: {e}')
                time.sleep(10)
print('')
avg = total/done
# Display comments with sentiment scores less than 0.5
print(f'舆情分析完成。平均情感得分（1为最低，5为最高）：{avg:.3f}，最高情感得分：{maxi:.3f}，最低情感得分：{mini:.3f}')
if avg>=3.8:
    print('舆情表现良好，恭喜您。')
    time.sleep(2)
elif 3.3<=avg<3.8:
    print('舆情整体良好但偶有恶评。请稍加注意即可。')
    time.sleep(2)
elif 2.7<=avg<3.3:
    print('您面临舆情危机。请谨慎小心。')
    time.sleep(2)
else:
    print('您面临严重的舆情危机。注意！')
    time.sleep(2)

print('\n以下是疑似恶评：')
for comment in negative_comments:
    print('用户名：', comment['username'])
    print('评论内容：', comment['content'])
    print('情感得分：', f"{comment['sentiment_score']:.3f}")
    print('')
time.sleep(2)
if savebad:
    with open(csv_file2, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        # 写入表头
        writer.writeheader()
        # 写入评论数据
        for comment in negative_comments:
            writer.writerow({
                'Content': content,
                'Name': name,
                'Liked': liked
            })

    print('评论疑似恶评数据已成功保存到 CSV 文件: ', csv_file2)
if draw:
    plt.hist(score_list, bins=range(int(min(score_list)), int(max(score_list)) + 1), edgecolor='black')
    plt.title('情感得分频率直方图')
    plt.xlabel('数值')
    plt.ylabel('频率')
    plt.show()
time.sleep(3)
print('感谢您使用此程序，祝您生活愉快！')
