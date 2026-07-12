# HamsterGo · Hamster Travel Day

English ｜ [中文](README.md)

A pure front-end packing checklist styled like a boarding pass, designed for trips where you're bringing your hamster along. Installable to your phone's home screen and usable like a regular app.

## Features

- **Auto quantity by trip length**: socks, tops, underwear, and daily contact lenses (plus spares) automatically show how many you need based on the number of days you set
- **Check / cross progress tracking**: tap an item once to check it (bringing it), tap again to cross it out (skipping it this time), tap a third time to clear it; both checked and crossed items count toward progress — there's no more "essential vs. optional" distinction
- **Document flow**: defaults to domestic flight (driver's license wallet), can switch to international (passport); after tapping "① Packed", the domestic/international toggle auto-hides, and it's only marked done after "② Stowed"
- **Edit mode**: add your own items under any category, optionally marking them to "scale with trip length"; added items can be renamed or deleted. Built-in items stay fixed and can't be edited or removed. Added items are saved permanently — even tapping "Start a new trip" (which resets checkmarks) won't remove them
- **Drag to reorder items**: in edit mode, a drag handle appears next to every item under Personal Item and Carry-on; press and drag up/down to reorder items within their own category (mouse and touch both supported), and the order is remembered. Categories themselves stay in a fixed order and can't be dragged
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
└── deploy.command       # double-click script to commit + push to GitHub
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
