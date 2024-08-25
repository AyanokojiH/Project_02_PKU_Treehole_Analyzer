# Ayano-codeworld
A gift of pkutreehole for only PKU students. The current authorization is not usable, so please try to refresh the authorization token on your PKU treehole website.
This project was done at 2024-07-02.

----提示----  
1.请确保本地安装了python且版本3.10及以上  

2.下载并解压缩至桌面后，打开命令行导航至文件pkutree.py所在目录，然后输入指令  
>python pkutree.py --q1
 
正常情况下会显示  

>Authorization failed. Please enter a new Authorization token.  
>When finished, rerun --q1 to see whether the new authorization is available:

这时，请你登录北大树洞的网页版，然后进入元素审查/开发者模式，获取请求头中的headers参数填入，具体教程可以参考  

>https://blog.csdn.net/keleinclude_/article/details/109715306

的前半部分。
填入后，再次输入指令  

>python pkutree.py --q1

如果显示Successfully entered the website 即表示成功。  

3.你可以使用指令
>python pkutree.py --h

来查看所有的功能。  
目前支持的功能有：  
q1: 检测是否联通；  
q2：统计所有的统分洞的分数信息；  
q3：统计所有的课程测评信息；  
q4：按照收藏数或者评论数排列树洞；  
q5：爬取单个树洞的所有内容；  
q6：生成树洞日榜前十；  
q7：人工设定关键词，并在关键词出现在新发的树洞里时，给用户发送微信消息。  

声明：本人完全尊重青研以及北大树洞使用规范，本程序旨在帮助广大学子有效利用树洞信息选课、生活。如有违反有关规定的风险，本人将自愿删除程序源代码。

