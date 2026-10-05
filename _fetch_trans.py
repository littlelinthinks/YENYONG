import json, re, time, urllib.parse, urllib.request, sys

segs = [l.rstrip('\n') for l in open('/tmp/yenmerge/_seg_all.txt', encoding='utf-8') if l.strip()]

SKIP = {
    "YENYONG.","OVERARCHING PTE. LTD.","SGS","CE","ISO 9001","ISO 14001","ISO 45001",
    "REACH","SVHC","GA4","Formspree","WhatsApp","CARB Phase 2","FloorScore","E0","E1",
    "AQL","L/C","CoO","DoP","DoP,","PSI","A2","B1","B-s3,d0","PDF","APAC","EN 13501-1",
    "EN 13986","GB 8624","GB","CTI","SHFTS","XMNIN","YJ","TBC","SPC","WPC","PVC","HPL",
    "ACP","FR","USD","AUD","CIF","FCL","MOQ","NRC","CNC","OEM","ODM","BAU","Canton Fair",
    "Big 5 Construct","Architect Expo","Build Expo","Foshan YenYong International Building Materials Trading Co., Ltd.",
    "Foshan","Singapore","Thailand","Bangkok","China","Associated","EN","DE","FR","RU","ZH",
    "Flooring","Tiles","Singapore headquarters.","YENYONG",".","·","•","—","–","· ",
}
HEX = re.compile(r'^#?[0-9A-Fa-f]{3,8}$')
def needs_trans(s):
    if not re.search(r'[A-Za-z]', s): return False
    if HEX.match(s.strip()): return False
    if s.strip() in SKIP: return False
    # pure code like B1 [TBC], 100 m², 500m², XMNIN26000701701, etc.
    if re.fullmatch(r'[A-Za-z0-9 .,/\-–—+×°²³|&\[\]()]*', s) and not re.search(r'[a-z]{3,}', s):
        return False
    # if it's only acronyms/numbers no real words
    if not re.search(r'[a-z]{3,}', s): 
        # allow if contains a space and a capital word phrase? skip to be safe
        return False
    return True

todo = [s for s in segs if needs_trans(s)]
todo.sort(key=lambda s: -len(s))  # longest (prose) first to spend quota wisely
print("total segs", len(segs), "to translate", len(todo))

cache = {}
# resume
try:
    cache = json.load(open('/tmp/yenmerge/_ru_seg.json', encoding='utf-8'))
    print("resumed cache", len(cache))
except: pass

def trans(text):
    q = urllib.parse.quote(text)
    url = "https://api.mymemory.translated.net/get?q="+q+"&langpair=en|ru"
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
            r = urllib.request.urlopen(req, timeout=20).read().decode('utf-8')
            d = json.loads(r)
            t = d.get('responseData',{}).get('translatedText','')
            if d.get('quotaFinished'): 
                return None, True
            return t, False
        except Exception as e:
            time.sleep(1)
    return '', False

i=0
for s in todo:
    if s in cache and cache[s]:
        continue
    t, qf = trans(s)
    if qf:
        print("QUOTA FINISHED at", i); break
    if t:
        cache[s]=t
    i+=1
    if i % 50 == 0:
        json.dump(cache, open('/tmp/yenmerge/_ru_seg.json','w',encoding='utf-8'), ensure_ascii=False)
        print("progress", i, "cached", len(cache))
    time.sleep(0.25)

json.dump(cache, open('/tmp/yenmerge/_ru_seg.json','w',encoding='utf-8'), ensure_ascii=False)
print("DONE cached", len(cache))
