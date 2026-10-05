import os, re, json

SRC = "/tmp/yenmerge"
ROOT_PAGES = ["acoustic-panel.html","aluminium-composite-panel.html","aluminium-honeycomb-panel.html","ar-preview.html","bamboo-crystal-panel.html","brand-guidelines.html","carbon-crystal-panel.html","case-studies.html","ceramic-porcelain-tile.html","certifications.html","colour-library.html","distributor-portal.html","distributors.html","exhibitions.html","factory-partners.html","factory-tour.html","flexible-stone-panel.html","founders.html","group-structure.html","hpl-compact-laminate.html","insights.html","material-calculator.html","news.html","pricing-calculator.html","product-comparison.html","product-configurator.html","pvc-wall-panel.html","quality-control.html","quote-request.html","sample-order.html","shipping-tracker.html","spc-rigid-core-flooring.html","spc-wall-panel.html","sustainability.html","videos.html","wpc-wall-panel.html"]
BLOG_PAGES = ["acoustic-panel-design.html","aging-in-place-remodel.html","bathroom-renovation-2026.html","carbon-crystal-explained.html","colour-trends-2026.html","dry-construction-benefits.html","flexible-stone-applications.html","hotel-renovation-guide.html","rental-property-upgrade.html","spc-vs-wpc-which-right.html"]

files = [(p, os.path.join(SRC,p)) for p in ROOT_PAGES] + [(os.path.join("blog",p), os.path.join(SRC,"blog",p)) for p in BLOG_PAGES]

def extract_text_segments(html):
    # remove script and style blocks
    h = re.sub(r'<script\b.*?</script>', ' ', html, flags=re.S|re.I)
    h = re.sub(r'<style\b.*?</style>', ' ', h, flags=re.S|re.I)
    # remove comments
    h = re.sub(r'<!--.*?-->', ' ', h, flags=re.S)
    segs = set()
    # meta description
    for m in re.finditer(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', h, re.I):
        if m.group(1).strip(): segs.add(m.group(1))
    # title
    for m in re.finditer(r'<title>(.*?)</title>', h, re.S|re.I):
        if m.group(1).strip(): segs.add(m.group(1))
    # alt / title / aria-label attributes
    for m in re.finditer(r'\b(alt|title|aria-label)=["\'](.*?)["\']', h, re.I):
        v=m.group(2)
        if v.strip(): segs.add(v)
    # text nodes
    for m in re.finditer(r'>([^<]+)<', h):
        t=m.group(1)
        if t.strip(): segs.add(t.strip())
    return segs

allsegs=set()
perfile={}
for rel,path in files:
    with open(path,encoding='utf-8') as f:
        html=f.read()
    segs=extract_text_segments(html)
    perfile[rel]=sorted(segs)
    allsegs|=segs

print("TOTAL FILES:", len(files))
print("TOTAL UNIQUE SEGMENTS:", len(allsegs))
with open("/tmp/yenmerge/_segments.json","w",encoding='utf-8') as f:
    json.dump({"all":sorted(allsegs),"perfile":perfile}, f, ensure_ascii=False, indent=1)
# print all unique segments
for s in sorted(allsegs):
    print("---", s)
