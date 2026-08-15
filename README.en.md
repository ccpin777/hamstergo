# HamsterGo · Hamster Travel Day

English ｜ [中文](README.md)

A pure front-end packing checklist styled like a boarding pass, as if a little hamster were helping you pack. Installable to your phone's home screen and usable like a regular app.

## Features

- **Quantity fields**: every item has a quantity field; normal mode shows only the number, while edit mode shows the input and stepper controls. Empty quantities stay blank and 0 is treated as empty; tops, socks, underwear, and daily contacts still get default values based on trip length
- **Check / cross progress tracking**: tap an item once to check it (bringing it), tap again to cross it out (skipping it this time), tap a third time to clear it; both checked and crossed items count toward progress — there's no more "essential vs. optional" distinction
- **Document flow**: defaults to domestic flight (driver's license wallet), can switch to international (passport); "① Packed" immediately counts toward progress, while "② Stowed" completes the airport hand-off. Edit mode can undo only the stowed state while keeping the document packed
- **Carry-on / Checked baggage toggles**: Carry-on and Checked Baggage each have their own on/off toggle. Domestic defaults to "carry-on on, checked off"; international defaults to "both on" — switching between domestic/international applies the matching defaults automatically, and you can still adjust either toggle by hand afterward. Whenever the checked-baggage toggle is on, the clothing category (tops, socks, underwear, pants, jacket, shoes, slippers) automatically moves into Checked Baggage; turning it off moves clothing back into Carry-on
- **Editing and adding items**: top icon controls open editing and a centered add dialog; the dialog supports Cancel, backdrop click, and Esc. Choose a major section, then a Carry-on subcategory. Custom items can be renamed, deleted, reordered, and quantified; built-in items stay fixed. "Start a new trip" remains available both at the top and in the footer
- **Drag to reorder items**: in edit mode, a drag handle appears next to every item; press and drag up/down to reorder items within their own category (mouse and touch both supported), and the order is remembered. Categories themselves stay in a fixed order and can't be dragged, and items can't be moved across categories
- **Pre-departure reminders**: Section 05 (`Pre-departure reminders 出發前提醒`) is excluded from the main completion rate; it auto-collapses when all reminders are checked and has a manual expand/collapse control
- **Status prompts**: the top headline switches between "🐹 Today is the day! N items are still missing." and "🐹 Packing complete! ✈️"; the main completion rate counts only Sections 01 to 04, excluding Section 05
- **Recheck flow**: the icon appears only after the main list is processed and the document is stowed. Recheck mode preserves crossed-out items, lets blank items be checked or unchecked, locks crossed-out items, and locks baggage toggles and flight instructions
- **Checklist items**: added Travel Toiletry Bag, Medicine Bag, and Charging Bag as normal checklist items
- **Document reminders**: two reminder points — before departure and after security
- **Local storage only**: checkmarks, day count, and custom items are all stored in the browser's `localStorage`, staying on your own device — nothing is uploaded to any server
- **Installable as a PWA**: add to your phone's home screen for a full-screen experience, with offline caching via a Service Worker

## File structure

```
.
├── index.html          # main page and logic
├── manifest.json        # PWA config (name, icons, colors, launch mode)
├── service-worker.js    # offline caching logic
├── resources/
│   ├── icon-192.png         # app icon (192×192)
│   ├── icon-512.png         # app icon (512×512)
│   └── *.svg                # individual UI icon copies
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

After that, double-click `deploy.command` any time you make changes, type a description, and it'll commit + push automatically.

## Data storage notes

All data lives in **this phone, this browser** (`localStorage`) — it doesn't sync across devices, and no one (including the developer) can see your data. Clearing browser data or switching phones will reset it.

## Customization

- To change checklist items or categories, edit the `getData()` function in `index.html`
- To change the color scheme, edit the CSS variables at the top of `index.html` under `:root` (`--navy`, `--amber`, etc.)
- To change the app icons, regenerate `resources/hamstergo-icon-192.png` / `resources/hamstergo-icon-512.png` with the same filenames; individual UI SVG copies also live in `resources/`, while the page keeps inline SVG for direct `index.html` opening
