import os, re, sys, glob

SRC = "/tmp/yenmerge"
OUT = "/tmp/yenmerge/zh"

ROOT_PAGES = ["acoustic-panel.html","aluminium-composite-panel.html","aluminium-honeycomb-panel.html","ar-preview.html","bamboo-crystal-panel.html","brand-guidelines.html","carbon-crystal-panel.html","case-studies.html","ceramic-porcelain-tile.html","certifications.html","colour-library.html","distributor-portal.html","distributors.html","exhibitions.html","factory-partners.html","factory-tour.html","flexible-stone-panel.html","founders.html","group-structure.html","hpl-compact-laminate.html","insights.html","material-calculator.html","news.html","pricing-calculator.html","product-comparison.html","product-configurator.html","pvc-wall-panel.html","quality-control.html","quote-request.html","sample-order.html","shipping-tracker.html","spc-rigid-core-flooring.html","spc-wall-panel.html","sustainability.html","videos.html","wpc-wall-panel.html"]
BLOG_PAGES = ["acoustic-panel-design.html","aging-in-place-remodel.html","bathroom-renovation-2026.html","carbon-crystal-explained.html","colour-trends-2026.html","dry-construction-benefits.html","flexible-stone-applications.html","hotel-renovation-guide.html","rental-property-upgrade.html","spc-vs-wpc-which-right.html"]

EDITORIAL = set(["insights.html"]) | set("blog/"+p for p in BLOG_PAGES)

sys.path.insert(0, SRC)
from zh_overrides import OVERRIDES

def load_seg():
    d = {}
    for fn in sorted(glob.glob(os.path.join(SRC, "_zhpart_*.txt"))):
        for line in open(fn, encoding='utf-8'):
            line = line.rstrip('\n')
            if '|||' not in line: 
                continue
            en, zh = line.split('|||', 1)
            en = en.strip()
            zh = zh.strip()
            if en and zh:
                d[en] = zh
    return d

DICT = load_seg()
DICT.update(OVERRIDES)  # overrides win
ITEMS = sorted(DICT.items(), key=lambda kv: -len(kv[0]))

def _apply(s):
    for en, zh in ITEMS:
        if en in s:
            s = s.replace(en, zh)
    return s

def rewrite_links(html, pagepath):
    def fix(m):
        href = m.group(1)
        if href.startswith(('http://','https://','//','mailto:','tel:','wa.me')):
            return m.group(0)
        if href.startswith(('assets/','#')):
            return m.group(0)
        if href == '/':
            return 'href="/zh/"'
        if href.startswith('/#'):
            return 'href="/zh' + href + '"'
        if href.startswith('blog/'):
            return 'href="/zh/' + href + '"'
        if href.startswith('/blog/'):
            return 'href="/zh' + href + '"'
        if href.startswith('/') and href.endswith('.html'):
            return 'href="/zh' + href + '"'
        return m.group(0)
    return re.sub(r'href="([^"]*)"', fix, html)

def lang_menu(html, pagepath):
    block = ('<div class="lang-menu"><a href="/%s">🇬🇧 EN</a>'
             '<a href="/de/%s">🇩🇪 DE</a>'
             '<a href="/fr/%s">🇫🇷 FR</a>'
             '<a href="/ru/%s">🇷🇺 RU</a>'
             '<a href="/zh/%s" class="on">🇨🇳 中文</a></div>') % (pagepath,pagepath,pagepath,pagepath,pagepath)
    return re.sub(r'<div class="lang-menu">.*?</div>', block, html, flags=re.S)

def translate(html):
    # Translate ONLY visible text nodes and text-bearing attributes.
    # Stash script/style/comment blocks so their code is never altered.
    scripts, styles, comments = [], [], []
    def stash(m, store):
        store.append(m.group(0))
        return '\x00%d\x00' % (len(store) - 1)
    h = re.sub(r'<script\b.*?</script>', lambda m: stash(m, scripts), html, flags=re.S|re.I)
    h = re.sub(r'<style\b.*?</style>', lambda m: stash(m, styles), h, flags=re.S|re.I)
    h = re.sub(r'<!--.*?-->', lambda m: stash(m, comments), h, flags=re.S)
    # visible text nodes
    h = re.sub(r'>([^<]+)<', lambda m: '>' + _apply(m.group(1)) + '<', h)
    # text-bearing attributes
    for attr in ('alt', 'title', 'aria-label', 'placeholder'):
        h = re.sub(r'(\b%s=")([^"]*)(")' % attr,
                   lambda m: m.group(1) + _apply(m.group(2)) + m.group(3), h)
    # meta description
    h = re.sub(r'(<meta\s+name=["\']description["\']\s+content=["\'])([^"\']*)(["\'])',
               lambda m: m.group(1) + _apply(m.group(2)) + m.group(3), h, flags=re.I)
    # restore stashed blocks untouched
    for i, s in enumerate(styles):
        h = h.replace('\x00%d\x00' % i, s)
    for i, s in enumerate(scripts):
        h = h.replace('\x00%d\x00' % i, s)
    for i, s in enumerate(comments):
        h = h.replace('\x00%d\x00' % i, s)
    return h

def process(relpath):
    src = os.path.join(SRC, relpath)
    with open(src, encoding='utf-8') as f:
        html = f.read()
    pagepath = relpath
    html = html.replace('<html lang="en">', '<html lang="zh">')
    html = rewrite_links(html, pagepath)
    if relpath in EDITORIAL:
        html = re.sub(r'<div class="links">.*?</div>', '', html, flags=re.S)
    html = translate(html)
    html = lang_menu(html, pagepath)
    out = os.path.join(OUT, relpath)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w', encoding='utf-8') as f:
        f.write(html)
    return out

if __name__ == '__main__':
    targets = [(p, os.path.join(SRC,p)) for p in ROOT_PAGES] + [("blog/"+p, os.path.join(SRC,"blog",p)) for p in BLOG_PAGES]
    done=0; missing=0
    for rel,src in targets:
        if not os.path.exists(src):
            print("MISSING SRC", rel); missing+=1; continue
        process(rel)
        done+=1
    print("Processed", done, "files; missing", missing)
