import requests
from bs4 import BeautifulSoup
import json
import os

URL = "https://www.caac.gov.cn/XXGK/XXGK/GFXWJ/"
KEYWORDS = ["规定", "办法", "规则", "规范性文件", "民航规", "交通运输部令"]

def fetch_items():
    r = requests.get(URL, timeout=10)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "html.parser")
    items = []
    for a in soup.select("a"):
        text = a.get_text(strip=True)
        href = a.get("href")
        if any(k in text for k in KEYWORDS):
            if href and not href.startswith("http"):
                href = "https://www.caac.gov.cn" + href
            items.append({"title": text, "url": href})
    return items

def load_seen():
    if os.path.exists("seen.json"):
        with open("seen.json") as f:
            return set(json.load(f))
    return set()

def save_seen(seen):
    with open("seen.json", "w") as f:
        json.dump(sorted(seen), f, ensure_ascii=False, indent=2)

def send_dummy(items):
    print("🆕 发现新法规：")
    for i in items:
        print(i["title"])
        print(i["url"])

def main():
    items = fetch_items()
    seen = load_seen()
    new = [i for i in items if i["title"] not in seen]
    if new:
        send_dummy(new)
    save_seen(i["title"] for i in items)

if __name__ == "__main__":
    main()
