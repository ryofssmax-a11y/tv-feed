#!/usr/bin/env python3
"""Usage: python3 update_feed.py <ainews|yamada|sakamichi> <items.json>
items.json = JSON array of item objects (see README). Needs env GITHUB_TOKEN."""
import base64,json,os,sys,urllib.request,datetime
name,src=sys.argv[1],sys.argv[2]
assert name in("ainews","yamada","sakamichi")
items=json.load(open(src)); items=items["items"] if isinstance(items,dict) else items
jst=datetime.timezone(datetime.timedelta(hours=9)); now=datetime.datetime.now(jst)
body=json.dumps({"date":now.strftime("%Y-%m-%d"),"updatedAt":now.isoformat(timespec="seconds"),"source":name+"-bot","items":items},ensure_ascii=False,indent=1)
api=f"https://api.github.com/repos/ryofssmax-a11y/tv-feed/contents/{name}.json"
h={"Authorization":"Bearer "+os.environ["GITHUB_TOKEN"],"Accept":"application/vnd.github+json","User-Agent":"tv-feed"}
sha=json.load(urllib.request.urlopen(urllib.request.Request(api,headers=h)))["sha"]
req=urllib.request.Request(api,method="PUT",headers=h,data=json.dumps({"message":f"update {name}","sha":sha,"content":base64.b64encode(body.encode()).decode()}).encode())
urllib.request.urlopen(req); print("updated",name,len(items),"items")
