import urllib.request, xml.etree.ElementTree as ET, json, email.utils, datetime

feeds = {
 "WORLD":"https://feeds.bbci.co.uk/news/world/rss.xml",
 "EUROPE":"https://feeds.bbci.co.uk/news/world/europe/rss.xml",
 "ASIA":"https://feeds.bbci.co.uk/news/world/asia/rss.xml",
 "AMERICAS":"https://feeds.bbci.co.uk/news/world/americas/rss.xml",
 "AFRICA":"https://feeds.bbci.co.uk/news/world/africa/rss.xml",
 "BUSINESS":"https://feeds.bbci.co.uk/news/business/rss.xml",
 "TECHNOLOGY":"https://feeds.bbci.co.uk/news/technology/rss.xml",
 "HEALTH":"https://feeds.bbci.co.uk/news/health/rss.xml",
 "SCIENCE":"https://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
}
TARGET = datetime.date(2026,11,24)
items=[]
for region,url in feeds.items():
    try:
        req=urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
        data=urllib.request.urlopen(req, timeout=20).read()
        root=ET.fromstring(data)
        for it in root.iter("item"):
            title=it.findtext("title") or ""
            pd=it.findtext("pubDate") or ""
            try:
                dt=email.utils.parsedate_to_datetime(pd)
            except Exception:
                continue
            d=dt.date()
            items.append({"region":region,"title":title.strip(),"date":str(d),"pub":pd})
    except Exception as e:
        print("ERR",region,e)

json.dump(items, open("all_items.json","w"), indent=1)
from collections import Counter
c=Counter(i["date"] for i in items)
print("date counts:", dict(sorted(c.items())))
print("total items:", len(items))
day=[i for i in items if i["date"]==str(TARGET)]
print("items on target day:", len(day))
