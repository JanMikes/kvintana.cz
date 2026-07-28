# -*- coding: utf-8 -*-
"""Kvintána — static site generator.

Renders the whole prototype into plain .html files at the project root.
No dependencies beyond the standard library.

    python3 tools/build.py
"""

import os
import re
import sys
import html
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import (  # noqa: E402
    SITE, SITE_URL, FORMSPREE, SHOWS, OFFERS, FILMS, HORSES, ALBUMS,
    GALLERY_CATS, PARTNERS, FACTS, REDIRECTS,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")

# --------------------------------------------------------------------------
# Image helpers
# --------------------------------------------------------------------------

_WIDTHS = {}        # name -> [widths] with a WebP file
_AVIF = {}          # name -> [widths] with an AVIF file


def scan_images():
    """Map every asset name to the widths that were actually generated."""
    if not os.path.isdir(IMG):
        sys.exit("assets/img is missing — run `sh tools/build_images.sh` first.")
    for f in os.listdir(IMG):
        m = re.match(r"^(.+)-(\d+)\.(webp|avif)$", f)
        if m:
            table = _WIDTHS if m.group(3) == "webp" else _AVIF
            table.setdefault(m.group(1), []).append(int(m.group(2)))
    for table in (_WIDTHS, _AVIF):
        for k in table:
            table[k].sort()


def pic(name, alt, sizes="100vw", cls="", ratio=None, eager=False, pos=None):
    """Responsive <picture>. All paths are root-relative."""
    widths = _WIDTHS.get(name)
    if not widths:
        return ('<div class="%s" style="aspect-ratio:%s;background:var(--night-card)"></div>'
                % (cls, ratio or "4/3"))
    srcset = ", ".join("/assets/img/%s-%d.webp %dw" % (name, w, w) for w in widths)
    avif = ""
    if _AVIF.get(name):
        avif = '<source type="image/avif" srcset="%s" sizes="%s">' % (
            ", ".join("/assets/img/%s-%d.avif %dw" % (name, w, w)
                      for w in _AVIF[name]), sizes)
    # An explicit aspect-ratio without object-fit stretches the photo — always
    # pair them. `pos` steers the crop when the subject isn't centred.
    if ratio:
        style = ' style="aspect-ratio:%s;object-fit:cover;object-position:%s"' % (
            ratio, pos or "center")
    else:
        style = ' style="object-position:%s"' % pos if pos else ""
    return (
        '<picture>'
        '%s'
        '<source type="image/webp" srcset="%s" sizes="%s">'
        '<img src="/assets/img/%s.jpg" alt="%s"%s%s loading="%s"%s decoding="async">'
        '</picture>'
    ) % (avif, srcset, sizes, name, esc(alt),
         ' class="%s"' % cls if cls else "", style,
         "eager" if eager else "lazy",
         ' fetchpriority="high"' if eager else "")


def img_src(name, width=800):
    widths = _WIDTHS.get(name, [])
    pick = next((w for w in widths if w >= width), widths[-1] if widths else None)
    if pick is None:
        return "/assets/img/%s.jpg" % name
    return "/assets/img/%s-%d.webp" % (name, pick)


def img_full(name):
    widths = _WIDTHS.get(name, [])
    return img_src(name, widths[-1] if widths else 2000)


def abs_url(path):
    """Absolute URL for canonical / og tags."""
    return SITE_URL + (path if path.startswith("/") else "/" + path)


# --------------------------------------------------------------------------
# Text helpers
# --------------------------------------------------------------------------

def esc(s):
    return html.escape(s, quote=True)


_PREP = re.compile(r"(?<![\w&;])([aiksuovzAIKSUOVZ])\s+(?=\w)")


def nb(text):
    """Czech typography: bind one-letter prepositions to the following word."""
    return _PREP.sub(lambda m: m.group(1) + "\u00a0", text)


def photos_cz(n):
    """Czech plural: 1 fotografie, 2-4 fotografie, 5+ fotografií."""
    if n == 1:
        return "1 fotografie"
    if 2 <= n <= 4:
        return "%d fotografie" % n
    return "%d fotografií" % n


def paras(text):
    return "\n".join("<p>%s</p>" % nb(p.strip()) for p in text.split("\n\n") if p.strip())


ICONS = {
    "arrow": '<svg class="%s" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M2 8h11M9 4l4 4-4 4"/></svg>',
    "phone": '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M5.2 2.5 6.6 5 5.3 6.4a8 8 0 0 0 4.3 4.3L11 9.4l2.5 1.4-.5 2.4c-.1.5-.6.8-1.1.8A11 11 0 0 1 1.9 3.6c0-.5.3-1 .8-1.1l2.5-.5z"/></svg>',
    "clock": '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><circle cx="8" cy="8" r="6.2"/><path d="M8 4.4V8l2.4 1.5"/></svg>',
    "users": '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><circle cx="6" cy="5.2" r="2.6"/><path d="M1.6 13.4a4.6 4.6 0 0 1 8.8 0"/><path d="M10.8 3.1a2.6 2.6 0 0 1 0 4.9M12 9.4a4.6 4.6 0 0 1 2.4 4"/></svg>',
    "close": '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M3.5 3.5l9 9M12.5 3.5l-9 9"/></svg>',
    "prev": '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M10 3l-5 5 5 5"/></svg>',
    "next": '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M6 3l5 5-5 5"/></svg>',
    "caret": '<svg class="nav__caret" viewBox="0 0 10 10" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M2 4l3 3 3-3"/></svg>',
    "pin": '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M8 14.5S13 10 13 6.4a5 5 0 0 0-10 0C3 10 8 14.5 8 14.5z"/><circle cx="8" cy="6.3" r="1.9"/></svg>',
    "mail": '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><rect x="1.5" y="3.5" width="13" height="9" rx="1"/><path d="M1.9 4.2 8 8.7l6.1-4.5"/></svg>',
}


def icon(name, cls=""):
    svg = ICONS[name]
    return svg % cls if "%s" in svg else svg


def arrow(cls="btn__arrow"):
    return ICONS["arrow"] % cls


# --------------------------------------------------------------------------
# Chrome: head / header / footer
# --------------------------------------------------------------------------

FONTS = (
    # Self-hosted (tools/build_fonts.py) — no third-party request, and the two
    # faces above the fold can be preloaded.
    '<link rel="preload" href="/assets/fonts/fraunces-latin-ext-normal.woff2" '
    'as="font" type="font/woff2" crossorigin>'
    '<link rel="preload" href="/assets/fonts/instrument-sans-latin-ext-normal.woff2" '
    'as="font" type="font/woff2" crossorigin>'
)


def inline_css():
    """fonts.css + site.css as one inline <style>.

    Both stylesheets together gzip to ~12 kB; inlining them takes two
    render-blocking requests off the critical path, which on mobile was
    costing ~750 ms of FCP/LCP (PageSpeed). The .css files stay in
    assets/ as the editable source — pages just don't link them.
    """
    global _CSS
    if _CSS is None:
        css = ""
        for f in ("fonts.css", "site.css"):
            with open(os.path.join(ROOT, "assets", "css", f), encoding="utf-8") as fh:
                css += fh.read() + "\n"
        css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)   # comments
        css = re.sub(r"[ \t]+", " ", css)                 # runs of spaces
        css = re.sub(r"\n\s*", "\n", css)                 # indentation + blank lines
        _CSS = "<style>%s</style>" % css.strip()
    return _CSS


_CSS = None

FAVICON = (
    '<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">'
    '<link rel="icon" href="/assets/favicon-32.png" sizes="32x32">'
    '<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">'
)


def nav_items():
    return [
        ("O nás", "/o-nas/", "o-nas"),
        ("Nabídka", "/nabidka/", "nabidka"),
        ("Fotogalerie", "/fotogalerie/", "fotogalerie"),
        ("Spolupráce", "/spoluprace/", "spoluprace"),
        ("Kontakt", "/kontakt/", "kontakt"),
    ]


