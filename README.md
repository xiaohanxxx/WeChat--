# WeChat-
基于微信移动端的公众号文章抓取
# 基于微信移动端公众号文章的抓取
## 使用教程
* pip install mitmproxy ，mitmproxy是一个抓取数据包的库，利用mitmproxy可以对接python脚本，用python实现监听app请求的数据包，并拦截http和https请求和响应，第一步先安装mitmproxy，确保手机和电脑在同一网络环境下，找到.mitmproxy文件夹里面的mitmproxy-ca-cert.cer证书，把这个证书安装到模拟器或手机中，当然安装的过程可能会出现很多坑，搜索引擎是你最好的帮手。

* 想要将获取到的数据保存为本地pdf文件需要用到另外一个工具wkhtmltopdf，文件大就不上传了，自行下载安装即可，安装完成后配置环境变量，将*\wkhtmltopdf\bin路径添加到path中即可。

* 完成上述步骤后，进入python安装目录的scripts目录下，查看该目录下是否有mitmdump.exe文件，把wechat+脚本拷贝到该目录下。使用cmd进入到scripts目录，输入命令mitmdump -s WeChat+.py 即可启动app监听。

* 打开模拟器，进入微信，随机选择一个公众号，进入全部历史文章，向下滑动翻看历史文章，此时cmd终端窗口会展现你需要的一切。

![展示](https://github.com/xiaohanxxx/WeChat-/blob/master/7A04590F82692E3CF4F0080B3B3F6366.gif "效果展示")
