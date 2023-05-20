# JavaScript 逆向爬虫程序设计

## 题目：[Python爬虫案例 | Scrape Center](https://scrape.center/) - [spa6](https://spa6.scrape.center/)

电影数据网站，数据通过 Ajax 加载，数据接口参数加密且有时间限制，源码经过混淆，适合 JavaScript 逆向分析。

## 思路

1. 学习网站常用数据防护方法（如JavaScript的压缩、混淆技术）
2. 分析 https://spa6.scrape.center/ 的加密方式
3. 使用 Hook 找到加密id；获取详情页 Ajax 的token
4. 使用 Python 实现详情页爬取

## 参考

1. [Python3WebSpider/ScrapeSpa6: Spider for https://spa6.scrape.center (github.com)](https://github.com/Python3WebSpider/ScrapeSpa6)
2. [爬虫学习-Scrape Center闯关(spa4,spa5,spa6)_spa6.scrape.center_鸣蜩十四的博客-CSDN博客](https://blog.csdn.net/Destiny_one/article/details/121206175)
3. [新兴爬虫利器 Playwright 的基本用法 | 静觅 (cuiqingcai.com)](https://cuiqingcai.com/36045.html)

## Contributors

- [Yitong Hu](https://yitong-hu.metattri.com/)
- [Zehao Xing](https://github.com/Sonaldovski)