def header(active):
    mega = "".join(
        '<a class="mega__item" href="%s">'
        '<span class="mega__thumb">%s</span>'
        '<span class="mega__name">%s</span>'
        '<span class="mega__desc">%s</span></a>'
        % (o["url"],
           pic(o["cover"], o["name"], sizes="220px"),
           esc(o["name"]), nb(esc(o["teaser"])))
        for o in OFFERS
    )

    links = ""
    for label, href, key in nav_items():
        if key == "nabidka":
            links += (
                '<button class="nav__link%s" data-mega-toggle aria-expanded="false" '
                'aria-controls="mega">%s%s</button>'
                % (" is-current" if active in ("nabidka",) + tuple(o["slug"] for o in OFFERS)
                   or active in [s["slug"] for s in SHOWS] else "",
                   label, icon("caret"))
            )
        else:
            links += '<a class="nav__link%s" href="%s">%s</a>' % (
                " is-current" if active == key else "", href, label)

    drawer_offers = "".join(
        '<li><a href="%s">%s</a></li>' % (o["url"], esc(o["name"])) for o in OFFERS
    )

    return """
<header class="header">
  <div class="shell header__inner">
    <a class="brand" href="/" aria-label="Kvintána — domů">
      <span class="brand__mark">Kvint<em>á</em>na</span>
      <span class="brand__sub">Spolek historického jezdectví</span>
    </a>
    <nav class="nav" aria-label="Hlavní">{links}</nav>
    <a class="header__call" href="tel:{tel}">{ph}{phone}</a>
    <button class="burger" data-burger aria-expanded="false" aria-label="Menu" aria-controls="drawer">
      <span></span><span></span><span></span>
    </button>
  </div>
  <div class="mega" id="mega" data-mega>
    <div class="shell">
      <p class="label" style="margin-bottom:1.4rem">Co pro vás umíme</p>
      <div class="mega__grid">{mega}</div>
    </div>
  </div>
</header>

<div class="drawer" id="drawer" data-drawer>
  <nav aria-label="Mobilní">
    <ul class="drawer__list">
      <li><a href="/o-nas/"><span class="numeral">01</span>O nás</a></li>
      <li><a href="/nabidka/"><span class="numeral">02</span>Nabídka</a>
        <ul class="drawer__sub">{doffers}</ul>
      </li>
      <li><a href="/fotogalerie/"><span class="numeral">03</span>Fotogalerie</a></li>
      <li><a href="/spoluprace/"><span class="numeral">04</span>Spolupráce</a></li>
      <li><a href="/kontakt/"><span class="numeral">05</span>Kontakt</a></li>
    </ul>
    <div class="drawer__foot">
      <a class="btn" href="tel:{tel}">{ph}{phone}</a>
    </div>
  </nav>
</div>
""".format(links=links, mega=mega, doffers=drawer_offers,
           tel=SITE["phone_href"], phone=SITE["phone"], ph=icon("phone"))


def footer():
    offer_links = "".join(
        '<li><a href="%s">%s</a></li>' % (o["url"], esc(o["name"])) for o in OFFERS
    )
    show_links = "".join(
        '<li><a href="/predstaveni/%s/">%s</a></li>' % (s["slug"], esc(s["name"]))
        for s in SHOWS
    )
    return """
<footer class="footer">
  <div class="shell">
    <div class="footer__top">
      <div>
        <p class="footer__mark">Kvint<em>á</em>na</p>
        <p class="footer__blurb">Spolek historického jezdectví. Rytířské turnaje,
          ohnivá show, dragouni i filmová stafáž — přijedeme za vámi.</p>
        <p style="margin-top:1.6rem">
          <a class="tlink" href="tel:{tel}">{phone}</a>
        </p>
        <p style="margin-top:.5rem">
          <a class="tlink" href="mailto:{mail}">{mail}</a>
        </p>
      </div>
      <div>
        <p class="footer__h">Nabídka</p>
        <ul class="footer__list">{offers}</ul>
      </div>
      <div>
        <p class="footer__h">Představení</p>
        <ul class="footer__list">{shows}</ul>
      </div>
      <div>
        <p class="footer__h">Kvintána</p>
        <ul class="footer__list">
          <li><a href="/o-nas/">O nás</a></li>
          <li><a href="/fotogalerie/">Fotogalerie</a></li>
          <li><a href="/spoluprace/">Spolupráce</a></li>
          <li><a href="/kontakt/">Kontakt</a></li>
        </ul>
      </div>
    </div>
    <div class="footer__bottom">
      <span>© Kvintána — spolek historického jezdectví</span>
      <span>{addr} · <a href="{map_url}" target="_blank" rel="noopener">{gps}</a></span>
    </div>
  </div>
</footer>
""".format(offers=offer_links, shows=show_links, tel=SITE["phone_href"],
           phone=SITE["phone"], mail=SITE["email"],
           addr=esc(", ".join(SITE["address"][1:])), gps=esc(SITE["gps"]),
           map_url=SITE["map_url"])


LIGHTBOX = """
<div class="lbox" data-lightbox role="dialog" aria-modal="true" aria-hidden="true" aria-label="Fotografie">
  <figure class="lbox__fig">
    <img data-lb-img src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==" alt="">
    <figcaption class="lbox__cap" data-lb-cap></figcaption>
  </figure>
  <button class="lbox__btn lbox__prev" data-lb-prev aria-label="Předchozí">{prev}</button>
  <button class="lbox__btn lbox__next" data-lb-next aria-label="Další">{next}</button>
  <button class="lbox__btn lbox__close" data-lb-close aria-label="Zavřít">{close}</button>
  <span class="lbox__count" data-lb-count></span>
</div>
""".format(prev=icon("prev"), next=icon("next"), close=icon("close"))


PAGES = []          # (url, og_image) for sitemap.xml


def breadcrumb_ld(crumbs):
    """crumbs: [(name, url|None)] — last item is the current page."""
    items = []
    for i, (name, url) in enumerate(crumbs, 1):
        item = {"@type": "ListItem", "position": i, "name": name}
        if url:
            item["item"] = abs_url(url)
        items.append(item)
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": items}


def page(url, title, desc, body, active="", lightbox=False,
         og_image="g0-45", crumbs=None, jsonld=None, sitemap=True, out_path=None):
    """`url` is the public path: "" for the homepage, "kontakt/" otherwise."""
    canonical = abs_url("/" + url)
    og = SITE_URL + img_src(og_image, 1200)

    blocks = list(jsonld or [])
    if crumbs:
        blocks.append(breadcrumb_ld(crumbs))
    ld = "".join(
        '<script type="application/ld+json">%s\n</script>\n'
        % json.dumps(b, ensure_ascii=False, indent=1) for b in blocks)

    doc = """<!doctype html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#14100e">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Kvintána">
<meta property="og:locale" content="cs_CZ">
<meta property="og:url" content="{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{og}">
<meta name="twitter:card" content="summary_large_image">
{favicon}
{fonts}
{css}
<script>document.documentElement.className+=" js"</script>
{ld}</head>
<body>
<a class="skip" href="#main">Přeskočit na obsah</a>
{header}
<main id="main">
{body}
</main>
{footer}
{lightbox}
<script src="/assets/js/site.js" defer></script>
</body>
</html>
""".format(title=esc(title), desc=esc(desc), favicon=FAVICON, fonts=FONTS,
           css=inline_css(), canonical=canonical, og=og, ld=ld,
           header=header(active), body=body, footer=footer(),
           lightbox=LIGHTBOX if lightbox else "")

    # GitHub Pages requires the error page at /404.html, not /404/index.html
    write(out_path or (url + "index.html"), doc)
    if sitemap:
        PAGES.append(url)
    return "/" + url


def write(path, text):
    out = os.path.join(ROOT, path)
    d = os.path.dirname(out)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(text)


# --------------------------------------------------------------------------
# Reusable blocks
# --------------------------------------------------------------------------

