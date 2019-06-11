# WeChat-
基于微信移动端的公众号文章抓取
# 基于微信移动端公众号文章的抓取
## 使用教程
* pip install mitmproxy ，mitmproxy是一个抓取数据包的库，利用mitmproxy可以对接python脚本，用python实现监听app数据包，并拦截http和https请求和响应，第一步先安装mitmproxy，当然安装的过程可能会出现很多坑，搜索引擎是你最好的帮手

* 安装完成后进入安装目录，一般默认在python下的scripts目录下，把wechat+脚本拷贝到该目录下。使用cmd进入到scripts目录，输入命令mitmdump -s WeChat+.py 即可启动app监听

* 打开模拟器，进入微信，随机选择一个公众号，进入全部历史文章，向下滑动翻看历史文章，观察cmd窗口发生变化，即可自动识别该公众号的信息实现自动抓取历史文章。

![展示](https://github.com/xiaohanxxx/WeChat-/blob/master/7A04590F82692E3CF4F0080B3B3F6366.gif "效果展示")
