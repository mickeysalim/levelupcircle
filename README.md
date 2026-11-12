# Mickey Salim · Level Up Circle

Personal-brand site for Mickey Salim (@hey.mickmok): a landing page plus six program pages. Checkout happens on Lynk.

Plain HTML, CSS and JavaScript. No framework and no build step needed to deploy.

## Structure

```
index.html                 Landing page
programs/*.html            Program pages (generated, see below)
assets/css/styles.css      All styles
assets/js/main.js          Slideshow, "see more" programs, sticky buy bar, scroll reveal
assets/img/                Photos, posters, logo, favicon, share image
tools/programs.json        Copy, prices and Lynk links for every program page
tools/build_programs.py    Builds programs/*.html from programs.json
vercel.json                Clean URLs (/programs/cv-audit) and asset caching
```

## Editing

- **Landing page copy or prices:** edit `index.html`.
- **Program pages:** edit `tools/programs.json`, then run `python3 tools/build_programs.py` (this also refreshes the version stamp on the CSS/JS links, so browsers pick up changes). Don't edit `programs/*.html` by hand; they are overwritten.
- **Next live session:** there's a commented-out strip in `index.html` under "Next live session". Fill it in and remove the comment markers.

## Preview locally

```
python3 -m http.server 8000
```

Then open http://localhost:8000.

## Deploy (Vercel, free)

1. On vercel.com, choose **Add New → Project** and import this GitHub repo.
2. Framework preset: **Other**. Leave the build command and output directory empty.
3. Deploy. Every push to `main` redeploys automatically.

To add a custom domain later: Project → Settings → Domains.