def sec_head(label, title, note="", tag="h2", cls="h2"):
    note_html = '<p class="sec-head__note">%s</p>' % nb(note) if note else "<div></div>"
    return """
<div class="sec-head" data-reveal>
  <div>
    <p class="label">{label}</p>
    <{tag} class="sec-head__title {cls}">{title}</{tag}>
  </div>
  {note}
</div>""".format(label=esc(label), title=nb(title), note=note_html, tag=tag, cls=cls)


def phero(label, title, lead, image, crumbs):
    cr = "".join('<li>%s</li>' % c for c in crumbs)
    return """
<section class="phero">
  <div class="phero__media">{img}</div>
  <div class="phero__scrim"></div>
  <div class="shell">
    <ul class="crumbs">{cr}</ul>
    <h1 class="phero__title">{title}</h1>
    {lead}
  </div>
</section>""".format(
        img=pic(image, title, sizes="100vw", eager=True),
        cr=cr, title=nb(title),
        lead='<p class="phero__lead">%s</p>' % nb(lead) if lead else "")


def band(image="g1-3",
         title="Přijedeme za vámi",
         text="Napište nám termín a místo. Ozveme se s nabídkou programu, "
              "který na vaši akci sedne.",
         primary=("Nezávazná poptávka", "/kontakt/"),
         secondary=("Prohlédnout nabídku", "/nabidka/")):
    return """
<section class="band">
  <div class="band__media">{img}</div>
  <div class="band__scrim"></div>
  <div class="shell" data-reveal>
    <p class="label label--bare" style="justify-content:center;display:flex">Kvintána</p>
    <h2 class="band__title" style="margin-top:1rem">{title}</h2>
    <p class="lead" style="margin:1.2rem auto 0;text-align:center">{text}</p>
    <div class="cluster">
      <a class="btn" href="{p1}">{p0}{arr}</a>
      <a class="btn btn--ghost" href="{s1}">{s0}</a>
    </div>
  </div>
</section>""".format(img=pic(image, title, sizes="100vw"),
                     title=nb(title), text=nb(text),
                     p0=primary[0], p1=primary[1], s0=secondary[0], s1=secondary[1],
                     arr=arrow())


def show_card(s, cls="", sizes="(max-width:620px) 92vw, (max-width:900px) 46vw, 30vw"):
    return """
<a class="card {cls}" href="/predstaveni/{slug}/" data-reveal>
  <span class="card__media">{img}</span>
  <span class="card__body">
    <span class="label label--bare" style="font-size:.7rem">{kicker}</span>
    <span class="card__title" style="margin-top:.5rem">{name}</span>
    <span class="card__text">{teaser}</span>
    <span class="card__spec">{clock}{length}</span>
  </span>
</a>""".format(cls=cls, slug=s["slug"],
               img=pic(s["cover"], s["name"], sizes=sizes, ratio="4/3"),
               kicker=esc(s["kicker"]), name=nb(esc(s["name"])), teaser=nb(esc(s["teaser"])),
               clock=icon("clock"), length=esc(s["length"]))


def offer_index():
    """Numbered editorial list. Each row carries its own thumbnail so the
    imagery is visible without hovering (and works on touch)."""
    rows = ""
    for i, o in enumerate(OFFERS, 1):
        rows += """
<a class="index__row" href="{url}">
  <span class="numeral">{n:02d}</span>
  <span class="index__thumb">{img}</span>
  <span class="index__name">{name}</span>
  <span class="index__desc">{teaser}</span>
  <span class="index__go">{arr}</span>
</a>""".format(url=o["url"], n=i,
               img=pic(o["cover"], o["name"], sizes="160px", ratio="4/3"),
               name=nb(esc(o["name"])), teaser=nb(esc(o["teaser"])), arr=arrow(""))
    return '<div class="index index--thumbs" data-reveal>%s</div>' % rows


def gallery_grid(photos, group, captions=None):
    out = ""
    for i, p in enumerate(photos):
        cap = (captions or {}).get(p, "")
        out += """
<a class="gal__item" href="{full}" data-lb="{full}" data-lb-group="{g}" data-lb-cap="{cap}">
  {img}{caphtml}
</a>""".format(full=img_full(p), g=group, cap=esc(cap),
               img=pic(p, cap or "Kvintána", sizes="(max-width:620px) 92vw, (max-width:900px) 46vw, 31vw"),
               caphtml='<span class="gal__cap">%s</span>' % esc(cap) if cap else "")
    return '<div class="gal gal--tiles">%s</div>' % out


# --------------------------------------------------------------------------
# Pages
# --------------------------------------------------------------------------

