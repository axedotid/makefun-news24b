import urllib.request, xml.etree.ElementTree as ET, json, email.utils, datetime
from collections import OrderedDict

feeds = OrderedDict([
 ("WORLD","https://feeds.bbci.co.uk/news/world/rss.xml"),
 ("EUROPE","https://feeds.bbci.co.uk/news/world/europe/rss.xml"),
 ("ASIA","https://feeds.bbci.co.uk/news/world/asia/rss.xml"),
 ("MIDDLE_EAST","https://feeds.bbci.co.uk/news/world/middle_east/rss.xml"),
 ("US_CANADA","https://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml"),
 ("LATIN_AMERICA","https://feeds.bbci.co.uk/news/world/latin_america/rss.xml"),
 ("AFRICA","https://feeds.bbci.co.uk/news/world/africa/rss.xml"),
 ("CHINA","https://feeds.bbci.co.uk/news/world/asia/china/rss.xml"),
 ("INDIA","https://feeds.bbci.co.uk/news/world/asia/india/rss.xml"),
 ("UK","https://feeds.bbci.co.uk/news/uk/rss.xml"),
 ("ENGLAND","https://feeds.bbci.co.uk/news/england/rss.xml"),
 ("SCOTLAND","https://feeds.bbci.co.uk/news/scotland/rss.xml"),
 ("WALES","https://feeds.bbci.co.uk/news/wales/rss.xml"),
 ("NI","https://feeds.bbci.co.uk/news/northern_ireland/rss.xml"),
 ("BUSINESS","https://feeds.bbci.co.uk/news/business/rss.xml"),
 ("MARKETPLACE","https://feeds.bbci.co.uk/news/business/market_place/rss.xml"),
 ("TECHNOLOGY","https://feeds.bbci.co.uk/news/technology/rss.xml"),
 ("ENTERTAINMENT","https://feeds.bbci.co.uk/news/entertainment/rss.xml"),
 ("HEALTH","https://feeds.bbci.co.uk/news/health/rss.xml"),
 ("EDUCATION","https://feeds.bbci.co.uk/news/education/rss.xml"),
 ("SCIENCE_ENV","https://feeds.bbci.co.uk/news/science_and_environment/rss.xml"),
 ("POLITICS","https://feeds.bbci.co.uk/news/politics/rss.xml"),
 ("SPORTS","https://feeds.bbci.co.uk/sport/rss.xml"),
 ("HEADLINES","https://feeds.bbci.co.uk/news/headlines_and_summaries/world/rss.xml"),
])
TARGET="2026-11-24"
items=[]
seen=set()
for region,url in feeds.items():
    try:
        req=urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
        data=urllib.request.urlopen(req, timeout=20).read()
        root=ET.fromstring(data)
        for it in root.iter("item"):
            title=(it.findtext("title") or "").strip()
            pd=it.findtext("pubDate") or ""
            try:
                dt=email.utils.parsedate_to_datetime(pd)
            except Exception:
                continue
            if dt.date().isoformat()!=TARGET: continue
            key=(region,title)
            if key in seen: continue
            seen.add(key)
            items.append({"region":region,"title":title,"pub":pd})
    except Exception as e:
        print("ERR",region,e)
json.dump(items, open("day_items.json","w"), indent=1)
print("TOTAL 24 Nov items:", len(items))
for i in items:
    print(i["region"],"|",i["title"])
