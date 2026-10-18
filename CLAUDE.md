# zhware-web

The static site for every zhware app, one GitHub Pages deployment at
<https://zhware.org>. Each app lives in its own folder with its own
`CLAUDE.md`; read that one before touching the folder.

| Path | What it is |
|---|---|
| `index.html` | Developer home: a list of the apps |
| `wordgarner/` | Word Garner: landing, privacy, support, terms, report form |
| `trailtrove/` | Trail Trove: landing, support, privacy |
| `404.html` | Neutral 404 for the whole site; Pages serves only a root one |
| `CNAME` | `zhware.org` |
| `.well-known/apple-app-site-association` | One file for every app: Apple reads it from the domain root, never from a path. Add each app's `<team>.<bundle id>` under `webcredentials` |
| `.nojekyll` | Lets Pages serve the dot-directory |

## Fixed decisions

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