def build_home():
    shows_html = "".join(show_card(s) for s in SHOWS)

    films_marquee = "".join(
        '<span class="marquee__item">%s</span>' % esc(f["title"]) for f in FILMS
    ) * 2

    teaser_photos = ["g5-32", "g2-6", "g6-23", "g1-2", "g16-54", "g0-45"]
    teaser = "".join(
        '<a class="gal__item" href="%s" data-lb="%s" data-lb-group="teaser">%s</a>'
        % (img_full(p), img_full(p), pic(p, "Kvintána", sizes="(max-width:900px) 46vw, 31vw"))
        for p in teaser_photos
    )

    # The hero counts mirror content.FACTS. "20+ let zkušeností" is the one
    # figure on this page the old site never stated — supplied by the club on
    # 28. 7. 2026, and the datum the readme used to list as missing.
    body = """
<section class="hero">
  <div class="hero__media">{heroimg}</div>
  <div class="hero__scrim"></div>
  <div class="shell hero__inner">
    <p class="label label--ember hero__label" data-reveal>Spolek historického jezdectví</p>
    <h1 class="hero__title" data-reveal style="--d:80ms">
      Kde historie <em>znovu</em> usedne na koně
    </h1>
    <p class="hero__sub" data-reveal style="--d:180ms">
      Rytířské turnaje, ohnivá show, dragouni Jeho Výsosti i filmová stafáž.
      Šest hotových programů, které přivezeme na váš hrad, do města i na náves.
    </p>
    <div class="cluster" data-reveal style="--d:260ms">
      <a class="btn" href="/predstaveni/">Prohlédnout představení{arr}</a>
      <a class="btn btn--ghost" href="/kontakt/">Nezávazná poptávka</a>
    </div>
    <div class="hero__meta" data-reveal style="--d:340ms">
      <span class="hero__stat"><span>představení</span><b>6</b></span>
      <span class="hero__stat"><span>filmů</span><b>9</b></span>
      <span class="hero__stat"><span>zkušeností</span><b>20+ let</b></span>
    </div>
  </div>
  <a class="hero__scroll" href="#o-nas">Posunout níž</a>
</section>

<section class="section" id="o-nas">
  <div class="shell">
    <div class="split split--offset">
      <div data-reveal>
        <p class="label">O nás</p>
        <h2 class="h2" style="margin:1.1rem 0 1.6rem">
          Láska ke&nbsp;koním, historii a&nbsp;přírodě
        </h2>
        <div class="prose prose--wide">
          <p>Jsme skromná parta lidí, jejíž jádro tvoří manželé Viktor a&nbsp;Tereza
          Fialovi. Spojuje nás láska ke&nbsp;koním, historii a&nbsp;přírodě.
          Tvůrčím způsobem se&nbsp;snažíme o&nbsp;propojení těchto náklonností.</p>
          <p>Věříme, že jsme vás už mnohokrát na&nbsp;svých cestách po&nbsp;hradech,
          městech a&nbsp;vesnicích rozesmáli i&nbsp;potěšili. Musíme jen doufat
          v&nbsp;to, že znovu odměníte každodenní usilovnou a&nbsp;pokornou dřinu
          nás a&nbsp;našich koní potleskem.</p>
        </div>
        <p style="margin-top:2rem"><a class="tlink" href="/o-nas/">Celý příběh spolku{arr2}</a></p>
      </div>
      <div data-reveal style="--d:120ms">
        <div class="duo">
          <figure class="duo__item">
            {viktor}
            <figcaption class="duo__cap">
              <span class="duo__name">Viktor Fiala</span>
              <span class="duo__role">instruktor</span>
            </figcaption>
          </figure>
          <figure class="duo__item">
            {tereza}
            <figcaption class="duo__cap">
              <span class="duo__name">Tereza Fialová</span>
              <span class="duo__role">spolek Kvintána</span>
            </figcaption>
          </figure>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="shell">{facts}</div>
</section>

<section class="section">
  <div class="shell">
    {head1}
    {index}
  </div>
</section>

<section class="section section--raise">
  <div class="shell">
    {head2}
    <div class="cards cards--stagger grid--3">{shows}</div>
    <p style="margin-top:2.5rem" data-reveal><a class="tlink" href="/predstaveni/">Všech šest představení{arr2}</a></p>
  </div>
</section>


<section class="section section--tight">
  <div class="shell" data-reveal>
    <p class="label" style="margin-bottom:1.5rem">Točili jsme s&nbsp;nimi</p>
  </div>
  <div class="marquee" data-reveal>
    <div class="marquee__track">{marquee}</div>
  </div>
  <div class="shell" style="margin-top:1.5rem" data-reveal>
    <a class="tlink" href="/filmy/">Filmografie a&nbsp;kaskadérské role{arr2}</a>
  </div>
</section>

<section class="section">
  <div class="shell">
    {head4}
    {teaser}
    <p style="margin-top:2.5rem" data-reveal><a class="tlink" href="/fotogalerie/">Otevřít fotogalerii{arr2}</a></p>
  </div>
</section>

{band}
""".format(
        heroimg=pic("g0-45", "Rytířský turnaj Kvintány pod hradbami hradu",
                    sizes="100vw", eager=True),
        viktor=pic("g3-51", "Viktor Fiala v dobové uniformě na koni",
                   sizes="(max-width:900px) 45vw, 22vw", ratio="3/4"),
        tereza=pic("g3-52", "Tereza Fialová v dobovém kostýmu",
                   sizes="(max-width:900px) 45vw, 22vw", ratio="3/4"),
        arr=arrow(), arr2=arrow("btn__arrow"),
        facts='<div class="facts" data-reveal>%s</div>' % "".join(
            '<div class="facts__item"><span class="facts__n">%s</span>'
            '<span class="facts__t">%s</span></div>' % (n, nb(esc(t))) for n, t in FACTS),
        head1=sec_head("Nabídka", "Co pro vás umíme",
                       "Od patnáctiminutového ohnivého čísla po vícedenní putování krajem. "
                       "Vyberte si, s čím máme přijet."),
        index=offer_index(),
        head2=sec_head("Představení", "Šest programů, které publikum baví",
                       "Vyberte si číslo, které se hodí na vaši akci — na náměstí, "
                       "na hradní nádvoří i na louku za vsí."),
        shows=shows_html,
        marquee=films_marquee,
        head4=sec_head("Fotogalerie", "Z našich cest",
                       "Fotografie z představení, natáčení i&nbsp;obyčejných dnů v sedle."),
        teaser='<div class="gal gal--tiles" data-reveal>%s</div>' % teaser,
        band=band(),
    )

    org = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "Kvintána",
        "alternateName": "Kvintána — spolek historického jezdectví",
        "url": SITE_URL + "/",
        "image": SITE_URL + img_src("g0-45", 1200),
        "telephone": SITE["phone"],
        "email": SITE["email"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": SITE["address"][1],
            "postalCode": "572 01",
            "addressLocality": "Polička",
            "addressCountry": "CZ",
        },
        "geo": {"@type": "GeoCoordinates",
                "latitude": SITE["lat"], "longitude": SITE["lon"]},
    }
    return page("",
                "Kvintána — spolek historického jezdectví",
                "Rytířské turnaje, ohnivá show, dragouni i filmová stafáž. "
                "Historická jezdecká vystoupení na hradech, ve městech a na vesnicích.",
                body, active="index", lightbox=True, jsonld=[org])


def build_about():
    roster = "".join(
        '<div class="roster__item"><p class="roster__name">%s</p>'
        '<p class="roster__role">kůň</p></div>' % esc(h) for h in HORSES
    )
    body = """
{phero}

<section class="section">
  <div class="shell">
    <div class="split">
      <div class="prose prose--wide prose--drop" data-reveal>
        <p>Jsme skromná parta lidí, jejíž jádro tvoří manželé Viktor a&nbsp;Tereza
        Fialovi. Spojuje nás láska ke&nbsp;koním, historii a&nbsp;přírodě. Tvůrčím
        způsobem se&nbsp;snažíme o&nbsp;propojení těchto náklonností, což by nám
        samo o&nbsp;sobě mohlo stačit k&nbsp;osobnímu uspokojení, ale stejně jako
        dobrý kuchař se&nbsp;musí podělit o&nbsp;své skvělé pokrmy a&nbsp;odměnou
        jsou mu spokojená břicha strávníků, tak i&nbsp;my máme neodbytná nutkání
        nabídnout vám to nejlepší z&nbsp;našeho soudku zábavy i&nbsp;umění
        a&nbsp;věříme, že jsme vás už mnohokrát na&nbsp;svých cestách
        po&nbsp;hradech, městech a&nbsp;vesnicích rozesmáli i&nbsp;potěšili.</p>
        <p>Musíme jen doufat v&nbsp;to, že znovu odměníte každodenní usilovnou
        a&nbsp;pokornou dřinu nás a&nbsp;našich koní potleskem.</p>
      </div>
      <div data-reveal style="--d:120ms">
        <div class="split__media">{img1}</div>
        <p class="split__cap">Detail zbroje — Rytíř Sysel z&nbsp;Holohlav</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--raise">
  <div class="shell">
    <div class="split split--flip">
      <div class="split__media" data-reveal>{img2}</div>
      <div data-reveal style="--d:120ms">
        <p class="label">Stáj</p>
        <h2 class="h2" style="margin:1.1rem 0 1.4rem">Koně, kteří znají oheň i&nbsp;dav</h2>
        <p class="prose">Naši koně znají salvy z&nbsp;mušket, kanonů
        i&nbsp;obyčejnou lidskou tlačenici. Ve&nbsp;stáji na&nbsp;vás čekají
        tihle:</p>
        <div class="roster" style="margin-top:2rem">{roster}</div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="split">
      <div data-reveal>
        <blockquote class="pull">
          „Vsaďte na&nbsp;koně, kteří prošli našima rukama.“
          <span class="pull__by">Kvintána</span>
        </blockquote>
      </div>
      <div class="prose" data-reveal style="--d:100ms">
        <p>Najdete nás v&nbsp;Širokém dole u&nbsp;Poličky. Vyjížďky vedeme
        v&nbsp;Lučicích, putování míří do&nbsp;Hostýnských vrchů a&nbsp;Moravské
        brány a&nbsp;s&nbsp;představeními jezdíme po&nbsp;hradech, městech
        a&nbsp;vesnicích.</p>
        <p>Pokud vás zajímá, s&nbsp;čím k&nbsp;vám můžeme přijet, začněte
        u&nbsp;nabídky. Pokud vás zajímá, jak to u&nbsp;nás vypadá, začněte
        u&nbsp;fotogalerie.</p>
        <p style="margin-top:1.6rem">
          <a class="tlink" href="/nabidka/">Nabídka{arr}</a>
        </p>
      </div>
    </div>
  </div>
</section>

{band}
""".format(
        phero=phero("O nás", "Jsme skromná parta lidí",
                    "Jádro spolku tvoří manželé Viktor a Tereza Fialovi. "
                    "Spojuje nás láska ke koním, historii a přírodě.",
                    "g5-31", ['<a href="/">Domů</a>', "O nás"]),
        img1=pic("g5-32", "Rytíř v plné zbroji", sizes="(max-width:900px) 92vw, 45vw",
                 ratio="4/3", pos="center 18%"),
        img2=pic("g6-21", "Koně pod stromem na pastvině", sizes="(max-width:900px) 92vw, 45vw", ratio="4/3"),
        roster=roster, arr=arrow(), band=band(image="g6-18"),
    )
    return page("o-nas/", "O nás — Kvintána",
                "Jádro spolku tvoří manželé Viktor a Tereza Fialovi. "
                "Spojuje nás láska ke koním, historii a přírodě.",
                body, active="o-nas", og_image="g5-31",
                crumbs=[("Domů", "/"), ("O nás", None)])


