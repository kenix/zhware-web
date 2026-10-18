# trailtrove (in zhware-web) — guide for Claude Code sessions

Public static site for the Trail Trove iOS/watchOS app: the support page and the privacy policy that the App
Store requires. Served at `https://zhware.org/trailtrove/` as a folder of the shared site (`sites/zhware-web`; hosting is in the root
`CLAUDE.md`). Links inside are root-relative with the `/trailtrove/` prefix. Plain HTML, no build step.

## Structure

```
index.html        redirect / landing with links to support and privacy
support/index.html   FAQ, contact, how tracking works and its limits — EN and DE on one page
privacy/index.html   privacy policy — EN and DE on one page
```

Each page is self-contained: inline `<style>`, system font stack, light and dark via `prefers-color-scheme`,
`lang` attributes per language block.

## Rules

- Plain HTML and CSS only. No JavaScript frameworks, no trackers, no analytics, no external fonts, no CDNs.
- English and German for every page. Keep the two versions in sync.
- **The privacy policy must state what the app actually does**, nothing more, nothing less: on-device only,
  Apple map tiles and reverse geocoding as the only network use, HealthKit and Photos read-only, no accounts, no
  tracking, no ads. When the app's behaviour changes (see `../../apps/trailtrove/docs/SPEC.md`), change the
  policy in the same piece of work.
- Preview locally with `python3 -m http.server`.
- **This repo is public. Never push without the owner's explicit approval.** Commit locally, show the pages, wait.
