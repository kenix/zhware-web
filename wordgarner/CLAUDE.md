# wordgarner (in zhware-web)

The Word Garner section of the shared site, `sites/zhware-web/wordgarner/`:
<https://zhware.org/wordgarner/>. Hosting, DNS and the apex page are in the
root `CLAUDE.md`; every path below is relative to this folder, and every link
inside it is root-relative with the `/wordgarner/` prefix.

It exists because both stores require it. Apple wants a support URL and a
privacy policy URL before a build can be submitted; Google Play wants a
privacy policy URL and a contact address, and its Data safety form has to be
backed by what the policy says. Everything here is written to be the answer
to one of those.

## Commands

There is no build. It is four HTML files and one stylesheet.

```bash
python3 -m http.server 8000     # from the repo root; http://localhost:8000/wordgarner/
```

## Fixed decisions (do not revisit)

- **Static HTML, hand-written, no generator and no dependencies.** The site
  is four pages that change a few times a year. A toolchain would be more
  to maintain than the thing it maintains.
- **No cookies, no analytics, no third-party scripts, no webfonts.** An app
  whose whole pitch is that it does not phone home cannot have a privacy
  page that loads a font from someone else's CDN. The single exception is
  eight lines of our own inline script on the report page, declared in the
  privacy policy.
- **The form posts to Web3Forms.** GitHub Pages serves files and runs
  nothing, so a form needs somewhere off-site to post to. It is a plain
  `<form method="POST">` with no JavaScript in the path, so it still works
  with scripting off; `redirect` is the thank-you page and `botcheck` is the
  Honeypot Trick that keeps the CAPTCHA out of the way. `access_key` is the
  public Web3Forms key for the support mailbox. **It is a third-party data
  flow and the privacy policy says so** — do not add another one without
  adding it there too.
- **The app's own details arrive in the link, not from the browser.** The
  app opens `/wordgarner/report/?d=<diagnostics>`; the page copies that into a
  read-only field so the user sees exactly what will be sent. The browser
  cannot be asked for the app version, and asking a person to copy it by
  hand is asking for the report without it.
  **`k` and `m` fill in the kind and the message the same way**, for the one
  report the app can start on somebody's behalf: a share whose format it
  could not make sense of, where the useful thing to send is the text that
  arrived and the app is the only thing holding it. Unlike `d` they land in
  the ordinary editable fields, because they are the reader's message and
  not a fact about their install — the same rule either way: what you can
  see is exactly what goes, and anything there can be deleted before Send.
  An unknown `k` is ignored rather than an error; these arrive from a URL.
- **Hosted on GitHub Pages** with the rest of `zhware.org`; see the root
  `CLAUDE.md`.
- **One stylesheet, light and dark**, driven by `prefers-color-scheme`.
- **The form's controls are styled, not left to the browser.** A browser
  sizes a `select` to its longest option and a `textarea` to a 20-column
  default, so on a 42rem column the report form read as three small boxes
  adrift in a wide page — the field somebody is meant to write a paragraph
  in was the width of a name, and could only be dragged bigger. They are
  one full-width column with the page's own border, radius and type, and
  the message box opens at the size the paragraph wants. `resize: vertical`
  on purpose: taller is useful, wider drags the page past the measure the
  whole site is set to. The `select`'s chevron is drawn in CSS because
  Safari drops the background and the padding on a control it still owns,
  and it takes two rules because a data URI cannot read `currentColor`.
  A `<label>` is `display: block`, so no `<br>` follows one.
- **One mark, defined once, in SVG.** The mark is a pea pod holding three
  seeds on a deep-teal tile. `icon.svg` is the app icon: each seed carries
  a glyph (A, あ, 字 — the scripts the app renders), converted to outlines
  so the file needs no font. It is also what the page header shows, at
  64 px, big enough that the glyphs read as letters; the name beside it is
  sized to match, because a large mark over a small name reads as a logo
  with a caption. `favicon.svg` is the same drawing with plain seeds, for the tab
  and anything else under 32 px, where a glyph only muddies its seed.
  Every raster icon — `favicon.ico`,
  `apple-touch-icon.png`, and with `--app` the app's iOS and Android sets —
  is produced by `tools/make_icons.py`, which *reads* those two SVGs and
  rasterises them (pure standard library, run by hand, output committed):
  32 px and above from `icon.svg`, below from `favicon.svg`. So the shape
  lives in the SVGs only; change it there, rerun the script, commit all of
  it. The tile carries its own background, which is why there is no
  dark-mode variant and no colour rule on `.brand .mark`.
- **Every icon reference carries `?v=N`.** A browser holds a favicon far
  longer than the ten minutes GitHub Pages asks for, so without it a
  returning visitor — an app-store reviewer, for one — keeps seeing the
  previous mark. Bump the number in all six pages when the mark changes.
- **One webfont, and it is ours.** 2.6 kB of Bricolage Grotesque cut down
  to the nine letters of the name, in `assets/fonts/`, used by `.brand`
  and nothing else. The old rule was "no webfonts", to keep the site quick
  on a store listing and to keep the privacy page honest; a same-origin
  subset smaller than the icon beside it answers both, which is why it was
  allowed to bend. Anything from a font network still is not. The
  `unicode-range` in the `@font-face` is the subset's own, so a letter
  outside the name falls back silently: re-cut the file before renaming
  the site. `assets/fonts/OFL.txt` is the licence the font ships under and
  has to stay beside it.

## Layout