def build_nabidka():
    cards = "".join("""
<a class="card" href="{url}" data-reveal>
  <span class="card__media">{img}</span>
  <span class="card__body">
    <span class="numeral">{n:02d}</span>
    <span class="card__title" style="margin-top:.4rem">{name}</span>
    <span class="card__text">{teaser}</span>
  </span>
</a>""".format(url=o["url"], n=i,
                img=pic(o["cover"], o["name"],
                        sizes="(max-width:620px) 92vw, (max-width:900px) 46vw, 30vw", ratio="4/3"),
                name=nb(esc(o["name"])), teaser=nb(esc(o["teaser"])))
        for i, o in enumerate(OFFERS, 1))

    body = """
{phero}
<section class="section">
  <div class="shell">
    <div class="cards grid--3">{cards}</div>
  </div>
</section>
{band}
""".format(
        phero=phero("Nabídka", "Sedm způsobů, jak si nás pozvat",
                    "Od patnáctiminutového ohnivého čísla po vícedenní putování krajem "
                    "nebo koně před filmovou kamerou.",
                    "g0-45", ['<a href="/">Domů</a>', "Nabídka"]),
        cards=cards, band=band(image="g3-48"))
    return page("nabidka/", "Nabídka — Kvintána",
                "Představení, putování, vyjížďky, jezdecké kurzy, školní výlety, "
                "filmy a přeprava koní.", body, active="nabidka", og_image="g0-45",
                crumbs=[("Domů", "/"), ("Nabídka", None)])


def build_predstaveni_index():
    cards = "".join(show_card(s) for s in SHOWS)
    body = """
{phero}
<section class="section">
  <div class="shell">
    {head}
    <div class="cards grid--3">{cards}</div>
  </div>
</section>

<section class="section section--raise">
  <div class="shell">
    <div class="split">
      <div data-reveal>
        <p class="label">Jak to probíhá</p>
        <h2 class="h2" style="margin:1.1rem 0 1.4rem">Od telefonu po&nbsp;potlesk</h2>
      </div>
      <div class="prose" data-reveal style="--d:100ms">
        <p><strong>1 — Ozvěte se.</strong> Napište nebo zavolejte termín, místo
        a&nbsp;koho chcete pobavit.</p>
        <p><strong>2 — Domluvíme detaily.</strong> Vyberete si číslo z&nbsp;nabídky,
        nebo poradíme. Zbytek — plochu, čas i&nbsp;cenu — doladíme společně.</p>
        <p><strong>3 — Přijedeme.</strong> Vlastními vozy, s&nbsp;vlastními koňmi.</p>
        <p style="margin-top:1.6rem"><a class="tlink" href="/kontakt/">Nezávazná poptávka{arr}</a></p>
      </div>
    </div>
  </div>
</section>
{band}
""".format(
        phero=phero("Představení", "Šest programů, které publikum baví",
                    "Rytířské turnaje, ohnivá show, dragouni Jeho Výsosti i komedie "
                    "o manželské rozepři řešené dřevcem.",
                    "g4-68", ['<a href="/">Domů</a>',
                              '<a href="/nabidka/">Nabídka</a>', "Představení"]),
        head=sec_head("Program", "Vyberte si číslo",
                      "U každého najdete obsazení, délku a fotografie z odehraných akcí."),
        cards=cards, arr=arrow(), band=band(image="g1-4"))
    return page("predstaveni/", "Představení — Kvintána",
                "Oheň a kůň, Partie krásného dragouna, Vivat Maria Theresia, "
                "Rytířské turnaje, Rytíř Sysel z Holohlav, průvody a bitvy.",
                body, active="predstaveni", og_image="g4-68",
                crumbs=[("Domů", "/"), ("Nabídka", "/nabidka/"), ("Představení", None)])


def build_show(s, prev, nxt):
    # Only render specs the source site actually states.
    items = [(k, v) for k, v in
             (("Obsazení", s["cast"]), ("Délka", s["length"])) if v]
    items.append(("Doprava", "Vlastní vozy a přívěsy"))
    spec = '<div class="stats">%s</div>' % "".join(
        '<span class="stats__i"><span>%s</span><b>%s</b></span>' % (esc(k), nb(esc(v)))
        for k, v in items)

    pager = """
<section class="shell">
  <div class="pager">
    <a class="pager__a" href="/predstaveni/{ps}/">
      <span class="label label--bare">Předchozí</span>
      <span class="pager__t">{pn}</span>
    </a>
    <a class="pager__a" href="/predstaveni/{ns}/">
      <span class="label label--bare" style="justify-content:flex-end">Další</span>
      <span class="pager__t">{nn}</span>
    </a>
  </div>
</section>""".format(ps=prev["slug"], pn=nb(esc(prev["name"])),
                     ns=nxt["slug"], nn=nb(esc(nxt["name"])))

    body = """
{phero}

<section class="section">
  <div class="shell">
    <div class="split split--rail">
      <div data-reveal>
        <div class="prose prose--wide prose--drop">{text}</div>
        {spec}
      </div>
      <div class="rail" data-reveal style="--d:100ms">
        <div class="rail__box">
          <p class="label label--ember">Poptávka</p>
          <p class="rail__price" style="margin:.9rem 0 .5rem">Chcete tohle číslo?</p>
          <p style="font-size:var(--t-sm);color:var(--bone-mute)">
            Napište nám termín a&nbsp;místo. Ozveme se&nbsp;s&nbsp;nabídkou.
          </p>
          <p style="margin-top:1.3rem">
            <a class="btn" href="/kontakt/?show={slug}" style="width:100%;justify-content:center">Poptat představení{arr}</a>
          </p>
          <p style="margin-top:.8rem">
            <a class="btn btn--ghost" href="tel:{tel}" style="width:100%;justify-content:center">{ph}{phone}</a>
          </p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--raise">
  <div class="shell">
    {head}
    {gal}
  </div>
</section>

{pager}
{band}
""".format(
        phero=phero(s["kicker"], s["name"], s["teaser"], s["hero"],
                    ['<a href="/">Domů</a>',
                     '<a href="/predstaveni/">Představení</a>',
                     esc(s["name"])]),
        text=paras(s["text"]), slug=s["slug"], arr=arrow(),
        tel=SITE["phone_href"], phone=SITE["phone"], ph=icon("phone"),
        spec=spec,
        head=sec_head("Fotogalerie", "Z odehraných akcí", "Klikněte pro zvětšení."),
        gal=gallery_grid(s["photos"], s["slug"],
                         captions={p: s["name"] for p in s["photos"]}),
        pager=pager,
        band=band(image=s["photos"][-1],
                  primary=("Nezávazná poptávka", "/kontakt/"),
                  secondary=("Další představení", "/predstaveni/")),
    )
    return page("predstaveni/%s/" % s["slug"],
                "%s — Kvintána" % s["name"], s["teaser"],
                body, active=s["slug"], lightbox=True,
                og_image=s["cover"],
                crumbs=[("Domů", "/"), ("Představení", "/predstaveni/"),
                        (s["name"], None)])


