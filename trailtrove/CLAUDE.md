# trailtrove (in zhware-web) — guide for Claude Code sessions

Public static site for the Trail Trove apps (iOS/watchOS and Android/Wear OS, one set of pages for both): the support page and the privacy policy that the App
Store and Google Play require. Served at `https://zhware.org/trailtrove/` as a folder of the shared site (`sites/zhware-web`; hosting is in the root
`CLAUDE.md`). Links inside are root-relative with the `/trailtrove/` prefix. Plain HTML, no build step.

## Structure

```
index.html        redirect / landing with links to support and privacy
support/index.html   FAQ, contact, how tracking works and its limits — EN and DE on one page
privacy/index.html   privacy policy — EN and DE on one page
report/index.html    suggestion and bug form (Web3Forms); the apps pass ?d=<details>&k=<kind>, #de in German
report/thanks/       where the form redirects after sending
```

Each page is self-contained: inline `<style>`, system font stack, light and dark via `prefers-color-scheme`,
`lang` attributes per language block.

## Rules

- Plain HTML and CSS only. No JavaScript frameworks, no trackers, no analytics, no external fonts, no CDNs.
- English and German for every page. Keep the two versions in sync.
- **The privacy policy must state what the app actually does**, nothing more, nothing less: on-device only,
  the network uses listed there and nothing else (the report form is a web page the user fills in), Health and Photos as described, no accounts, no
  tracking, no ads. When either app's behaviour changes (see `../../apps/trailtrove/docs/SPEC.md` and, for Android, `../../apps/trailtrove-android/docs/ANDROID.md`), change the
  policy in the same piece of work.
- Preview locally with `python3 -m http.server`.
- **This repo is public. Never push without the owner's explicit approval.** Commit locally, show the pages, wait.
