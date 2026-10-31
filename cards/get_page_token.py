"""Explorer-এর user token → long-lived → বসতবাড়ি page token, CivilHub/.env-এ সেভ।
ধাপ: CivilHub/.env-এ USER_TOKEN=<Explorer থেকে কপি> লিখুন, তারপর: python3 cards/get_page_token.py"""
import os, json, subprocess, sys
ROOT=os.path.dirname(os.path.abspath(__file__)); ENV=os.path.join(ROOT,"..",".env"); PAGE="1212036218657647"
def readenv(p):
    d={}
    if os.path.exists(p):
        for l in open(p):
            if "=" in l and not l.startswith("#"): k,v=l.strip().split("=",1); d[k]=v.strip().split(" #")[0].strip()
    return d
def g(url): return json.loads(subprocess.run(["curl","-s",url],capture_output=True,text=True).stdout)
env=readenv(ENV); app=readenv(os.path.expanduser("~/Desktop/PartTime/USFaceless/.env"))
ut=env.get("USER_TOKEN"); aid,sec=app.get("META_APP_ID"),app.get("META_APP_SECRET")
if not ut: sys.exit("USER_TOKEN নেই CivilHub/.env-এ")
if aid and sec:
    r=g(f"https://graph.facebook.com/v21.0/oauth/access_token?grant_type=fb_exchange_token&client_id={aid}&client_secret={sec}&fb_exchange_token={ut}")
    if "access_token" in r: ut=r["access_token"]; print("long-lived user token ok")
    else: print("exchange failed:",r.get("error",{}).get("message"))
acc=g(f"https://graph.facebook.com/v21.0/me/accounts?fields=name,id,access_token&limit=100&access_token={ut}")
pages={p["id"]:p for p in acc.get("data",[])}
print("pages:",[p["name"] for p in pages.values()])
if PAGE not in pages: sys.exit("বসতবাড়ি পেজ এই ইউজারের accounts-এ নেই; মিনহাজকে আপনাকে admin করতে বলুন")
lines=[l for l in (open(ENV).read().splitlines() if os.path.exists(ENV) else []) if not l.startswith("BOSOT_PAGE_TOKEN=")]
lines.append("BOSOT_PAGE_TOKEN="+pages[PAGE]["access_token"]); open(ENV,"w").write("\n".join(lines)+"\n")
dbg=g(f"https://graph.facebook.com/v21.0/debug_token?input_token={pages[PAGE]['access_token']}&access_token={ut}").get("data",{})
print("saved BOSOT_PAGE_TOKEN; expires_at:",dbg.get("expires_at",0) or "never")