def simple_offer(slug, url, label, title, lead, hero, prose, extra="", gallery=None,
                 gallery_head=None, band_img=None, meta=None):
    gal = ""
    if gallery:
        gal = """
<section class="section section--raise">
  <div class="shell">
    {head}
    {grid}
  </div>
</section>""".format(head=sec_head(*(gallery_head or ("Fotogalerie", "Jak to u nás vypadá", ""))),
                     grid=gallery_grid(gallery, slug, captions={p: title for p in gallery}))

    meta_html = ""
    if meta:
        rows = "".join(
            '<div class="spec__row"><span class="spec__k">%s</span>'
            '<span class="spec__v">%s</span></div>' % (esc(k), nb(v)) for k, v in meta)
        meta_html = '<div class="spec" style="margin-top:1.5rem">%s</div>' % rows

    body = """
{phero}
<section class="section">
  <div class="shell">
    <div class="split split--rail">
      <div data-reveal>
        <div class="prose prose--wide prose--drop">{prose}</div>
        {extra}
      </div>
      <div class="rail" data-reveal style="--d:100ms">
        <div class="rail__box">
          <p class="label label--ember">Máte zájem?</p>
          <p class="rail__price" style="margin:.9rem 0 .5rem">{title}</p>
          <p style="font-size:var(--t-sm);color:var(--bone-mute)">
            Zavolejte nebo napište. Domluvíme termín i&nbsp;rozsah.
          </p>
          <p style="margin-top:1.3rem">
            <a class="btn" href="/kontakt/?show={slug}" style="width:100%;justify-content:center">Nezávazná poptávka{arr}</a>
          </p>
          <p style="margin-top:.8rem">
            <a class="btn btn--ghost" href="tel:{tel}" style="width:100%;justify-content:center">{ph}{phone}</a>
          </p>
        </div>
        {meta}
      </div>
    </div>
  </div>
</section>
{gal}
{band}
""".format(
        phero=phero(label, title, lead, hero,
                    ['<a href="/">Domů</a>',
                     '<a href="/nabidka/">Nabídka</a>', esc(title)]),
        prose=prose, extra=extra, title=nb(esc(title)), slug=slug, arr=arrow(),
        tel=SITE["phone_href"], phone=SITE["phone"], ph=icon("phone"),
        meta=meta_html, gal=gal, band=band(image=band_img or hero))
    return page(url.strip("/") + "/", "%s — Kvintána" % title, lead, body,
                active=slug, lightbox=bool(gallery), og_image=hero,
                crumbs=[("Domů", "/"), ("Nabídka", "/nabidka/"), (title, None)])


def build_offers():
    out = []

    # --- Putování ---------------------------------------------------------
    out.append(simple_offer(
        "putovani", "putovani/", "Nabídka", "Putování",
        "Vícedenní jízdy krajem po stopách dávných kupeckých karavan.",
        "g6-18",
        paras(
            "Poznejte na vlastní kůži putování krajem v sedle ušlechtilých zvířat "
            "a projděte se po stopách dávných kupeckých karavan Jantarovou stezkou "
            "a Moravskou bránou, vyjeďte na úbočí Hostýnských a Veřovických vrchů, "
            "jež se svírají ve věčném objetí.\n\n"
            "Pohlédněte až k Lysé hoře na východě, Pradědu na severu či na západ "
            "k temné hradbě Českomoravské vrchoviny. Přebroďte s námi divokou Odru "
            "nebo líbivou Bečvu, abyste pak mohli spočinout ve voňavé trávě pod "
            "mléčnou dráhou, v malebném hostinci posnídat domácí omeletu či nalézt "
            "bezpečí pod hradbami rozeklaného Starého Jičína nebo pevnosti Helfštýn."
        ),
        gallery=["g6-18", "g6-19", "g6-20", "g6-21", "g6-22", "g6-23", "g6-24", "g6-25", "g6-26"],
        gallery_head=("Fotogalerie", "Fotografie z putování", "Klikněte pro zvětšení."),
        meta=[("Kde", "Jantarová stezka, Moravská brána, Hostýnské a&nbsp;Veřovické vrchy"),
              ("Výhledy", "Lysá hora, Praděd, Českomoravská vrchovina"),
              ("Brody", "Odra a&nbsp;Bečva"),
              ("Zastávky", "Starý Jičín, Helfštýn")],
        band_img="g6-22"))

    # --- Vyjížďky ---------------------------------------------------------
    horses = " · ".join(HORSES)
    out.append(simple_offer(
        "vyjizdky", "vyjizdky/", "Nabídka", "Vyjížďky",
        "Do sedla pod vedením zkušeného instruktora.",
        "g6-23",
        paras("Přijeďte za námi do Lučic, kde na vás v maštali čekají naši krásní "
              "koníci Šeila, Lady Lucky, Rainy, Pretty Woman, Amanda a zkušený "
              "instruktor Viktor Fiala."),
        extra="""
<div class="roster" style="margin-top:2.5rem" data-reveal>%s</div>""" % "".join(
            '<div class="roster__item"><p class="roster__name">%s</p>'
            '<p class="roster__role">kůň</p></div>' % esc(h) for h in HORSES),
        meta=[("Instruktor", "Viktor Fiala"),
              ("Koně", horses),
              ("Kde", "Lučice")],
        band_img="g6-24"))

    # --- Jezdecké kurzy ---------------------------------------------------
    out.append(simple_offer(
        "jezdecke-kurzy", "jezdecke-kurzy/", "Nabídka", "Jezdecké kurzy",
        "Vícedenní výcvikové pobyty pro školky, školy, firmy i skupiny.",
        "g6-26",
        paras("Organizujeme vícedenní výcvikové pobyty pro školky, školy, firmy "
              "či různé skupiny osob s možností stravování i ubytování v blízkém "
              "okolí či turisticky atraktivním prostředí Hostýnských vrchů."),
        meta=[("Pro koho", "Školky, školy, firmy i&nbsp;skupiny osob"),
              ("Délka", "Vícedenní pobyt"),
              ("Zázemí", "Stravování i&nbsp;ubytování v&nbsp;blízkém okolí"),
              ("Prostředí", "Hostýnské vrchy")],
        band_img="g6-21"))

    # --- Školní výlety ----------------------------------------------------
    out.append(simple_offer(
        "skolni-vylety", "skolni-vylety/", "Nabídka", "Školní výlety",
        "Historie, kterou si děti můžou osahat.",
        "g21-66",
        paras(
            "Školní výlety jsou samostatnou částí naší nabídky — fotografie níž "
            "jsou z několika z nich.\n\n"
            "Podobu programu domluvíme předem: co děti uvidí, na co si budou moct "
            "sáhnout a jak dlouho to bude trvat. Napište nám, kolik dětí a jakého "
            "věku přivedete a kam máme přijet."
        ),
        gallery=["g21-66", "g21-67"],
        gallery_head=("Fotogalerie", "Z výletů", "Klikněte pro zvětšení."),
        meta=None,
        band_img="g21-67"))

    # --- Filmy ------------------------------------------------------------
    film_rows = "".join("""
<a class="index__row" href="%s" %s>
  <span class="numeral">%02d</span>
  <span class="index__name">%s</span>
  <span class="index__desc">%s</span>
  <span class="index__go">%s</span>
</a>""" % ("/fotogalerie/#" + f["title"].lower().replace(" ", "-") if f["photos"] else "/fotogalerie/",
           "",
           i, nb(esc(f["title"])),
           "%s v galerii" % photos_cz(len(f["photos"])) if f["photos"] else "Bez fotografií",
           arrow(""))
        for i, f in enumerate(FILMS, 1))

    out.append(simple_offer(
        "filmy", "/filmy/", "Nabídka", "Filmy",
        "Perfektně vycvičené koně i jezdce do kaskadérských i komparsových rolí.",
        "g16-54",
        paras("Nabízíme perfektně vycvičené koně i jezdce do kaskadérských "
              "i komparsových rolí. Mohli jste nás vidět v těchto filmech:"),
        extra="""
<div style="margin-top:3rem" data-reveal>
  <p class="label" style="margin-bottom:1.5rem">Filmografie</p>
  <div class="index index--sm">%s</div>
</div>""" % film_rows,
        gallery=["g16-54", "g8-63", "g9-62", "g15-58", "g13-61", "g16-53",
                  "g15-56", "g15-57", "g8-65", "g15-59", "g16-55", "g15-60"],
        gallery_head=("Fotogalerie", "Z natáčení", "Klikněte pro zvětšení."),
        meta=[("Nabízíme", "Koně i&nbsp;jezdce, kaskadérské a&nbsp;komparsové role"),
              ("Koně znají", "Salvy z&nbsp;mušket, kanony i&nbsp;lidskou tlačenici"),
              ("Doprava", "Vlastní vozy a&nbsp;přívěsy"),
              ("Filmů", "9")],
        band_img="g8-63"))

    # --- Přeprava koní ----------------------------------------------------
    out.append(simple_offer(
        "preprava-koni", "preprava-koni/", "Nabídka", "Přeprava koní",
        "Vozy a přívěsy — pro vaše koně i k zapůjčení.",
        "g5-27",
        paras("Dopravu zajišťujeme vozy Nissan Terrano, Nissan Pathfinder "
              "a přívěsy Autovia."),
        extra="""
<div style="margin-top:2.5rem" data-reveal>
  <p class="label" style="margin-bottom:1.2rem">Možnost zapůjčení</p>
  <div class="spec">
    <div class="spec__row"><span class="spec__k">01</span><span class="spec__v">2&nbsp;ks přívěsu pro pár koní</span></div>
    <div class="spec__row"><span class="spec__k">02</span><span class="spec__v">Vozík sklápěcí, nosnost 3&nbsp;t</span></div>
    <div class="spec__row"><span class="spec__k">03</span><span class="spec__v">Vozík celolaminátový, možnost uzamčení nákladu</span></div>
  </div>
</div>""",
        meta=[("Vozy", "Nissan Terrano, Nissan Pathfinder"),
              ("Přívěsy", "Autovia"),
              ("Zapůjčení", "Přívěsy i&nbsp;vozíky")],
        band_img="g5-27"))

    return out


