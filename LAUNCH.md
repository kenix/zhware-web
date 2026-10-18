# Launching zhware.org

The runbook for taking this site live and moving Word Garner onto it. Do the
steps in order: every step only needs the ones above it. Tick them off here
and delete the file once the last one is done.

GitHub account: `kenix`. DNS: Spaceship. Mail: whatever already serves
`app.support@zhware.org`.

## A. Mail first, so nothing bounces

1. **Check that `app.support@zhware.org` receives mail.** Send it a test
   from another account.
2. **One Web3Forms key for every app.** At <https://web3forms.com/> create an
   access key for `app.support@zhware.org` and name it `support-zhware`. The
   key arrives by mail. Hand it over and it goes into the `access_key` field
   of `wordgarner/report/index.html`, and of any later app's form. It is
   public by design. Each form's hidden `subject` field says which app
   a message came from. Word Garner's says `Word Garner report`.
3. **Retire `wordgarner.support@zhware.org`** (decided 2026-10-18, no
   forward). Build 5 is never released, so no public build shows it. Move
   everything that still sends to it:
   - In `svcs/lexis/fly.toml`, `LEXIS_REPORT_TO` (the daily report and the ceiling
     alert) is `dev.support@zhware.org`. Done and deployed 2026-10-18.
   - The Web3Forms key is renamed `support-zhware`, bound to `app.support@`.
     Done.
   - The Google consent screen's support email, if it was ever set (step 14).
   - Any App Store Connect contact that uses it.

   Delete the mailbox after the step 15 submission has gone through, so a
   reviewer's mail can't bounce in the meantime.

## B. GitHub repository

4. **Create the repository:** <https://github.com/new>, owner `kenix`, name
   `zhware-web`, **Public** (Pages on a free account needs a public
   repository), with no README, no licence and no .gitignore.
5. **Push `main` only:**

   ```sh
   cd sites/zhware-web
   git remote add origin git@github.com:kenix/zhware-web.git
   git push -u origin main
   ```

   **Never push `trailtrove-next`.** The repository is public, so a pushed
   branch shows unreleased Trail Trove wording to anyone, even though Pages
   only serves `main`.
6. **Verify the domain**, to prevent takeover. Click your avatar, then
   **Settings ▸ Pages** (the account's settings, not the repository's), then
   **Add a domain**, `zhware.org`. GitHub shows a TXT record, host
   `_github-pages-challenge-kenix`, with a value. Add that record in
   step 7, then come back and click **Verify**. If `zhware.org` is already
   listed as verified (from setting up `wordgarner.zhware.org`), skip this
   step.

## C. Spaceship DNS

7. In Spaceship, open **Domain Manager**, then `zhware.org`, then its DNS
   records.
   - **First, look at what is there.** Delete any **A**, **AAAA**, **ALIAS**
     or **URL redirect / parking** record on the host `@` (the apex). **Do not
     touch MX, or TXT records for SPF, DKIM or DMARC.** They carry the mail.
     Keep the `wordgarner` CNAME as well: the old site stays up as redirects
     (step 17).
   - **Add these records:**

     | Type | Host | Value |
     |---|---|---|
     | A | `@` | `185.199.108.153` |
     | A | `@` | `185.199.109.153` |
     | A | `@` | `185.199.110.153` |
     | A | `@` | `185.199.111.153` |
     | AAAA | `@` | `2606:50c0:8000::153` |
     | AAAA | `@` | `2606:50c0:8001::153` |
     | AAAA | `@` | `2606:50c0:8002::153` |
     | AAAA | `@` | `2606:50c0:8003::153` |
     | CNAME | `www` | `kenix.github.io` |
     | TXT | `_github-pages-challenge-kenix` | the value from step 6 |

   - **Never put a CNAME on `@`.** It would replace the MX records, and the
     support mailboxes would stop receiving.
8. **Check from the terminal** (allow up to an hour):

   ```sh
   dig +short zhware.org A          # the four 185.199.x.153
   dig +short zhware.org AAAA       # the four 2606:50c0:...
   dig +short www.zhware.org        # kenix.github.io. then the IPs
   dig +short zhware.org MX         # unchanged from before
   ```

## D. Pages

9. **Repository `zhware-web`, then Settings ▸ Pages.** Set **Source** to
   *Deploy from a branch*, then pick **`main`** and **`/ (root)`**, then
   **Save**.
