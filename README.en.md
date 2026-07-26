# HamsterGo · Hamster Travel Day

English ｜ [中文](README.md)

A pure front-end packing checklist styled like a boarding pass, as if a little hamster were helping you pack. Installable to your phone's home screen and usable like a regular app.

## Features

- **Auto quantity by trip length**: socks, tops, underwear, and daily contact lenses (plus spares) automatically show how many you need based on the number of days you set; clothing quantities are shown as plain numbers instead of phrased day counts
- **Check / cross progress tracking**: tap an item once to check it (bringing it), tap again to cross it out (skipping it this time), tap a third time to clear it; both checked and crossed items count toward progress — there's no more "essential vs. optional" distinction
- **Document flow**: defaults to domestic flight (driver's license wallet), can switch to international (passport); after tapping "① Packed", the domestic/international toggle auto-hides, and it's only marked done after "② Stowed"
- **Carry-on / Checked baggage toggles**: Carry-on and Checked Baggage each have their own on/off toggle. Domestic defaults to "carry-on on, checked off"; international defaults to "both on" — switching between domestic/international applies the matching defaults automatically, and you can still adjust either toggle by hand afterward. Whenever the checked-baggage toggle is on, the clothing category (tops, socks, underwear, pants, jacket, shoes, slippers) automatically moves into Checked Baggage; turning it off moves clothing back into Carry-on
- **Edit mode**: add your own items under any category, and rename or delete them later. Built-in items stay fixed and can't be edited or removed. Clothing items can still toggle quantity display/editing. New items no longer have quantity controls at creation time. Added items are saved permanently — even tapping "Start a new trip" (which resets checkmarks) won't remove them
- **Drag to reorder items**: in edit mode, a drag handle appears next to every item; press and drag up/down to reorder items within their own category (mouse and touch both supported), and the order is remembered. Categories themselves stay in a fixed order and can't be dragged, and items can't be moved across categories
- **Pre-departure reminders**: a new Section 05 (`Pre-departure reminders 出發前提醒`) used as a reminder checklist; items can be checked on and off, but they do not count toward the main packing completion rate
- **Status prompts**: the top headline switches between "🐹 Today is the day! N items are still missing." and "🐹 Packing complete! ✈️"; the main completion rate counts only Sections 01 to 04, excluding Section 05
- **Recheck flow**: one tap clears all checked items while keeping crossed-out items, so you can review the same list again without losing "not bringing" choices
- **Document reminders**: two reminder points — before departure and after security
- **Local storage only**: checkmarks, day count, and custom items are all stored in the browser's `localStorage`, staying on your own device — nothing is uploaded to any server
- **Installable as a PWA**: add to your phone's home screen for a full-screen experience, with offline caching via a Service Worker

## File structure

```
.
├── index.html          # main page and logic
├── manifest.json        # PWA config (name, icons, colors, launch mode)
├── service-worker.js    # offline caching logic
├── icon-192.png         # app icon (192×192)
├── icon-512.png         # app icon (512×512)
├── deploy.command       # double-click script to commit + push to GitHub
└── dev-log.md           # development log
```

## Local testing

The Service Worker only registers over HTTPS or localhost, so you can't just double-click `index.html` and open it via `file://`. Spin up any simple local server, e.g.:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000` in your browser.

## Deploying to GitHub Pages

First-time setup:

1. Create a new GitHub repository (Public)
2. Run `git init` in this folder and add the repo's remote (`git remote add origin <repo-url>`)
3. Commit and push these files (at the repo root, not inside a subfolder)
4. Go to the repo's **Settings → Pages**, set Source to **Deploy from a branch**, Branch to **main** / **root**, and save
5. After 1–2 minutes you'll get a URL: `https://your-username.github.io/repo-name/`
6. Open that URL on your phone's browser → add to home screen to use it like a full-screen app

After that, double-click `deploy.command` any time you make changes, type a description (and optionally a version bump), and it'll commit + push automatically.

## Data storage notes

All data lives in **this phone, this browser** (`localStorage`) — it doesn't sync across devices, and no one (including the developer) can see your data. Clearing browser data or switching phones will reset it.

## Customization

- To change checklist items or categories, edit the `getData()` function in `index.html`
- To change the color scheme, edit the CSS variables at the top of `index.html` under `:root` (`--navy`, `--amber`, etc.)
- To change the icons, regenerate `icon-192.png` / `icon-512.png` keeping the same filenames