def build_gallery():
    chips = "".join(
        '<button class="chip%s" type="button" data-filter-val="%s" '
        'aria-pressed="%s">%s</button>'
        % (" is-current" if k == "all" else "", k,
           "true" if k == "all" else "false", esc(label))
        for k, label in GALLERY_CATS)

    tiles = ""
    for a in ALBUMS:
        photos = "".join(
            '<a class="sr" href="%s" data-lb="%s" data-lb-group="%s" data-lb-cap="%s" '
            'tabindex="-1" aria-hidden="true">%s</a>'
            % (img_full(p), img_full(p), a["slug"], esc(a["name"]), esc(a["name"]))
            for p in a["photos"][1:])
        tiles += """
<div data-album="{cat}" id="{slug}">
  <a class="album" href="{full}" data-lb="{full}" data-lb-group="{slug}" data-lb-cap="{name}">
    {img}
    <span class="album__body">
      <span class="album__title">{name}</span>
      <span class="album__count">{n}</span>
    </span>
  </a>
  {rest}
</div>""".format(cat=a["cat"], slug=a["slug"], full=img_full(a["photos"][0]),
                 img=pic(a["photos"][0], a["name"],
                         sizes="(max-width:620px) 92vw, (max-width:900px) 46vw, 31vw"),
                 name=nb(esc(a["name"])), n=photos_cz(len(a["photos"])), rest=photos)

    body = """
{phero}
<section class="section">
  <div class="shell">
    {head}
    <div class="cluster" data-filter data-reveal style="margin-bottom:2.5rem">{chips}</div>
    <div class="albums">{tiles}</div>
  </div>
</section>
{band}
""".format(
        phero=phero("Fotogalerie", "Třináct alb z cest",
                    "Fotografie z představení, natáčení i obyčejných dnů v sedle.",
                    "g0-45", ['<a href="/">Domů</a>', "Fotogalerie"]),
        head=sec_head("Alba", "Vyberte si", "Klikněte na album a listujte šipkami."),
        chips=chips, tiles=tiles, band=band(image="g4-68"))
    return page("fotogalerie/", "Fotogalerie — Kvintána",
                "Fotografie z historických jezdeckých představení, natáčení filmů "
                "a putování krajem.", body, active="fotogalerie", lightbox=True, og_image="g0-45",
                crumbs=[("Domů", "/"), ("Fotogalerie", None)])


def build_kontakt():
    prog_opts = "".join('<option value="%s">%s</option>' % (s["slug"], esc(s["name"]))
                        for s in SHOWS)
    prog_opts += "".join('<option value="%s">%s</option>' % (o["slug"], esc(o["name"]))
                         for o in OFFERS if o["slug"] != "predstaveni")

    body = """
{phero}

<section class="section">
  <div class="shell">
    <div class="split split--rail">
      <div data-reveal>
        <p class="label">Napište nám</p>
        <h2 class="h2" style="margin:1.1rem 0 1.6rem">Nezávazná poptávka</h2>
        <p class="prose" style="margin-bottom:2.5rem">Řekněte nám termín, místo
        a&nbsp;koho chcete pobavit. Ozveme se&nbsp;s&nbsp;návrhem programu i&nbsp;cenou.</p>

        <form class="form" data-form action="{formspree}" method="POST" novalidate>
          <div class="form__row">
            <p class="sr" aria-hidden="true">
            <label>Nechte prázdné<input type="text" name="_gotcha" tabindex="-1" autocomplete="off"></label>
          </p>
          <div class="field"><label for="f-name">Jméno a&nbsp;příjmení</label>
              <input id="f-name" name="name" type="text" required placeholder="Jan Novák"></div>
            <div class="field"><label for="f-org">Pořadatel / organizace</label>
              <input id="f-org" name="org" type="text" placeholder="Město, hrad, škola…"></div>
          </div>
          <div class="form__row">
            <div class="field"><label for="f-mail">E-mail</label>
              <input id="f-mail" name="email" type="email" required placeholder="jan@example.cz"></div>
            <div class="field"><label for="f-tel">Telefon</label>
              <input id="f-tel" name="tel" type="tel" placeholder="+420 000 000 000"></div>
          </div>
          <div class="form__row">
            <div class="field"><label for="f-date">Termín akce</label>
              <input id="f-date" name="date" type="text" inputmode="numeric"
                     placeholder="17. 5. 2026" pattern="\\s*\\d{{1,2}}\\.\\s*\\d{{1,2}}\\.\\s*\\d{{4}}\\s*"
                     title="Zadejte datum ve tvaru 17. 5. 2026"></div>
            <div class="field"><label for="f-place">Místo</label>
              <input id="f-place" name="place" type="text" placeholder="Hrad Starý Jičín"></div>
          </div>
          <div class="field"><label for="f-prog">O&nbsp;co máte zájem</label>
            <select id="f-prog" name="program">
              <option value="">Poradíte nám</option>
              {opts}
            </select>
          </div>
          <div class="field"><label for="f-msg">Zpráva</label>
            <textarea id="f-msg" name="message" placeholder="Kolik čekáte diváků, jaká je plocha, kdy má vystoupení začít…"></textarea>
          </div>
          <div class="form__ok" data-form-ok>
            <strong>Děkujeme, poptávka odešla.</strong> Ozveme se&nbsp;vám na&nbsp;uvedený
            kontakt. Spěchá to? Zavolejte na&nbsp;{phone}.
          </div>
          <div class="form__err" data-form-err>
            <strong>Odeslání se&nbsp;nepovedlo.</strong> Zkuste to prosím znovu, nebo nám
            rovnou zavolejte na&nbsp;{phone}, případně napište na&nbsp;{mail}.
          </div>
          <div class="cluster" style="margin-top:.5rem">
            <button class="btn" type="submit">Odeslat poptávku{arr}</button>

          </div>
        </form>
      </div>

      <div class="rail" data-reveal style="--d:100ms">
        <div class="rail__box">
          <p class="label label--ember">Zavolejte nám</p>
          <p style="margin:.9rem 0 1.4rem">
            <a class="tlink" href="tel:{tel}" style="font-size:var(--t-lg);font-family:var(--display)">{phone}</a>
          </p>
          <p class="label label--bare" style="margin-bottom:.5rem">Viktor Fiala</p>
          <p style="font-size:var(--t-sm);color:var(--bone-mute)">
            <a class="tlink" href="mailto:{mail}">{mail}</a>
          </p>
        </div>

        <div class="spec" style="margin-top:1.5rem">
          <div class="spec__row"><span class="spec__k">Adresa</span>
            <span class="spec__v">{addr}</span></div>
          <div class="spec__row"><span class="spec__k">GPS</span>
            <span class="spec__v"><a class="tlink" href="{map_url}" target="_blank" rel="noopener">{gps}</a></span></div>

        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="shell" data-reveal>
    <p class="label" style="margin-bottom:1.4rem">Kde nás najdete</p>
    <a class="map" href="{map_url}" target="_blank" rel="noopener"
       aria-label="Otevřít adresu v Google Mapách">
      {mapimg}
    </a>
    <p class="map__foot">
      <a class="tlink" href="{map_url}" target="_blank" rel="noopener">Otevřít v&nbsp;Google Mapách{arr2}</a>
      <span class="form__note">Podklad mapy © přispěvatelé OpenStreetMap</span>
    </p>
  </div>
</section>
""".format(
        phero=phero("Kontakt", "Ozvěte se",
                    "Nejrychleji nás zastihnete na telefonu. Poptávku můžete poslat "
                    "i formulářem níž.",
                    "g6-18", ['<a href="/">Domů</a>', "Kontakt"]),
        opts=prog_opts, arr=arrow(), formspree=FORMSPREE,
        tel=SITE["phone_href"], phone=SITE["phone"],
        mail=SITE["email"], addr="<br>".join(esc(x) for x in SITE["address"]),
        gps=esc(SITE["gps"]), arr2=arrow("btn__arrow"),
        map_url=SITE["map_url"],
        mapimg=pic("map-siroky-dul", "Mapa okolí — Široký důl u Poličky", sizes="100vw"))
    return page("kontakt/", "Kontakt — Kvintána",
                "Viktor Fiala, +420 737 179 811, jizda@centrum.cz. "
                "Široký důl 5, 572 01 Polička.", body, active="kontakt", og_image="g6-18",
                crumbs=[("Domů", "/"), ("Kontakt", None)])


