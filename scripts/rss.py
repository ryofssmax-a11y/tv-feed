import json,urllib.request,datetime,xml.etree.ElementTree as ET
feeds=["https://rss.itmedia.co.jp/rss/2.0/aiplus.xml","https://news.google.com/rss/search?q=%E7%94%9F%E6%88%90AI&hl=ja&gl=JP&ceid=JP:ja"]
items=[]
for f in feeds:
  try:
    r=ET.fromstring(urllib.request.urlopen(urllib.request.Request(f,headers={"User-Agent":"Mozilla/5.0"}),timeout=20).read())
    for i in r.iter("item"):
      items.append({"title":(i.findtext("title") or "").strip(),"url":i.findtext("link"),"publisher":f.split("/")[2]})
      if len(items)%10==0: break
  except Exception as e: print(f,e)
jst=datetime.timezone(datetime.timedelta(hours=9));n=datetime.datetime.now(jst)
json.dump({"date":n.strftime("%Y-%m-%d"),"updatedAt":n.isoformat(timespec="seconds"),"source":"rss","items":items[:20]},open("rss.json","w"),ensure_ascii=False,indent=1)
print(len(items))
