# zhware-web

The static site for every zhware app, one GitHub Pages deployment at
<https://zhware.org>. Each app lives in its own folder with its own
`CLAUDE.md`; read that one before touching the folder.

| Path | What it is |
|---|---|
| `index.html` | Developer home: the signature, one sentence, one card per app with its own tile and its pages |
| `logo.svg` | The wordmark, outlined: `zh` bold, `ware` regular at 62 % opacity, a brass full stop. Inlined into `index.html` so it takes `currentColor` |
| `favicon.svg` | `zh.` on nothing; the ink follows the tab's light or dark theme |
| `icon.svg` | `zh.` on a paper tile: the source of `favicon.ico` and `apple-touch-icon.png` |
| `tools/make_mark.py` | Writes the five files above and the font subset from Hanken Grotesk. Needs `fonttools` and `brotli` in a throwaway venv and the variable TTF from google/fonts; neither is committed. Rasters go through `wordgarner/tools/make_icons.py` |
| `assets/fonts/` | `hanken-grotesk.woff2` (Latin, weights 400 to 700, about 13 kB) and its `OFL.txt`, used by the root pages only |
| `wordgarner/` | Word Garner: landing, privacy, support, terms, report form |
| `trailtrove/` | Trail Trove: landing, support, privacy |
| `404.html` | Neutral 404 for the whole site; Pages serves only a root one |
| `CNAME` | `zhware.org` |
| `.well-known/apple-app-site-association` | One file for every app: Apple reads it from the domain root, never from a path. Add each app's `<team>.<bundle id>` under `webcredentials` |
| `.nojekyll` | Lets Pages serve the dot-directory |

## Fixed decisions

- **The mark is direction A, "Signature"** (decided 2026-10-18 over a
  publisher tile and a seal): lowercase `zhware` in Hanken Grotesk, `zh`
  bold and `ware` lighter, closed by a brass full stop. No tile of its own,
  so it stays quiet beside the app tiles, which carry the colour. Change it
  through `tools/make_mark.py`, then bump `?v=` on the icon links.
- **The root pages load nothing from anyone else**, the font included: the
  footer says so. Never link a font network or a CDN from here.
- **No shared stylesheet.** Each app has its own styling, fonts and icons in
  its own folder. Only the root page is neutral.
- **Every link inside an app folder is root-relative with the app prefix**
  (`/wordgarner/privacy/`), including CSS `url()`. A bare `/privacy/` would
  point at nothing.
- **Static HTML, no build, no dependencies.** Preview from the repo root:
  `python3 -m http.server 8000`, then `http://localhost:8000/wordgarner/`.
- **Each app's privacy page is its own claim about its own app.** Review a
  diff folder by folder; a change in one app's folder never edits another's.
- **A push publishes every app.** Push only with the owner's approval; keep
  unfinished work on a branch.

## Hosting

GitHub Pages, branch `main`, folder `/`. `zhware.org` is an apex domain, so
DNS needs the four GitHub A records (`185.199.108.153` to `.111.153`) and the
matching AAAA records, and `www` is a CNAME to `<user>.github.io`. **Never
put a CNAME on the apex: it would break the MX records and with them the
support mailboxes.** Verify `zhware.org` under the GitHub account's Pages
verified domains.
