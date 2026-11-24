import json
items=json.load(open("day_items.json"))
# canonical region label per feed-region (collapse to newspaper sections)
regmap={
 "US_CANADA":"AMERICAS","AFRICA":"AFRICA","UK":"BRITAIN","NI":"EUROPE",
 "BUSINESS":"BUSINESS","HEALTH":"HEALTH","EDUCATION":"EDUCATION",
 "POLITICS":"POLITICS","EUROPE":"EUROPE","ASIA":"ASIA","WORLD":"WORLD",
 "MIDDLE_EAST":"MIDDLE EAST","LATIN_AMERICA":"AMERICAS","CHINA":"ASIA",
 "INDIA":"ASIA","TECHNOLOGY":"TECHNOLOGY","SCIENCE_ENV":"SCIENCE",
 "SCOTLAND":"BRITAIN","WALES":"BRITAIN","ENGLAND":"BRITAIN",
 "MARKETPLACE":"BUSINESS","ENTERTAINMENT":"CULTURE",
}
# prefer earlier-listed priority region for each unique title
priority=["US_CANADA","ASIA","EUROPE","AFRICA","MIDDLE_EAST","LATIN_AMERICA","WORLD",
          "CHINA","INDIA","TECHNOLOGY","BUSINESS","POLITICS","UK","HEALTH",
          "EDUCATION","SCIENCE_ENV","SCOTLAND","WALES","ENGLAND","NI"]
by_title={}
for it in items:
    t=it["title"]
    if t not in by_title:
        by_title[t]={"title":t,"src":it["region"],"pub":it["pub"]}
    else:
        # upgrade source to higher priority
        if priority.index(it["region"])<priority.index(by_title[t]["src"]):
            by_title[t]["src"]=it["region"]

curated=[]
for t,v in by_title.items():
    v["region"]=regmap.get(v["src"],v["src"])
    curated.append(v)

# sort by priority region order then pub time
order={r:i for i,r in enumerate(["WORLD","MIDDLE EAST","EUROPE","ASIA","AMERICAS","AFRICA","BRITAIN","POLITICS","BUSINESS","TECHNOLOGY","HEALTH","EDUCATION","SCIENCE","CULTURE"])}
curated.sort(key=lambda x:(order.get(x["region"],99), x["pub"]))
json.dump(curated, open("curated.json","w"), indent=1)
print("unique headlines:", len(curated))
from collections import Counter
print(Counter(c["region"] for c in curated))
for c in curated: print(f'  [{c["region"]:9}] {c["title"]}')