def build_spoluprace():
    rows = "".join("""
<a class="partner" href="{url}" target="_blank" rel="noopener" data-reveal>
  <span class="numeral">{n:02d}</span>
  <span>
    <span class="partner__name">{name}</span>
    {note}
  </span>
  <span class="partner__host">{host} ↗</span>
</a>""".format(url=p["url"], n=i, name=nb(esc(p["name"])), host=esc(p["host"]),
                note='<span class="partner__note">%s</span>' % nb(esc(p["note"]))
                if p["note"] else "")
        for i, p in enumerate(PARTNERS, 1))

    body = """
{phero}
<section class="section">
  <div class="shell">
    {head}
    <div>{rows}</div>
  </div>
</section>
{band}
""".format(
        phero=phero("Spolupráce", "Lidé a místa, bez kterých by to nešlo",
                    "Fotografové, hrady, agentury a spolky, se kterými se potkáváme "
                    "sezónu co sezónu.",
                    "g2-6", ['<a href="/">Domů</a>', "Spolupráce"]),
        head=sec_head("Partneři", "Doporučujeme",
                      "Odkazy vedou na weby partnerů."),
        rows=rows, band=band(image="g4-42"))
    return page("spoluprace/", "Spolupráce — Kvintána",
                "Partneři spolku Kvintána — fotografové, hrady, agentury a spolky.",
                body, active="spoluprace", og_image="g2-6",
                crumbs=[("Domů", "/"), ("Spolupráce", None)])


# --------------------------------------------------------------------------

REDIRECT_TPL = """<!doctype html>
<html lang="cs">
<head>
<meta charset="utf-8">
<title>Přesměrování — Kvintána</title>
<link rel="canonical" href="{target_abs}">
<meta name="robots" content="noindex, follow">
<meta http-equiv="refresh" content="0; url={target}">
<script>location.replace({target_js});</script>
</head>
<body style="background:#14100e;color:#ede3d4;font-family:system-ui,sans-serif;padding:3rem">
<p>Stránka se přesunula. <a href="{target}" style="color:#e86a32">Pokračovat na {target}</a></p>
</body>
</html>
"""


def build_redirects():
    """Old Nette URLs -> new paths. Pages cannot 301, so these are canonical
    + instant-meta-refresh stubs."""
    for src, target in sorted(REDIRECTS.items()):
        write(src.strip("/") + "/index.html", REDIRECT_TPL.format(
            target=target,
            target_abs=abs_url(target.split("#")[0]),
            target_js=json.dumps(target)))
    return len(REDIRECTS)


def build_sitemap():
    urls = "".join(
        "  <url><loc>%s</loc></url>\n" % abs_url("/" + u) for u in sorted(set(PAGES)))
    write("sitemap.xml",
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + urls + "</urlset>\n")
    write("robots.txt",
          "User-agent: *\nAllow: /\n\nSitemap: %s\n" % abs_url("/sitemap.xml"))
    return len(set(PAGES))


def build_404():
    links = "".join(
        '<a class="index__row" href="%s">'
        '<span class="numeral">%02d</span>'
        '<span class="index__thumb">%s</span>'
        '<span class="index__name">%s</span>'
        '<span class="index__desc">%s</span>'
        '<span class="index__go">%s</span></a>'
        % (o["url"], i, pic(o["cover"], o["name"], sizes="160px", ratio="4/3"),
           nb(esc(o["name"])), nb(esc(o["teaser"])), arrow(""))
        for i, o in enumerate(OFFERS[:3], 1))

    body = """
<section class="phero phero--404">
  <div class="phero__media">{img}</div>
  <div class="phero__scrim"></div>
  <div class="shell">
    <p class="label label--bare">Chyba 404</p>
    <h1 class="phero__title">Tady už kůň nedojede</h1>
    <p class="phero__lead">Stránka, kterou hledáte, se buď přejmenovala, nebo se
    splašila a utekla. Zkuste se vrátit na začátek cesty.</p>
    <div class="cluster" style="margin-top:2rem">
      <a class="btn" href="/">Zpátky domů{arr}</a>
      <a class="btn btn--ghost" href="/kontakt/">Napsat nám</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="shell">
    {head}
    <div class="index index--thumbs">{links}</div>
  </div>
</section>
""".format(img=pic("g16-54", "Jezdci mizící v mlze", sizes="100vw", eager=True),
           arr=arrow(), links=links,
           head=sec_head("Kam dál", "Nebo si vyberte odsud",
                         "Nejčastější cíle na webu Kvintány."))
    return page("404/", "Stránka nenalezena — Kvintána",
                "Tady už kůň nedojede — stránka neexistuje.",
                body, og_image="g16-54", sitemap=False, out_path="404.html")


def main():
    scan_images()
    built = []
    built.append(build_home())
    built.append(build_about())
    built.append(build_nabidka())
    built.append(build_predstaveni_index())
    for i, s in enumerate(SHOWS):
        built.append(build_show(s, SHOWS[i - 1], SHOWS[(i + 1) % len(SHOWS)]))
    built += build_offers()
    built.append(build_gallery())
    built.append(build_kontakt())
    built.append(build_spoluprace())
    built.append(build_404())

    n_red = build_redirects()
    n_map = build_sitemap()

    print("Built %d pages, %d redirect stubs, sitemap with %d urls:"
          % (len(built), n_red, n_map))
    for b in built:
        print("  " + b)


if __name__ == "__main__":
    main()