| Path | What it is |
|---|---|
| `index.html` | Landing page: what the app is, what it does, store links |
| `privacy/index.html` | Privacy policy — the URL both stores require |
| `support/index.html` | Support page — the URL Apple requires, plus the FAQ |
| `report/index.html` | The bug/idea form, posted to Web3Forms |
| `report/thanks/index.html` | Where Web3Forms sends people afterwards |
| `terms/index.html` | Terms of use / EULA supplement |
| `icon.svg` | The mark with glyphs on the seeds: the app icon, the page header, and every raster of 32 px or more |
| `favicon.svg` | The mark with plain seeds: the tab icon, and anything under 32 px |
| `favicon.ico`, `apple-touch-icon.png` | Rasters of the SVGs, written by `tools/make_icons.py` |
| `tools/make_icons.py` | Rasterises the two SVGs; `--app PATH` also writes the app's icon sets. Run by hand, output committed |
| `assets/style.css` | The whole stylesheet |
| `assets/fonts/` | The wordmark subset and its `OFL.txt`. The only webfont |
| `assets/screenshots/` | Store screenshots, as they are taken |

Pages live in directories with an `index.html` so the URLs have no `.html`
suffix and a trailing slash works.

## What the store listings need from here

| Field | Value |
|---|---|
| Privacy policy URL (Apple, Google) | `https://zhware.org/wordgarner/privacy/` |
| Support URL (Apple) | `https://zhware.org/wordgarner/support/` |
| Marketing URL (Apple, optional) | `https://zhware.org/wordgarner/` |
| Contact email (Google) | `app.support@zhware.org` |
| EULA (Apple, optional) | `https://zhware.org/wordgarner/terms/` |

**Both stores' data answers change the moment the hosted engine is enabled
in a shipped build**, and they have to agree with `/wordgarner/privacy/#hosted` word
for word. What to declare: an *account* linked to the user (the anonymous
identifier), *app functionality* and — since the daily report of
2026-10-03 counts distinct accounts — *analytics* as its purposes, no
tracking, no advertising, and user-generated content — the captured text — sent to a
sub-processor and not linked to an identity. **Email accounts add one
line:** *Contact info ▸ Email address*, collected, linked to the user, for
*app functionality* (account management) only — even though the service
keeps only a hash of it, the stores count what is collected, not what is
stored. Resend is the sub-processor that sends the codes. Apple additionally requires
that an app offering account creation offers account deletion **in the
app**; Settings ▸ Account ▸ Delete account is that, and it revokes the Sign
in with Apple grant, which is a separate review requirement.

## Keeping it true

The privacy policy is a factual claim about the app, not boilerplate. If the
app ever gains an account, an analytics SDK, a crash reporter, a push
notification, or a server of its own, **this page is wrong until it is
changed**, and the store listing's data-safety answers are wrong with it.
The privacy page's *What might change* section is the one place that looks
forward, and it is a promise as much as a plan: anything hosted is
**optional**, and this page is updated **before** it ships. Do not soften
either half.

**The hosted engine has now shipped, and the promise was kept.** It moved
out of *What might change* and into *What leaves your device* as a section
that says what is sent, who else sees it (OpenAI, named), what is kept (an
anonymous identifier and a daily counter, both expiring — and since
27 September 2026, for an email account, a hash of the address and an
Argon2id hash of the password, with Resend named as the sender of the
codes), what is logged (a
digest, never the text) and how to delete the account. The forward-looking
section keeps hosted storage alone, and now points at the shipped section as
evidence that the order holds. **Write the page before the build, every
time** — the one order in which such a commitment means anything.

It also promises, in as many words, that **signing in is never a
prerequisite for using the app** — no sign-in wall, asked once at the moment
something hosted is requested, never again if declined, and everything else
working with no account at all. That constrains the hosted service, not the
other way round, and the app is built to it.

The claims that would break first:

- "no analytics, advertising or tracking"
- "three things can ever leave your device, and you ask for each of them" —
  text through Lexis once you sign in, a dictionary pack from GitHub, and
  the vocabulary to the reader's *own* iCloud once iCloud sync is on
  (2026-10-10). It was *one* until the packs shipped, *three* while the app
  also took an API key of the reader's own, *two* after keys were removed on
  2026-09-27, and *three* again with sync. The summary panel has had to be
  recounted each time; a new flow breaks the sentence again.
- "it never reaches us" for iCloud sync — CloudKit's *private* database of
  the reader's Apple ID, no server of ours in the path. Data the developer
  cannot access is not "collected" for either store's privacy answers, which
  is why sync adds nothing there. A sync through Lexis (Android) would break
  this and move hosted storage out of *What might change*.
- "the app no longer takes an API key of your own" — on the privacy, terms,
  home and support pages. Keys coming back means all four change first.
- "a word up to 40 characters, a phrase 80, a sentence 300; Chinese,
  Japanese and Korean count twice" — on the home and support pages. These
  are `CaptureLimits` in the app and `MAX_WORD`/`MAX_PHRASE`/`MAX_SENTENCE`
  in Lexis; change the pages when those change.
- "your email address is not sent and not stored" — it is handed to the
  *app* by Apple or Google and stays in the Keychain. The service never
  receives it, and the moment it does this line is false.
- "the text itself is never logged" — the usage log carries a digest so
  repeats can be counted. Logging the word instead breaks it.
- "OpenAI" as the named sub-processor. Changing provider means changing
  this page first.
- "the only push notification is the silent one Apple sends while iCloud
  sync is on" — the reminder is still local. Any visible push breaks it.
- "this site sets no cookies, runs no analytics and loads nothing from
  anybody else: no third-party scripts, and no font network" — the
  wordmark font is served from this site, and that is the whole reason the
  sentence can still be written this way. Pulling one file from a CDN
  breaks it.

## Related

- The app: `apps/wordgarner`. Its Settings ▸ About links here, and its
  support tile opens `/wordgarner/support/`.
- The support address is `app.support@zhware.org`, shared by every zhware
  app. It appears on this site and as `AppConfig.supportEmail` in the app.
