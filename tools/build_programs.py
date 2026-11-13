#!/usr/bin/env python3
"""Builds the product pages in /programs from the data in tools/programs.json.

Edit tools/programs.json, then run:
    python3 tools/build_programs.py
No dependencies beyond Python 3.
"""
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "tools" / "programs.json").read_text(encoding="utf-8"))
OUT = ROOT / "programs"
# Version stamp for the stylesheet and script, so browsers fetch the new files after every change.
import hashlib, re
VER = hashlib.sha1((ROOT / "assets/css/styles.css").read_bytes() + (ROOT / "assets/js/main.js").read_bytes()).hexdigest()[:8]
# Audits and the 1:1 have a real process to explain; guidebooks don't.
HAS_HOW = {"cv-audit", "linkedin-audit", "one-on-one"}

CHECK_LIGHT = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#4C6A51" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12l5 5 9-10"/></svg>'
CHECK_DARK = CHECK_LIGHT.replace("#4C6A51", "#F5DCCB")
LOCK = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg>'
BOLT = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M13 2L4 14h7l-1 8 9-12h-7z"/></svg>'


def e(s):
    return escape(s, quote=True)


def checks(items, icon, indent="          "):
    return "\n".join(f'{indent}<div class="check">{icon}<span>{e(t)}</span></div>' for t in items)


def access_label(slug):
    if slug == "one-on-one":
        return "1 hour on Google Meet"
    if slug in HAS_HOW:
        return "Report in 3 working days"
    return "Instant access by email"


