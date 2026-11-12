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

CHECK_LIGHT = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#4C6A51" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12l5 5 9-10"/></svg>'
CHECK_DARK = CHECK_LIGHT.replace("#4C6A51", "#F5DCCB")
LOCK = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg>'

e = lambda s: escape(s, quote=True)


def checks(items, icon):
    return "\n".join(f'          <div class="check">{icon}<span>{e(t)}</span></div>' for t in items)


def page(slug, p):
    title = f'{e(p["t1"])} <span class="accent">{e(p["t2"])}</span>'
    plain_title = f'{p["t1"]} {p["t2"]}'
    badge = f'<span class="badge">{e(p["badge"])}</span>' if p.get("badge") else ""
    was = f'<span style="text-decoration: line-through">{e(p["was"])}</span>' if p.get("was") else ""
    cover_lines = "".join(f'<div><b>{i:02d}</b><span>{e(t)}</span></div>' for i, t in enumerate(p["coverLines"], 1))

    why_points = checks(p["why"].get("points", []), CHECK_LIGHT)
    get_items = "\n".join(
        f'        <div class="get__item"><span class="get__num">{i:02d}</span><strong>{e(g["t"])}</strong><span>{e(g["d"])}</span></div>'
        for i, g in enumerate(p["get"], 1))

    topics = ""
    if p.get("topics"):
        topics = f'''
      <div class="topics">
        <h3>{e(p["topicsLabel"])}</h3>
        <div>
{checks(p["topics"], CHECK_LIGHT)}
        </div>
      </div>'''

    speakers = ""
    if p.get("people"):
        cards = "\n".join(
            f'        <div class="speaker"><span class="speaker__i" aria-hidden="true">{e(x["n"][0])}</span><div><strong>{e(x["n"])}</strong><span>{e(x["s"])}</span><small>{e(x["f"])}</small></div></div>'
            for x in p["people"])
        speakers = f'''
  <section class="section speakers" style="padding-top: 0">
    <div class="wrap">
      <h2>{e(p.get("peopleTitle", "Meet the speakers"))}</h2>
      <div class="speakers__grid">
{cards}
      </div>
    </div>
  </section>'''

    steps = "\n".join(f'          <div class="step"><span class="step__n">{i}</span><p>{e(t)}</p></div>' for i, t in enumerate(p["how"], 1))

    quote = ""
    if p.get("quote"):
        q = p["quote"]
        quote = f'''
  <section class="section" style="padding-bottom: 0">
    <figure class="pdp-quote reveal">
      <blockquote>"{e(q["text"])}"</blockquote>
      <figcaption><strong>{e(q["who"])}</strong> <span class="muted">· {e(q["what"])}</span></figcaption>
    </figure>
  </section>'''

    partner = ""
    if p.get("partner"):
        pa = p["partner"]
        partner = f'''
  <section class="section" style="padding-bottom: 0">
    <div class="partner">
      <div>
        <span class="eyebrow">In collaboration with</span>
        <h2>{e(pa["title"])}</h2>
        <p>{e(pa["body"])}</p>
      </div>
    </div>
  </section>'''

    related = "\n".join(
        f'''        <a class="rel" href="{r}.html">
          <span class="prog__tag">{e(DATA[r]["kicker"])}</span>
          <span class="rel__name">{e(DATA[r]["t1"])} <span class="accent">{e(DATA[r]["t2"])}</span></span>
          <span class="rel__line">{e(DATA[r]["line"])}</span>
          <span class="rel__foot"><strong>{e(DATA[r]["price"])}</strong><span>See details →</span></span>
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
<link rel="stylesheet" href="/assets/css/styles.css">
</head>
<body class="pdp">
<!-- Generated by tools/build_programs.py from tools/programs.json. Edit the JSON, then rebuild. -->

<nav class="nav" aria-label="Main">
  <div class="wrap">
    <a href="../index.html" class="brand"><span class="brand__name">Mickey Salim</span><span class="brand__sub">Level Up Circle</span></a>
    <a href="../index.html#programs" class="nav__back">← All programs</a>
  </div>
</nav>

<main>
  <section class="pdp-hero">
    <div class="wrap">
      <div class="cover cover--{p["cover"]}" aria-hidden="true">
        <span class="cover__top">Level Up Circle by Mickey Salim</span>
        <div class="cover__title">{e(p["t1"])}<em>{e(p["t2"])}</em></div>
        <div class="cover__lines">{cover_lines}</div>
      </div>
      <div class="buy">
        <div class="buy__tags"><span class="eyebrow">{e(p["kicker"])}</span>{badge}</div>
        <h1>{title}</h1>
        <p class="lead">{e(p["hook"])}</p>
        <div class="buy__box">
          <div class="buy__price"><strong>{e(p["price"])}</strong>{was}<span>{e(p["unit"])}</span></div>
          <a href="{e(p["link"])}" class="btn btn--primary" data-buy-anchor>{e(p["cta"])}</a>
          <span class="buy__note">{LOCK} Secure checkout on Lynk · {e(p["after"])}</span>
        </div>
      </div>
    </div>
  </section>

  <section class="section band why">
    <div class="wrap">
      <div class="why__head">
        <span class="eyebrow">01 — Why this exists</span>
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
        <span class="eyebrow">02 — What you'll get</span>
        <h2>Everything <span class="accent">included</span></h2>
      </div>
      <div class="get__list">
{get_items}
      </div>{topics}
    </div>
  </section>
{speakers}
  <section class="section dark how">
    <div class="wrap">
      <div class="how__col">
        <span class="eyebrow">03 — How it works</span>
        <div>
{steps}
        </div>
      </div>
      <div class="how__col">
        <span class="eyebrow">04 — Who it's for</span>
        <div>
{checks(p["forList"], CHECK_DARK)}
        </div>
      </div>
    </div>
  </section>
{quote}{partner}
  <section class="section">
    <div class="note">
      <img src="/assets/img/mickey-candid.jpg" alt="Mickey Salim" width="480" height="480" loading="lazy">
      <div>
        <p>{e(p["note"])}</p>
        <p class="sign">Onwards and upwards, {e(p["signoff"])}</p>
      </div>
    </div>
  </section>

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
    <div class="footer__brand"><strong>Mickey Salim</strong><span>© 2026 Mickey Salim · Level Up Circle</span></div>
    <div class="footer__links">
      <a class="ig-main" href="https://instagram.com/hey.mickmok" target="_blank" rel="noopener">@hey.mickmok</a>
      <a href="https://instagram.com/levelupp.circle" target="_blank" rel="noopener">@levelupp.circle</a>
      <a class="top" href="../index.html">← Home</a>
    </div>
  </div>
</footer>

<div class="buybar" data-buybar inert>
  <div class="wrap">
    <div class="buybar__info"><strong>{e(p["name"])}</strong><span>{e(p["price"])}</span></div>
    <a href="{e(p["link"])}" class="btn btn--primary">{e(p["ctaShort"])}</a>
  </div>
</div>

<script src="/assets/js/main.js" defer></script>
</body>
</html>
'''


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for slug, p in DATA.items():
        (OUT / f"{slug}.html").write_text(page(slug, p), encoding="utf-8")
        print("built", f"programs/{slug}.html")
