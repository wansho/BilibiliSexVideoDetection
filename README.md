B站软色情视频过滤
======

## 原理
手动构建了软色情词典（词的权重不同），对含有软色情信息的弹幕进行统计，得到一个视频中软色情弹幕的占比，如果占比超过0.01，则标记为软色情，否则不是软色情视频。

## 使用的库

* lxml
* requests
* BeautifulSoup

## 使用说明
打开main.py文件, 输入要测试的av号，例如 4392812，然后运行得到结果

## 下一步打算
做一个chrome浏览器插件

## 参考
https://github.com/regaliastar/bili-danmu
