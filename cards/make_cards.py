"""Render 30 info cards 1080x1350 in the বসতবাড়ি design system.
Usage: python3 make_cards.py [--bg cards/bg]   (optional Flow images cards/bg/dayNN.jpg|png used as photo panel)"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(ROOT,"out"); os.makedirs(OUT,exist_ok=True)
BG=os.path.join(ROOT,"bg")
W,H=1080,1350; C=(46,49,54); G=(59,60,64); Y=(245,184,28); FOG=(132,133,135); WHITE=(255,255,255); BL=(47,111,228)
BN="/System/Library/Fonts/KohinoorBangla.ttc"; LAT="/System/Library/Fonts/Supplemental/Arial Bold.ttf"
def f(sz,idx=2): return ImageFont.truetype(BN,sz,index=idx)
def fl(sz): return ImageFont.truetype(LAT,sz)
logo=Image.open(os.path.join(ROOT,"..","brand","logo.jpg")).convert("RGB").crop((110,60,490,220))
def wrap(d,text,font,maxw):
    lines=[];cur=""
    for w in text.split():
        t=(cur+" "+w).strip()
        if d.textlength(t,font=font)<=maxw: cur=t
        else: lines.append(cur); cur=w
    if cur: lines.append(cur)
    return lines
def card(c):
    im=Image.new("RGB",(W,H),C); d=ImageDraw.Draw(im)
    for x in range(0,W,40): d.line([(x,0),(x,H)],fill=(55,60,68))
    for y in range(0,H,40): d.line([(0,y),(W,y)],fill=(55,60,68))
    # photo panel (Flow image) or illustration placeholder
    bgp=None
    for ext in ("jpg","png","jpeg","webp"):
        p=os.path.join(BG,f"day{c['d']:02d}.{ext}")
        if os.path.exists(p): bgp=p;break
    panel=(60,340,1020,840)
    if bgp:
        ph=Image.open(bgp).convert("RGB"); pw,phh=panel[2]-panel[0],panel[3]-panel[1]
        r=max(pw/ph.width,phh/ph.height); ph=ph.resize((int(ph.width*r),int(ph.height*r)))
        ph=ph.crop(((ph.width-pw)//2,(ph.height-phh)//2,(ph.width-pw)//2+pw,(ph.height-phh)//2+phh))
        im.paste(ph,(panel[0],panel[1]))
    else:
        d.rectangle(panel,fill=G,outline=(80,84,90),width=2)
        d.text((W//2,585),"[ Flow image: "+c["img"][:38]+"… ]",font=fl(20),fill=FOG,anchor="mm")
    d.rectangle([(60,840),(1020,846)],fill=Y)
    # badge top-left
    b=logo.resize((190,80)); im.paste(b,(60,60))
    d.text((60,150),"বসতবাড়ি Structures",font=f(26,1),fill=FOG)
    d.text((1020,70),f"DAY {c['d']:02d} / 30",font=fl(22),fill=FOG,anchor="ra")
    d.text((1020,100),"তথ্য কার্ড",font=f(22,0),fill=FOG,anchor="ra")
    # big number
    d.text((60,300),c["n"],font=f(100,2),fill=Y,anchor="ls")
    # title
    y=890
    for ln in wrap(d,c["t"],f(60,2),960): d.text((60,y),ln,font=f(60,2),fill=WHITE); y+=78
    y+=10
    for ln in wrap(d,c["s"],f(34,0),960): d.text((60,y),ln,font=f(34,0),fill=(200,202,204)); y+=48
    d.rectangle([(60,1260),(1020,1262)],fill=(80,84,90))
    d.text((60,1280),"প্রশ্ন? ইনবক্স বা 01521-479737",font=f(26,0),fill=Y)
    d.text((1020,1280),"ইঞ্জি. এস. এম. মিনহাজ · MIEB",font=f(24,0),fill=FOG,anchor="ra")
    return im
cards=json.load(open(os.path.join(ROOT,"cards30.json")))
for c in cards: card(c).save(os.path.join(OUT,f"day{c['d']:02d}.png"))
print("rendered",len(cards))
