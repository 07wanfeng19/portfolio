# 网页数据抓取工具（作品二）

一个**零第三方依赖**的通用网页抓取脚本，用 Python 标准库即可运行，抓取任意网页的标题、正文、链接、图片，导出为 CSV / JSON。

## 功能

- 抓取网页标题、正文、所有链接、所有图片
- 自动解析 HTML（无需手写正则）
- 导出 CSV（Excel 可直接打开）或 JSON
- 内置 User-Agent 与超时，礼貌抓取
- **零依赖**：仅用 Python 标准库（urllib + html.parser），客户环境无需 `pip install`

## 用法

```bash
# 导出 CSV（默认）
python3 scraper.py https://example.com --out result.csv

# 导出 JSON
python3 scraper.py https://example.com --format json --out result.json

# 指定输出文件
python3 scraper.py https://example.com --out 我的数据.csv
```

## 实测效果

- 抓取 `https://www.baidu.com`：标题「百度一下，你就知道」，82 条链接 + 19 张图片，正确导出 CSV。

## 技术点（接单可强调）

- 纯标准库，无依赖，即拷即用
- HTMLParser 流式解析，内存占用低
- 自动编码识别（charset），处理中文网页无乱码
- 相对链接自动转绝对（urljoin）
- 结构化输出，方便后续二次处理

## 适用场景（接单需求）

- 「帮我抓 XX 网站的 XX 信息，整理成表格」
- 「把网页上的列表数据导出来」
- 「抓取图片链接存起来」

> 注意：抓取前请遵守目标网站的 robots.txt 和法律法规，不抓取需要登录/付费/隐私的内容。