10. **Custom domain:** `zhware.org` ▸ **Save** (the `CNAME` file already says
    so). Wait for the DNS check to pass.
11. **Tick Enforce HTTPS** once GitHub offers it. The certificate takes
    from minutes to about an hour.
12. **Check the live site:**

    ```sh
    for p in / /wordgarner/ /wordgarner/support/ /wordgarner/privacy/ \
             /wordgarner/terms/ /wordgarner/report/ /trailtrove/ \
             /trailtrove/support/ /trailtrove/privacy/ \
             /.well-known/apple-app-site-association; do
      printf '%s %s\n' "$(curl -so /dev/null -w '%{http_code}' https://zhware.org$p)" "$p"
    done
    curl -sI https://www.zhware.org | grep -i '^location'   # -> https://zhware.org/
    ```

    Every line should show `200`. The AASA must answer `200` directly, with no
    redirect. A day later Apple's cache should have it too:
    `curl -s https://app-site-association.cdn-apple.com/a/v1/zhware.org`.
13. **Send a test report** through `/wordgarner/report/` and check that it
    arrives at `app.support@`.

## E. Consoles

14. **Google Auth Platform** (if the Word Garner project exists; see
    `apps/wordgarner/docs/google-ios.md`):
    - Open **Branding**. Change the app home page to
      `https://zhware.org/wordgarner/`, the privacy policy to
      `https://zhware.org/wordgarner/privacy/` and the terms to
      `https://zhware.org/wordgarner/terms/`. The authorised domain stays
      `zhware.org`.
    - **User support email** offers only your own Google sign-in address or a
      Google Group you manage. If `app.support@zhware.org` is not offered, you
      can create a Google account for that existing address (choose "use my
      current email address" when signing up). Add that account as Owner
      under IAM, sign in as it, and pick it. Otherwise keep your own address.
    - **Developer contact information:** `app.support@zhware.org` (any
      address works here).
15. **App Store Connect, Word Garner 1.0.** Build 5 is the approved build
    but is never released. Build 15 (`1.0.0+15`, commit `69a460b`) carries
    the new URLs, `app.support@` and `webcredentials:zhware.org`.
    1. Archive and upload build 15 as `apps/wordgarner/docs/app-store-release.md`
       describes. It lands in TestFlight and leaves the approved build
       alone. Record the review video on it (shot list in
       `docs/app-review-notes.md`, with a fresh demo account) and take the
       screenshots (`tool/screenshots.sh` on *iPhone 17 Pro Max* and
       *iPad Pro 13-inch*).
    2. When ready, **Developer Reject** build 5 on the 1.0 version page. The
       version becomes editable. Release stays manual.
    3. **App Privacy ▸ Privacy Policy URL:**
       `https://zhware.org/wordgarner/privacy/`.
    4. On the version page, set the **Support URL** to
       `https://zhware.org/wordgarner/support/` and the **Marketing URL** to
       `https://zhware.org/wordgarner/`. Replace the screenshots. In App Review
       Information, put in the new demo account and the review video, and
       optionally set the contact email to `app.support@`.
    5. Pick build 15 and **Submit for Review**. The pages are live since
       step 12, which Review opens.
    6. On the next sign-up on a device, check that iOS offers a strong password.
       That proves the AASA works.
16. **Google Play** (when the listing exists): **Store settings ▸ Store
    listing contact details**: email `app.support@zhware.org`, website
    `https://zhware.org/wordgarner/`. **App content ▸ Privacy policy**:
    `https://zhware.org/wordgarner/privacy/`.

## F. Afterwards

17. **Turn `wordgarner.zhware.org` into redirects.** Replace the
    `wordgarner-web` pages with stubs that send each path to
    `https://zhware.org/wordgarner/...`, and keep its AASA for TestFlight
    builds already installed. That is a push, so it needs your approval. Keep its DNS record
    for months.
18. **When Word Garner is released:** on the home page, swap its *Coming
    soon* tag for the App Store link.
19. **When Trail Trove's iOS build ships:** rebase `trailtrove-next` onto
    `main`, bump its *Effective* date, merge, push, and swap its tag for the
    store link. The app must already link to `zhware.org/trailtrove/` (asked
    of the Trail Trove session on 2026-10-18).
20. **Retire `sites/trailtrove-web`.** It was never pushed, and its pending
    edits live on `trailtrove-next`. Archive `kenix/wordgarner-web` once the
    redirects have done their job.
