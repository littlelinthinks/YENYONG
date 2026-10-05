#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Produce French-structure skeletons from English source.
Handles: lang attribute, internal link rewriting, lang-menu (FR on, page-specific),
editorial minimal nav, nav/footer/boilerplate label translation.
Leaves unique prose (hero copy, feature cards, tables, paragraphs, titles, meta)
in English for manual translation."""
import re, os

SRC = '/tmp/yenmerge'
OUT = '/tmp/yenmerge/fr'

ROOT_PAGES = [
 'acoustic-panel.html','aluminium-composite-panel.html','aluminium-honeycomb-panel.html',
 'ar-preview.html','bamboo-crystal-panel.html','brand-guidelines.html','carbon-crystal-panel.html',
 'case-studies.html','ceramic-porcelain-tile.html','certifications.html','colour-library.html',
 'distributor-portal.html','distributors.html','exhibitions.html','factory-partners.html',
 'factory-tour.html','flexible-stone-panel.html','founders.html','group-structure.html',
 'hpl-compact-laminate.html','insights.html','material-calculator.html','news.html',
 'pricing-calculator.html','product-comparison.html','product-configurator.html','pvc-wall-panel.html',
 'quality-control.html','quote-request.html','sample-order.html','shipping-tracker.html',
 'spc-rigid-core-flooring.html','spc-wall-panel.html','sustainability.html','videos.html',
 'wpc-wall-panel.html',
]
BLOG_PAGES = [
 'acoustic-panel-design.html','aging-in-place-remodel.html','bathroom-renovation-2026.html',
 'carbon-crystal-explained.html','colour-trends-2026.html','dry-construction-benefits.html',
 'flexible-stone-applications.html','hotel-renovation-guide.html','rental-property-upgrade.html',
 'spc-vs-wpc-which-right.html',
]
EDITORIAL = {'insights.html'} | {'blog/'+b for b in BLOG_PAGES}

EXTERNAL_PREFIXES = ('http://','https://','//','mailto:','tel:','data:')

def rewrite_href(v):
    if v.startswith(EXTERNAL_PREFIXES):
        return v
    if v == '/':
        return '/fr/'
    if v.startswith('/#'):
        return '/fr' + v
    if re.match(r'^/blog/[\w\-]+\.html$', v):
        return '/fr' + v
    if re.match(r'^/[\w\-]+\.html$', v):
        return '/fr' + v
    if re.match(r'^blog/[\w\-]+\.html$', v):
        return '/fr/' + v
    if re.match(r'^[\w\-]+\.html$', v):
        return '/fr/' + v
    # assets: /favicon.png, /apple-touch-icon.png, /manifest.webmanifest, /assets/...
    return v

def fix_hrefs(html):
    return re.sub(r'href="([^"]*)"', lambda m: 'href="%s"' % rewrite_href(m.group(1)), html)

# Boilerplate label translations (safe global exact-string replacements)
LABELS = [
    ('>Home</a>', '>Accueil</a>'),
    ('>Products</a>', '>Produits</a>'),
    ('>Downloads</a>', '>Téléchargements</a>'),
    ('>Projects</a>', '>Projets</a>'),
    ('>Insights</a>', '>Actualités</a>'),
    ('<h4>Products</h4>', '<h4>Produits</h4>'),
    ('<h4>Resources</h4>', '<h4>Ressources</h4>'),
    ('>SPC Flooring</a>', '>Sol SPC</a>'),
    ('>WPC Wall Panel</a>', '>Panneau mural WPC</a>'),
    ('>PVC Wall Panel</a>', '>Panneau mural PVC</a>'),
    ('>Carbon Crystal</a>', '>Panneau Carbon Crystal</a>'),
    ('>Acoustic Panel</a>', '>Panneau acoustique</a>'),
    ('>Colour Library</a>', '>Bibliothèque de couleurs</a>'),
    ('>Compare</a>', '>Comparer</a>'),
    ('>Certifications</a>', '>Certifications</a>'),
    ('>Downloads</a>', '>Téléchargements</a>'),
    # hero / cta buttons
    ('>Request Samples</a>', '>Demander un échantillon</a>'),
    ('>Email Us</a>', '>Nous contacter</a>'),
    ('>Get a Quote</a>', '>Demander un devis</a>'),
    ('>WhatsApp Us</a>', '>WhatsApp</a>'),
    ('>WhatsApp</a>', '>WhatsApp</a>'),
    # stats labels
    ('>Indicative Price</div>', '>Prix indicatif</div>'),
    ('>Min. Order</div>', '>Commande minimale</div>'),
    ('>Quote Response</div>', '>Réponse devis</div>'),
    ('>Free Samples</div>', '>Échantillons gratuits</div>'),
    ('>Min. Order</div>', '>Commande minimale</div>'),
    # slogan
    ('Building for a Sustainable Future', 'Bâtir pour un avenir durable'),
    # recurring section headings (h2)
    ('<h2>Product Overview</h2>', '<h2>Aperçu du produit</h2>'),
    ('<h2>Key Features</h2>', '<h2>Caractéristiques clés</h2>'),
    ('<h2>Technical Specifications</h2>', '<h2>Spécifications techniques</h2>'),
    ('<h2>Product Gallery</h2>', '<h2>Galerie produit</h2>'),
    ('<h2>Applications</h2>', '<h2>Applications</h2>'),
    ('<h2>Why Choose YENYONG.</h2>', '<h2>Pourquoi choisir YENYONG.</h2>'),
    # cta band
    ('<h2>Request samples & a quote</h2>', '<h2>Demander des échantillons et un devis</h2>'),
    ('Tell us your project size, finish and destination port — we respond within 24 hours.',
     'Indiquez-nous la taille de votre projet, la finition et le port de destination — nous répondons sous 24 heures.'),
    ('<title>Insights & Blog | YENYONG.</title>', '<title>Actualités et blog | YENYONG.</title>'),
]

def build(name, is_blog):
    src_path = os.path.join(SRC, 'blog' if is_blog else '', name)
    with open(src_path, encoding='utf-8') as f:
        c = f.read()
    pagepath = ('blog/' + name) if is_blog else name
    # 1. lang attribute
    c = c.replace('<html lang="en">', '<html lang="fr">')
    # 2. lang-btn flag/label
    c = c.replace('<span class="fl">🇬🇧</span><span class="lb">EN</span>',
                  '<span class="fl">🇫🇷</span><span class="lb">FR</span>')
    # 3. rewrite internal hrefs (anchors + links)
    c = fix_hrefs(c)
    # 4. regenerate lang-menu (page-specific, FR active)
    lm = ('<div class="lang-menu">'
          '<a href="/%s">🇬🇧 EN</a>' % pagepath
          + '<a href="/de/%s">🇩🇪 DE</a>' % pagepath
          + '<a href="/fr/%s" class="on">🇫🇷 FR</a>' % pagepath
          + '<a href="/ru/%s">🇷🇺 RU</a>' % pagepath
          + '<a href="/zh/%s">🇨🇳 中文</a>' % pagepath
          + '</div>')
    c = re.sub(r'<div class="lang-menu">.*?</div>', lm, c, flags=re.S)
    # 5. editorial: drop links div
    if ('blog/' + name if is_blog else name) in EDITORIAL:
        c = re.sub(r'<div class="links">.*?</div>\s*', '', c, flags=re.S)
    # 6. boilerplate labels
    for a, b in LABELS:
        c = c.replace(a, b)
    # write
    out_path = os.path.join(OUT, 'blog' if is_blog else '', name)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(c)
    return out_path

if __name__ == '__main__':
    n = 0
    for p in ROOT_PAGES:
        build(p, False); n += 1
    for p in BLOG_PAGES:
        build(p, True); n += 1
    print('skeletons written:', n)
