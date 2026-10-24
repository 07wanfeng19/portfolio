#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网页数据抓取工具（作品二 · 通用型）
====================================
功能：抓取任意网页的标题、正文、链接、图片等结构化信息，导出为 CSV / JSON。

设计目标（接单可强调）：
1. 零第三方依赖（仅用标准库，客户环境无需 pip install）；
2. 自动解析 HTML，无需手写正则；
3. 支持输出 CSV / JSON 两种格式；
4. 内置 UA 与超时，礼貌抓取。

用法：
    python3 scraper.py <网址> [--out 输出.csv] [--format csv|json]

示例：
    python3 scraper.py https://example.com --out result.csv
    python3 scraper.py https://example.com --format json
"""

import sys
import csv
import json
import argparse
import urllib.request
import urllib.parse
from html.parser import HTMLParser


# ---------------------------------------------------------------------------
# 轻量 HTML 解析器：只提取标题、正文文本、链接、图片
# ---------------------------------------------------------------------------
class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.text_chunks = []      # 正文文本
        self.links = []            # (文字, href)
        self.images = []           # (alt, src)
        self._in_title = False
        self._in_script_style = False
        self._skip_tags = {"script", "style", "noscript", "svg"}
        self._cur_link = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        tag = tag.lower()
        if tag in self._skip_tags:
            self._in_script_style = True
        if tag == "title":
            self._in_title = True
        if tag == "a":
            href = attrs.get("href", "")
            self._cur_link = href
        if tag == "img":
            src = attrs.get("src", "")
            alt = attrs.get("alt", "")
            if src:
                self.images.append((alt, src))

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in self._skip_tags:
            self._in_script_style = False
        if tag == "title":
            self._in_title = False
        if tag == "a":
            self._cur_link = None

    def handle_data(self, data):
        if self._in_title:
            self.title += data.strip()
            return
        if self._in_script_style:
            return
        text = data.strip()
        if text:
            self.text_chunks.append(text)
            if self._cur_link is not None:
                self.links.append((text, self._cur_link))

    def body_text(self):
        return "\n".join(self.text_chunks)


# ---------------------------------------------------------------------------
# 抓取
# ---------------------------------------------------------------------------
def fetch(url, timeout=15):
    """抓取网页 HTML，返回 (最终URL, 文本)。"""
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0 Safari/537.36"
            )
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        # 处理常见编码
        charset = resp.headers.get_content_charset() or "utf-8"
        html_bytes = resp.read()
        final_url = resp.geturl()
    return final_url, html_bytes.decode(charset, errors="replace")


def parse(html):
    """解析 HTML，返回结构化 dict。"""
    p = PageParser()
    p.feed(html)
    # 把相对链接转绝对（基于传入的 base，这里简化处理，保留原样）
    return {
        "title": p.title,
        "text": p.body_text()[:5000],      # 正文截断，避免过大
        "text_length": len(p.body_text()),
        "links": p.links[:200],            # 最多 200 条链接
        "images": p.images[:100],          # 最多 100 张图
    }


def to_csv(data, out_path, base_url):
    """导出 CSV（链接、图片分列展开）。"""
    rows = []
    for text, href in data["links"]:
        full = urllib.parse.urljoin(base_url, href) if href else ""
        rows.append({"类型": "链接", "文字": text, "地址": full})
    for alt, src in data["images"]:
        full = urllib.parse.urljoin(base_url, src) if src else ""
        rows.append({"类型": "图片", "文字": alt, "地址": full})
    with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["类型", "文字", "地址"])
        w.writeheader()
        w.writerows(rows)
    return len(rows)


def to_json(data, out_path, base_url):
    """导出 JSON。"""
    out = {
        "title": data["title"],
        "text_length": data["text_length"],
        "text": data["text"],
        "links": [{"text": t, "url": urllib.parse.urljoin(base_url, h) if h else ""}
                  for t, h in data["links"]],
        "images": [{"alt": a, "url": urllib.parse.urljoin(base_url, s) if s else ""}
                   for a, s in data["images"]],
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    return len(data["links"]) + len(data["images"])


def main():
    ap = argparse.ArgumentParser(description="网页数据抓取工具")
    ap.add_argument("url", help="要抓取的网址")
    ap.add_argument("--out", "-o", default="", help="输出文件路径")
    ap.add_argument("--format", "-f", choices=["csv", "json"], default="csv",
                    help="输出格式（默认 csv）")
    args = ap.parse_args()

    print(f"[*] 正在抓取: {args.url}")
    try:
        final_url, html = fetch(args.url)
    except Exception as e:
        print(f"[!] 抓取失败: {e}")
        sys.exit(1)

    data = parse(html)
    print(f"[*] 页面标题: {data['title'] or '(无)'}")
    print(f"[*] 正文长度: {data['text_length']} 字符")
    print(f"[*] 链接数: {len(data['links'])} · 图片数: {len(data['images'])}")

    out_path = args.out or ("out." + args.format)
    if args.format == "csv":
        n = to_csv(data, out_path, final_url)
    else:
        n = to_json(data, out_path, final_url)
    print(f"[✓] 已导出 {n} 条记录 → {out_path}")


if __name__ == "__main__":
    main()
