# trailtrove-web

Static support and privacy site for **Trail Trove**, the free altitude, steps and trail app for iPhone and
Apple Watch. Plain HTML and CSS, no build step, served by GitHub Pages at <https://zhware.org/trailtrove/>.

## Pages

| Path | URL | Content |
|---|---|---|
| `/` | <https://zhware.org/trailtrove/> | Short intro with links (EN + DE) |
| `/support/` | <https://zhware.org/trailtrove/support/> | FAQ, contact, how tracking works and its limits (EN + DE) |
| `/privacy/` | <https://zhware.org/trailtrove/privacy/> | Privacy policy (EN + DE) |
| `/404.html` | — | Not-found page |

Both URLs are referenced from the app (Settings → About) and from App Store Connect.

## Local preview

```sh
python3 -m http.server 8000
# open http://localhost:8000/trailtrove/support/ (run from the repo root)
```

## Deployment

Part of the shared zhware.org site; hosting and DNS are in the root `CLAUDE.md`.

## App

The app source lives in the private repository `kenix/trailtrove`. The privacy policy here must describe what
that app actually does; change the two together.
