"""Bulk-schedule the 30 cards as FB photo posts via Graph API.
Needs CivilHub/.env with BOSOT_PAGE_TOKEN (page token for page id 1212036218657647).
Usage: python3 cards/schedule.py --start 2026-11-03 [--dry]   (one post per day at 20:30 BST)"""
import os, sys, json, datetime, subprocess, argparse
ROOT=os.path.dirname(os.path.abspath(__file__)); PAGE="1212036218657647"
env={}
ep=os.path.join(ROOT,"..",".env")
for l in (open(ep) if os.path.exists(ep) else []):
    if "=" in l and not l.startswith("#"): k,v=l.strip().split("=",1); env[k]=v.strip()
TOK=env.get("BOSOT_PAGE_TOKEN"); 
ap=argparse.ArgumentParser(); ap.add_argument("--start",required=True); ap.add_argument("--dry",action="store_true"); ap.add_argument("--hour",type=int,default=20); ap.add_argument("--minute",type=int,default=30); a=ap.parse_args()
cards=json.load(open(os.path.join(ROOT,"cards30.json")))
start=datetime.date.fromisoformat(a.start); BST=datetime.timezone(datetime.timedelta(hours=6))
for c in cards:
    day=start+datetime.timedelta(days=c["d"]-1)
    when=int(datetime.datetime(day.year,day.month,day.day,a.hour,a.minute,tzinfo=BST).timestamp())
    cap=f"{c['t']}\n\n{c['s']}\n\nআপনার বাড়ির ক্ষেত্রে কী হয়েছিল? কমেন্টে লিখুন। প্রশ্ন থাকলে ইনবক্স করুন।\n\n#বসতবাড়ি #বাড়িনির্মাণ #সিভিলইঞ্জিনিয়ারিং #StructuralEngineering #Dhaka"
    img=os.path.join(ROOT,"out",f"day{c['d']:02d}.png")
    print(f"day{c['d']:02d} → {day} 20:30 BST | {c['n']} {c['t'][:40]}")
    if a.dry: continue
    if not TOK: sys.exit("BOSOT_PAGE_TOKEN missing in CivilHub/.env")
    r=subprocess.run(["curl","-s","-F",f"source=@{img}","-F",f"message={cap}","-F","published=false","-F",f"scheduled_publish_time={when}","-F",f"access_token={TOK}",f"https://graph.facebook.com/v21.0/{PAGE}/photos"],capture_output=True,text=True)
    print("   ", r.stdout[:120].replace(TOK,"[tok]"))
