# crewbook (in zhware-web) — guide for Claude Code sessions

Public static site for the Crewbook iOS/watchOS rowing club app: the landing page, the support page and the privacy
policy that the App Store requires. Served at `https://zhware.org/crewbook/` as a folder of the shared site
(`sites/zhware-web`; hosting is in the root `CLAUDE.md`). Links inside are root-relative with the `/crewbook/` prefix.
Plain HTML, no build step.

## Structure

```
index.html           landing with links to support and privacy
support/index.html   FAQ and contact — EN and DE on one page
privacy/index.html   privacy policy — EN and DE on one page
favicon.svg          the app icon (logbook page with a club oar), copy of apps/crewbook/design/icon/svg/Favicon.svg
apple-touch-icon.png 180 px, copy of apps/crewbook/design/icon/png/apple-touch-icon.png
```

Each page is self-contained: inline `<style>`, system font stack, light and dark via `prefers-color-scheme`,
`lang` attributes per language block. Brand colour lake blue `#2F8AC4`.

## Rules

- Plain HTML and CSS only. No JavaScript frameworks, no trackers, no analytics, no external fonts, no CDNs.
- English and German for every page. Keep the two versions in sync.
- **The privacy policy must state what the app actually does**, nothing more, nothing less: the controller split
  (club controls its members' data, zhware processes it; zhware controls only the account email and sign-in), the data
  kept, the position on the water, Fly.io, Neon and Resend, swisstopo tiles as the only request from the device,
  weather and storm warning fetched by the server, no ads, no tracking. When the app's behaviour changes (see
  `../../apps/crewbook/docs/PLAN.md`), change the policy in the same piece of work, with a new date.
- **The agreement page is pending.** The Crewbook agreement (terms of use plus data processing, which a club accepts
  when it registers) needs the owner's text (open question 4 in `docs/PLAN.md`). Do not write one; add
  `/crewbook/agreement/` only when the owner supplies the text.
- Not in `.well-known/apple-app-site-association`: the app uses no webcredentials.
- Preview from the repo root with `python3 -m http.server 8000`.
- **This repo is public. Never push without the owner's explicit approval.** Commit locally, show the pages, wait.