def page(slug, p):
    plain_title = f'{p["t1"]} {p["t2"]}'
    badge = f'<span class="badge">{e(p["badge"])}</span>' if p.get("badge") else ""
    was = f'<s>{e(p["was"])}</s>' if p.get("was") else ""
    meta = f'\n        <p class="meta">{e(p["meta"])}</p>' if p.get("meta") else ""

    why_points = checks(p["why"].get("points", []), CHECK_LIGHT, "        ")
    get_items = "\n".join(
        f'          <div class="get__item"><span class="get__num">{i:02d}</span><div><strong>{e(g["t"])}</strong><span>{e(g["d"])}</span></div></div>'
        for i, g in enumerate(p["get"], 1))
    topics = ""
    if p.get("topics"):
        topics = f'''
        <div class="topics">
          <h3>{e(p["topicsLabel"])}</h3>
{checks(p["topics"], CHECK_LIGHT)}
        </div>'''

    speakers = ""
    if p.get("people"):
        cards = "\n".join(
            f'        <div class="speaker"><span class="speaker__i" aria-hidden="true">{e(x["n"][0])}</span><div><strong>{e(x["n"])}</strong><span>{e(x["s"])}</span><small>{e(x["f"])}</small></div></div>'
            for x in p["people"])
        speakers = f'''
  <section class="section speakers" style="padding-top: 0">
    <div class="wrap">
      <h2>Meet the <span class="accent">speakers</span></h2>
      <div class="speakers__grid">
{cards}
      </div>
    </div>
  </section>
'''

    how = ""
    if slug in HAS_HOW:
        steps = "\n".join(f'          <div class="step"><span class="step__n">{i}</span><p>{e(t)}</p></div>' for i, t in enumerate(p["how"], 1))
        how = f'''
      <div class="how">
        <span class="eyebrow">How it works</span>
        <div class="steps">
{steps}
        </div>
      </div>'''

    CROSS = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#F5DCCB" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>'
    not_for = "\n".join(f'          <div class="check check--not">{CROSS}<span>{e(t)}</span></div>' for t in p.get("notFor", []))

    quote = ""
    if p.get("quote"):
        q = p["quote"]
        quote = f'''
  <section class="section">
    <figure class="pdp-quote reveal">
      <blockquote>"{e(q["text"])}"</blockquote>
      <figcaption><strong>{e(q["who"])}</strong> <span class="muted">· {e(q["what"])}</span></figcaption>
    </figure>
  </section>
'''

    partner = ""
    if p.get("partner"):
        pa = p["partner"]
        partner = f'''
  <section class="section">
    <div class="partner">
      <div>
        <span class="eyebrow">In collaboration with</span>
        <h2>{e(pa["title"])}</h2>
        <p>{e(pa["body"])}</p>
      </div>
    </div>
  </section>
'''

    related = "\n".join(
        f'''        <a class="rel" href="{r}.html">
          <span class="rel__body">
            <span class="prog__tag">{e(DATA[r]["kicker"])}</span>
            <span class="rel__name">{e(DATA[r]["t1"])} <span class="accent">{e(DATA[r]["t2"])}</span></span>
            <span class="rel__line">{e(DATA[r]["line"])}</span>
            <span class="rel__foot"><strong>{e(DATA[r]["price"])}</strong><span>See details →</span></span>
          </span>
        </a>''' for r in p["related"])

    return f'''<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(plain_title)} · Mickey Salim</title>
<meta name="description" content="{e(p["line"])}">
<meta name="theme-color" content="#F2EEEA">
<meta property="og:type" content="product">
<meta property="og:title" content="{e(plain_title)} · Mickey Salim">
<meta property="og:description" content="{e(p["line"])}">
<meta property="og:image" content="/assets/img/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="/assets/img/favicon.png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700;1,900&family=Onest:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/styles.css?v={VER}">
</head>
<body class="pdp">
<!-- Generated by tools/build_programs.py from tools/programs.json. Edit the JSON, then rebuild. -->

<nav class="nav" aria-label="Main">
  <div class="wrap">
    <a href="../index.html" class="brand" aria-label="Level Up Circle, home"><img class="brand__logo" src="/assets/img/level-up-circle-logo.png" alt="Level Up Circle" width="516" height="493"></a>
    <div class="nav__links"><a href="/programs" class="nav__link">Programs</a><a href="../index.html#about" class="nav__name">Mickey Salim</a></div>
  </div>
</nav>

<main>
  <section class="pdp-hero">
    <div class="wrap">
      <div class="pdp-hero__text">
        <div class="buy__tags"><span class="eyebrow">{e(p["kicker"])}</span>{badge}</div>
        <h1>{e(p["t1"])} <span class="accent">{e(p["t2"])}</span></h1>
        <p class="lead">{e(p["hook"])}</p>
{meta}
      </div>
      <div class="buycard">
        <div class="buycard__price"><strong>{e(p["price"])}</strong>{was}<span>{e(p["unit"])}</span></div>
        <span class="access">{BOLT}{e(access_label(slug))}</span>
        <a href="{e(p["link"])}" class="btn btn--primary" data-buy-anchor>{e(p["cta"])}</a>
        <span class="buy__note">{LOCK} Secure checkout on Lynk</span>
      </div>
    </div>
  </section>

  <section class="section band why">
    <div class="wrap">
      <div class="why__head">
        <h2>{e(p["why"]["title"])}</h2>
      </div>
      <div class="why__body">
        <p>{e(p["why"]["body"])}</p>
{why_points}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="get__head">
        <h2>Everything <span class="accent">included</span></h2>
      </div>
      <div class="get__body">
        <div>
{get_items}
        </div>{topics}
      </div>
    </div>
  </section>
{speakers}
  <section class="section dark who">
    <div class="wrap">
      <div>
        <span class="eyebrow">Who it's for</span>
        <h2>Is this <span class="accent">for you?</span></h2>
      </div>
      <div>
{checks(p["forList"], CHECK_DARK)}
{not_for}
      </div>{how}
    </div>
  </section>
{quote}{partner}
  <section class="section band related">
    <div class="wrap">
      <h2>You might <span class="accent">also like</span></h2>
      <div class="related__grid">
{related}
      </div>
    </div>
  </section>
</main>

<footer class="footer">
  <div class="wrap">
    <div class="footer__brand"><span>© 2026 Mickey Salim</span></div>
    <div class="footer__links">
      <a class="ig-main" href="https://instagram.com/hey.mickmok" target="_blank" rel="noopener">@hey.mickmok</a>
      <a href="https://instagram.com/levelupp.circle" target="_blank" rel="noopener">@levelupp.circle</a>
      <a class="top" href="../index.html#programs">← All programs</a>
    </div>
  </div>
</footer>

<div class="buybar" data-buybar inert>
  <div class="wrap">
    <div class="buybar__info"><strong>{e(p["name"])}</strong><span>{e(p["price"])}</span></div>
    <a href="{e(p["link"])}" class="btn btn--primary">{e(p["ctaShort"])}</a>
  </div>
</div>

<script src="/assets/js/main.js?v={VER}" defer></script>
</body>
</html>
'''


FILTERS = [("all", "All"), ("linkedin", "LinkedIn & CV"), ("abroad", "Working abroad"), ("study", "Study in Singapore"), ("personal", "1:1")]


