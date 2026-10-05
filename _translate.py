import os, re, sys

SRC = "/tmp/yenmerge"
OUT = "/tmp/yenmerge/ru"

ROOT_PAGES = ["acoustic-panel.html","aluminium-composite-panel.html","aluminium-honeycomb-panel.html","ar-preview.html","bamboo-crystal-panel.html","brand-guidelines.html","carbon-crystal-panel.html","case-studies.html","ceramic-porcelain-tile.html","certifications.html","colour-library.html","distributor-portal.html","distributors.html","exhibitions.html","factory-partners.html","factory-tour.html","flexible-stone-panel.html","founders.html","group-structure.html","hpl-compact-laminate.html","insights.html","material-calculator.html","news.html","pricing-calculator.html","product-comparison.html","product-configurator.html","pvc-wall-panel.html","quality-control.html","quote-request.html","sample-order.html","shipping-tracker.html","spc-rigid-core-flooring.html","spc-wall-panel.html","sustainability.html","videos.html","wpc-wall-panel.html"]
BLOG_PAGES = ["acoustic-panel-design.html","aging-in-place-remodel.html","bathroom-renovation-2026.html","carbon-crystal-explained.html","colour-trends-2026.html","dry-construction-benefits.html","flexible-stone-applications.html","hotel-renovation-guide.html","rental-property-upgrade.html","spc-vs-wpc-which-right.html"]

EDITORIAL = set(["insights.html"]) | set("blog/"+p for p in BLOG_PAGES)

# Import dictionary
sys.path.insert(0, SRC)
from _ru_dict import DICT

def rewrite_links(html, pagepath):
    def fix(m):
        href = m.group(1)
        if href.startswith(('http://','https://','//','mailto:','tel:','wa.me')):
            return m.group(0)
        if href.startswith('blog/'):
            return 'href="/ru/' + href[6:] + '"' if href[6:].endswith('.html') else m.group(0)
        if href == '/':
            return 'href="/ru/"'
        if href.startswith('/#'):
            return 'href="/ru' + href + '"'
        if href.startswith('/blog/'):
            return 'href="/ru' + href + '"'
        if href.startswith('/') and href.endswith('.html'):
            return 'href="/ru' + href + '"'
        return m.group(0)
    return re.sub(r'href="([^"]*)"', fix, html)

def lang_menu(html, pagepath):
    block = ('<div class="lang-menu"><a href="/%s">🇬🇧 EN</a>'
             '<a href="/de/%s">🇩🇪 DE</a>'
             '<a href="/fr/%s">🇫🇷 FR</a>'
             '<a href="/ru/%s" class="on">🇷🇺 RU</a>'
             '<a href="/zh/%s">🇨🇳 中文</a></div>') % (pagepath,pagepath,pagepath,pagepath,pagepath)
    return re.sub(r'<div class="lang-menu">.*?</div>', block, html, flags=re.S)

def translate(html):
    # longest-first for substring replacement
    items = sorted(DICT.items(), key=lambda kv: -len(kv[0]))
    for en, ru in items:
        if en in html:
            html = html.replace(en, ru)
    return html

def process(relpath):
    src = os.path.join(SRC, relpath)
    with open(src, encoding='utf-8') as f:
        html = f.read()
    pagepath = relpath  # e.g. "acoustic-panel.html" or "blog/foo.html"
    # 1. lang attr
    html = html.replace('<html lang="en">', '<html lang="ru">')
    # 2. rewrite internal links
    html = rewrite_links(html, pagepath)
    # 3. editorial: drop nav links div
    if relpath in EDITORIAL:
        html = re.sub(r'<div class="links">.*?</div>', '', html)
    # 4. text translation (also covers nav labels, footer, attributes)
    html = translate(html)
    # 5. lang menu (after translation so EN/other labels not touched; uses pagepath)
    html = lang_menu(html, pagepath)
    out = os.path.join(OUT, relpath)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w', encoding='utf-8') as f:
        f.write(html)
    return out

if __name__ == '__main__':
    targets = [(p, os.path.join(SRC,p)) for p in ROOT_PAGES] + [("blog/"+p, os.path.join(SRC,"blog",p)) for p in BLOG_PAGES]
    done=0
    for rel,src in targets:
        if not os.path.exists(src):
            print("MISSING SRC", rel); continue
        process(rel)
        done+=1
    print("Processed", done, "files")
