# zhware-web / wordgarner

The public site for [Word Garner](https://zhware.org/wordgarner/) — the landing
page, the privacy policy, the support page and the terms of use that the App
Store and Google Play require before a build can be submitted.

Plain static HTML. No build step, no dependencies, no JavaScript.

## The mark

A pea pod holding three seeds, on a deep-teal tile. `icon.svg` is the app
icon, with a glyph on each seed (A, あ, 字, as outlines — no font needed),
and it is the header's logo too, at 64 px, where those glyphs are readable.
`favicon.svg` is the same drawing with plain seeds, for the tab and anything
else under 32 px, where the glyphs only blur.
`favicon.ico` (16/32/48) and `apple-touch-icon.png` (180) are rasters of
those two files, for the browsers and home screens that will not take an
SVG. Everything is committed; after changing the mark, regenerate the
rasters — and, with `--app`, the app's iOS and Android icon sets from the
same files:

```bash
python3 tools/make_icons.py --app ../../../apps/wordgarner
```

The icon links carry a `?v=N`, because browsers hold a favicon much longer
than the site asks them to. Bump it in all six pages when the mark changes,
or returning visitors keep the old one.

The name beside the mark is set in Bricolage Grotesque — 2.6 kB in
`assets/fonts/`, cut down to the nine letters of "Word Garner" and served
from this site, never from a font network. It is the only webfont here and
the only thing that uses it is the header. Renaming the site means cutting
a new subset first: the `@font-face` declares the subset's own
`unicode-range`, so a letter it does not contain falls back to the system
sans without a word.

## Preview

```bash
python3 -m http.server 8000
# http://localhost:8000
```

## Publishing

The whole site is one GitHub Pages deployment; see the root `README.md`.

## The report form

`/wordgarner/report/` posts to [Web3Forms](https://web3forms.com/), which emails it on
to `app.support@zhware.org`. GitHub Pages cannot run anything itself,
so the form needs an off-site endpoint.

The access key is shared by every app's form: one key named `support-zhware`, registered once at <https://web3forms.com/> with
`app.support@zhware.org` and the website `https://zhware.org/wordgarner/support/`,
then paste the key into the `access_key` hidden field in `report/index.html`.
The key is public by design — it only says which mailbox to deliver to.

Spam is handled by the **Honeypot Trick**: the hidden `botcheck` checkbox. A
bot ticks it, a person never sees it, and Web3Forms drops the message. No
CAPTCHA in the path.

Two things worth checking against their current documentation before you
rely on them:

- **No attachments.** File uploads are a paid Web3Forms feature, so the form
  is text only and people are pointed at the support address for screenshots.
  Adding a file input back means `enctype="multipart/form-data"`, a paid plan,
  and a line in the privacy policy.
- **The `redirect` field.** It points at `/wordgarner/report/thanks/`, which only works
  once the custom domain is live.

## URLs the store listings need

| Field | Value |
|---|---|
| Privacy policy URL (Apple, Google) | `https://zhware.org/wordgarner/privacy/` |
| Support URL (Apple) | `https://zhware.org/wordgarner/support/` |
| Marketing URL (Apple, optional) | `https://zhware.org/wordgarner/` |
| Contact email (Google) | `app.support@zhware.org` |
| EULA (Apple, optional) | `https://zhware.org/wordgarner/terms/` |

## Before submitting

- [ ] Drop store screenshots into `assets/screenshots/` and reference them on
      the landing page (`apps/wordgarner/tool/screenshots.sh` takes them).
- [ ] Add the App Store and Play links to the landing page once the listings
      exist.
- [ ] Re-read `privacy/index.html` against what the app actually does, and
      answer Play's Data safety form the same way.
- [ ] Paste the Web3Forms `access_key` into `report/index.html` and send one
      test report end to end.
- [ ] Look at the landing page on a real phone in both themes. The palette
      moved to the mark's colours (deep teal on light, pea green on dark)
      and only the desktop browser has seen it.