def programs_page():
    head = page("linkedin-makeover", DATA["linkedin-makeover"]).split("<body", 1)[0]
    head = head.replace("<title>LinkedIn Makeover · Mickey Salim</title>", "<title>Programs · Mickey Salim</title>")
    head = head.replace('content="A step-by-step guide to give your LinkedIn profile a glow up."', 'content="Guides, audits and 1:1 advice from Mickey Salim, built from real experience in global companies."')
    head = head.replace('og:title" content="LinkedIn Makeover · Mickey Salim"', 'og:title" content="Programs · Mickey Salim"')
    head = head.replace('<meta property="og:type" content="product">', '<meta property="og:type" content="website">')
    tabs = "".join(f'<button class="tab" data-filter="{fid}" aria-pressed="{"true" if fid == "all" else "false"}">{e(lbl)}</button>' for fid, lbl in FILTERS)
    rows = "\n".join(f'''        <a class="row" href="/programs/{slug}" data-tags="{" ".join(p["tags"])}">
          <span class="row__meta"><span>{e(p["listFormat"])}</span>{f'<span class="row__badge">{e(p["listBadge"])}</span>' if p.get("listBadge") else ""}</span>
          <span class="row__main"><span class="row__name">{e(p["t1"])} <span class="accent">{e(p["t2"])}</span></span><span class="row__line">{e(p["line"])}</span></span>
          <span class="row__price"><strong>{e(p["price"])}</strong><span aria-hidden="true">→</span></span>
        </a>''' for slug, p in DATA.items())
    return head + f'''<body class="programs-page">
<!-- Generated by tools/build_programs.py from tools/programs.json. Edit the JSON, then rebuild. -->

<nav class="nav" aria-label="Main">
  <div class="wrap">
    <a href="/" class="brand" aria-label="Level Up Circle, home"><img class="brand__logo" src="/assets/img/level-up-circle-logo.png" alt="Level Up Circle" width="516" height="493"></a>
    <div class="nav__links"><a href="/programs" class="nav__link is-current" aria-current="page">Programs</a><a href="/#about" class="nav__name">Mickey Salim</a></div>
  </div>
</nav>

<main>
  <section class="index-hero">
    <div class="wrap">
      <h1>Programs</h1>
      <p>Guides, audits and 1:1 advice, built from real experience in global companies.</p>
    </div>
  </section>

  <div class="tabs-bar">
    <div class="wrap"><div class="tabs" role="toolbar" aria-label="Filter programs">{tabs}</div></div>
  </div>

  <section class="index-list">
    <div class="wrap" data-filter-list>
{rows}
      <p class="index-empty" hidden>Nothing here yet.</p>
    </div>
  </section>

  <!-- Free resources: add a section here (same .row markup, "Free" instead of a price) once the first resource is ready. -->

  <section class="index-close">
    <div class="wrap">
      <p>Not sure which one fits? <a href="https://ig.me/m/hey.mickmok" target="_blank" rel="noopener">DM me on Instagram</a> and I'll point you in the right direction.</p>
    </div>
  </section>
</main>

<footer class="footer">
  <div class="wrap">
    <div class="footer__brand"><span>© 2026 Mickey Salim</span></div>
    <div class="footer__links">
      <a class="ig-main" href="https://instagram.com/hey.mickmok" target="_blank" rel="noopener">@hey.mickmok</a>
      <a href="https://instagram.com/levelupp.circle" target="_blank" rel="noopener">@levelupp.circle</a>
      <a class="top" href="/">← Home</a>
    </div>
  </div>
</footer>

<script src="/assets/js/main.js?v={VER}" defer></script>
</body>
</html>
'''


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    # Stamp the landing page too
    home = ROOT / "index.html"
    html = re.sub(r'/assets/css/styles\.css(\?v=\w+)?', f"/assets/css/styles.css?v={VER}", home.read_text(encoding="utf-8"))
    html = re.sub(r'/assets/js/main\.js(\?v=\w+)?', f"/assets/js/main.js?v={VER}", html)
    home.write_text(html, encoding="utf-8")
    print("stamped index.html with", VER)
    for slug, p in DATA.items():
        (OUT / f"{slug}.html").write_text(page(slug, p), encoding="utf-8")
        print("built", f"programs/{slug}.html")
    (OUT / "index.html").write_text(programs_page(), encoding="utf-8")
    print("built programs/index.html")
