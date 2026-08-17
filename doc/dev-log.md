# 2026-08-17 — PWA product version display

- Standardized the HamsterGo PWA display to two lines: `Version 1.0` and `Build 10`; desktop mode hides the Build line, while the mobile brand title remains fixed-size and advanced the Service Worker cache identifier to v10 so an installed PWA refreshes the updated shell.

# HamsterGo — Dev Log

## 1.0 — 2026-08-17 — Version baseline

The current HamsterGo state is recorded as the first tracked version baseline: **1.0**, matching the version displayed in the app UI at that time. This establishes the starting point for the Apps Index version history; future product updates may advance it beyond 1.0.

---

## 2026-08-12 — Desktop layout, font persistence, visibility icons, and deployment script organization

Updated the packaged desktop window to use a blank native title bar. Font size and heading-font preferences are now part of the local travel state and encrypted cloud sync payload, with migration from the previous standalone localStorage keys. Added reusable `resources/eye-open.svg` and `resources/eye-closed.svg` assets for the sync-code and password visibility controls.

Reorganized deployment helpers: `Run.command` is at the HamsterGo project root, `deploy-worker.command` is in `cloudflare/`, and `deploy-github.command` is in the HamsterGo project root. Updated each script to resolve the correct project or Worker directory, and verified both moved scripts point to their intended locations and pass shell syntax checks. Added ignore rules for screenshots and kept credentials out of committed source files.

Files touched:
- app.py
- index.html
- Run.command
- cloudflare/deploy-worker.command
- deploy-github.command
- resources/eye-open.svg
- resources/eye-closed.svg
- .gitignore

## 2026-08-12 — Cloud sync, encryption, deployment, and desktop build

Added Cloudflare D1 synchronization for HamsterGo. Travel state is encrypted in the browser with AES-GCM before upload; the encryption password is kept locally on the device and is not sent to Cloudflare. Sync requests now send the sync code through the Authorization header instead of putting it in the new request URL. The legacy /record/<sync-key> endpoint remains available for compatibility.

Added automatic upload after local changes, a compact sync status light in the header, password visibility toggles, and an advanced sync settings section containing the sync tools. The current daily workflow remains sync code plus encryption password; the experimental account API is not shown in the frontend.

Added a PyWebView macOS desktop build flow. command/build.command builds dist/HamsterGo.app with resources/icon-1024.png; temporary PyInstaller output and dist/HamsterGo are removed after a successful build. The local desktop server uses a stable localhost port so browser storage can persist between launches.

Added separate deployment entry points:
- deploy-github.command for the frontend GitHub push workflow
- deploy-worker.command for Cloudflare Worker deployment

Files touched:
- index.html
- app.py
- cloudflare/src/index.js
- cloudflare/migrations/0002_add_encrypted_payload.sql
- cloudflare/migrations/0003_add_accounts.sql
- command/build.command
- deploy-worker.command
- deploy-github.command
- dev-log.md

## 2026-08-05 — 航班資訊與最近航班顯示

新增可收合的航班資訊列：主頁顯示最近一班尚未出發的航班，飛機 icon 可進入／完成編輯；編輯模式至少保留兩班航班，支援新增與移除。航班資料包含航班編號、出發時間、機場／航廈，並支援匯出與匯入。出發時間使用純數字輸入，會即時格式化；主頁摘要以 12 小時制顯示 AM／PM，已出發航班會自動隱藏。

編輯中的航班表單不會被定時更新重建，避免輸入焦點跳動；收合與編輯狀態使用相同的飛機按鈕切換。
手機主頁航班摘要改為兩行顯示：第一行為航班編號與出發時間，第二行為機場／航廈；編輯中各航班列即時更新，主頁摘要則在完成編輯後更新。
時間欄位新增分隔符號 Backspace 處理，刪除日期或時間時不會卡在斜線、逗號或冒號上，並兼容手機瀏覽器。

Files touched:
- index.html
- dev-log.md




## 2026-08-05 — 統一證件完成用字

將證件完成狀態與操作按鈕統一使用「已收好」，移除「已收妥」、「已確認收好」與「檢查已收好」等不同說法。

**Files touched**:
- `index.html`
- `dev-log.md`

## 2026-08-05 — 再次檢查改為上中下排列

依手機操作調整再次檢查視窗：移動與回程按鈕垂直排列，取消按鈕置於最下方並維持短版圓角樣式。

**Files touched**:
- `index.html`
- `dev-log.md`

## 2026-08-05 — 優化再次檢查視窗排版

移動與回程改為並排模式卡片，縮窄選擇視窗；取消按鈕改為短版圓角樣式，減少視覺上的延伸感。

**Files touched**:
- `index.html`
- `dev-log.md`

## 2026-08-05 — 移除再次檢查選項 tooltip

移除移動與回程選項的滑過提示，避免重複顯示說明。

**Files touched**:
- `index.html`
- `dev-log.md`

## 2026-08-05 — 簡化再次檢查選擇視窗

移除移動與回程的證件說明文字，選項只保留圖示與模式名稱；保留「取消」文字，並改用較符合主題的低強調按鈕樣式。

**Files touched**:
- `index.html`
- `dev-log.md`

## 2026-08-05 — 回程提示副標題

回程模式有物品尚未確認時，副標題顯示「別忘了把所有東西帶回家」。

**Files touched**:
- `index.html`
- `dev-log.md`

## 2026-08-05 — X 狀態不計入進度

統一所有模式的進度計算，標記為「X」的沒帶物品會從進度總數排除，不再增加完成進度；進度只反映已勾選與尚未確認的物品。

**Files touched**:
- `index.html`
- `dev-log.md`

## 2026-08-05 — 證件收好後鎖定清單

移除「行李確認了嗎？」完成提示，改由使用者自行控制。出發、回程與移動模式中，按下證件「已收好」或「檢查已收好」後，鎖定所有清單項目；保留 5 秒「返回」操作，返回後解除鎖定。

**Files touched**:
- `index.html`
- `dev-log.md`

## 2026-08-05 — 移動模式只剩證件提示

移動模式中，當其他物品都已確認、只剩證件尚未檢查時，顯示「只剩證件未確認」，副標題顯示「別忘了證件噢 👀」。

**Files touched**:
- `index.html`
- `dev-log.md`

## 2026-08-05 — 鎖定狀態保留原本顏色

清單鎖定後不再降低項目透明度，維持原本的文字與勾選顏色，只保留不可修改的互動狀態。

**Files touched**:
- `index.html`
- `dev-log.md`

## 2026-08-05 — 出發模式證件已帶上後恢復完成提示

一般出發模式中，證件已按「帶了」但尚未按「已收好」時，恢復顯示「行李都整理好了！ ✈️」；「只剩證件未確認」只在證件尚未按「帶了」時顯示。

**Files touched**:
- `index.html`
- `dev-log.md`

## 2026-08-05 — 統一只剩證件提示

出發、移動與回程模式在只剩證件尚未確認時，統一顯示「只剩證件未確認」，副標題顯示「別忘了證件噢 👀」。只有仍有其他物品未確認時，才顯示各模式的準備提示與數量。

**Files touched**:
- `index.html`
- `dev-log.md`

## 2026-08-05 — 確認鎖定只用於一般出發

「行李確認了嗎？」鎖定視窗只在一般出發模式的進度達到 100% 時出現。移動與回程模式保留重新檢查的用途，不跳出鎖定視窗，避免影響再次勾選。

**Files touched**:
- `index.html`
- `dev-log.md`

## 2026-08-05 — 修正再次檢查無法勾選

進入移動／回程模式時解除上一階段 100% 確認所造成的清單鎖定，確保再次檢查時可以重新勾選物品。

**Files touched**:
- `index.html`
- `dev-log.md`

## 2026-08-05 — 調整出發與移動副標題

「準備移動了！」下方顯示「移動前確認每一件物品都帶上了」；「要出發了！」下方顯示「出發前確認每一件東西都裝進行李」。

**Files touched**:
- `index.html`
- `dev-log.md`

## 2026-08-05 — 100% 進度確認與清單鎖定

進度達到 100% 時顯示「行李確認了嗎？」主題視窗。選「是，確認完成」會鎖定勾選／打叉狀態；選「否，繼續檢查」則維持可編輯。回程不再顯示「放在隨身包方便檢查。」副標題。

**Files touched**:
- `index.html`
- `dev-log.md`

## 2026-08-05 — 統一移動與出發的待確認提示

移動模式改為與一般出發相同的標題結構：標題顯示「準備移動了！」，第二行顯示「還有 X 件物品尚未確認」，不再為只剩證件時另設特殊標題或副標題。

**Files touched**:
- `index.html`
- `dev-log.md`

## 2026-08-05 — 調整移動模式提示層級

移動模式尚有多項物品未確認時，標題顯示「準備移動了！」、副標題顯示未確認數量；只剩證件時，改顯示「證件尚未檢查！」與「別忘了證件噢 👀」。

**Files touched**:
- `index.html`
- `dev-log.md`

## 2026-08-05 — 證件完成後五秒返回

證件標記完成後顯示五秒「返回」按鈕，可取消「已收好」但保留「帶了」狀態；五秒後按鈕自動消失，編輯模式的事後退回功能保留。

**Files touched**:
- `index.html`
- `dev-log.md`

## 2026-08-05 — 調整回程狀態提示

回程模式的提示分成三段：尚有物品未確認時顯示「準備回家！」，全部物品帶上但證件尚未收好時顯示「安心回家！」，證件按下「已收好」後顯示「Bon voyage! 🛫」。

**Files touched**:
- `index.html`
- `dev-log.md`

## 2026-08-05 — 調整回程完成前提示

回程模式在證件按下「帶了」後的提示由「安心回家！」改為「準備回家了」。

**Files touched**:
- `index.html`
- `dev-log.md`

## 2026-08-05 — 縮短移動模式證件按鈕

「檢查已收好」按鈕改為依文字內容自動寬度，不再撐滿證件列右側空間。

**Files touched**:
- `index.html`
- `dev-log.md`

## 2026-08-05 — 調整移動模式按鈕文字

移動模式的證件確認按鈕由「證件已確認收好」改為「檢查已收好」。

**Files touched**:
- `index.html`
- `dev-log.md`

## 2026-08-05 — 區分移動與回程的證件流程

移動模式的證件預設視為已帶上，只顯示「證件已確認收好」單一確認項目，按下後才計入移動進度。回程模式則與一般出發相同，證件從「帶了」與「已收好」都未選開始，依序完成後顯示「安心回家！」與「Bon voyage! 🛫」。

**Files touched**:
- `index.html`
- `dev-log.md`

## 2026-08-05 — 調整證件提醒語氣

移動模式中證件尚未收好時，下方提醒由操作說明改為「別忘了收好證件噢 👀」。

**Files touched**:
- `index.html`
- `dev-log.md`

## 2026-08-05 — 出發完成提示改為 Bon voyage

正常出發完成後的提示改為「Bon voyage! 🛫」，移動模式仍顯示「可以移動了！」。

**Files touched**:
- `index.html`
- `dev-log.md`

## 2026-08-05 — 出發提示使用起飛圖示

出發完成提示採用較符合中文介面的「一路順風！」，並將飛機圖示由 `✈️` 改為代表起飛的 `🛫`。

**Files touched**:
- `index.html`
- `dev-log.md`

## 2026-08-05 — 出發完成提示

一般出發流程在所有行李確認完成、證件按下「② 已收好」後，完成提示改為「一路順風！ ✈️」；移動模式仍使用「可以移動了！」。

**Files touched**:
- `index.html`
- `dev-log.md`

## 2026-08-05 — 回程證件改為手動確認

移動與回程模式開始時，證件的「帶了」與「已收好」都保持未選。回程按下「帶了」後顯示「安心回家！」，到機場再按「已收好」才顯示「Bon voyage! 🛫」。

**Files touched**:
- `index.html`
- `dev-log.md`

## 2026-08-05 — 區分已帶上與證件已收好

進度標籤由「已確認」改為「已帶上」。移動模式在所有物品帶上但證件尚未按「② 已收好」時，會顯示「證件尚未收好！」與操作提示；完成證件收好後才顯示「可以移動了！」。

**Files touched**:
- `index.html`
- `dev-log.md`

## 2026-08-05 — 移動與回程情境卡片

將再次檢查視窗的「移動／回程」選項改為符合 HamsterGo 主題的情境卡片，使用同等層級的票券風格選擇，不再以一般主要／次要按鈕呈現。

**Files touched**:
- `index.html`
- `dev-log.md`

## 2026-08-05 — 再次檢查加入移動與回程模式

「再次檢查」現在會先顯示主題確認視窗，讓使用者選擇「移動」或「回程」。移動模式需要再次確認證件是否已收好；回程模式則將證件視為已帶上，不要求再次確認「已收好」。完成提示改為「行李都整理好了！ ✈️」，避免暗示已經通過安檢。

**Files touched**:
- `index.html`
- `dev-log.md`

## 2026-08-05 — 調整備用隱形眼鏡間距

增加備用隱形眼鏡數字輸入框與下一個設定區塊之間的垂直間距，改善設定面板的閱讀層次。

**Files touched**:
- `index.html`
- `dev-log.md`

## 2026-08-05 — 調整備用隱形眼鏡設定介面

設定面板的欄位標題改為「備用隱形眼鏡」，下方直接顯示可編輯的數字輸入框，移除額外的「備用數目」文字。

**Files touched**:
- `index.html`
- `dev-log.md`

## 2026-08-05 — 再次檢查自動帶上證件

進入「再次檢查」時，依國內線或國際線自動選用駕照錢包或護照，並直接標記為「① 帶了」；使用者只需要再次確認「② 已收好」。

**Files touched**:
- `index.html`
- `dev-log.md`

## 2026-08-05 — 再次檢查時排除沒帶項目

按下「再次檢查」進入移動模式後，標記為沒帶（X）的項目不再計入進度分子或分母；尚未確認的項目仍會列入待確認數量。一般打包模式的原有進度計算維持不變。

**Files touched**:
- `index.html`
- `dev-log.md`

## 2026-08-05 — 隱形眼鏡備用數目設定

在設定面板加入「隱形眼鏡／備用數目」，預設為 2，可自行調整 0–30。日拋隱形眼鏡數量現在依「行程天數 + 備用數目」計算，設定會保存並隨旅行 JSON 匯出／匯入。

**Files touched**:
- `index.html`
- `dev-log.md`

## 2026-08-05 — 新旅程自訂確認視窗

將雙點倉鼠開始新旅程時的瀏覽器原生確認視窗，改成符合 HamsterGo 主題的自訂 modal；支援取消、點背景關閉與 Esc 關閉。

**Files touched**:
- `index.html`
- `dev-log.md`

## 2026-08-05 — 日拋隱形眼鏡預設數量

日拋隱形眼鏡的預設數量改為行程天數加 2，作為額外備用量；例如 3 天行程預設顯示 5。

**Files touched**:
- `index.html`
- `dev-log.md`

## 2026-08-05 — 桌面版倉鼠游標

桌面滑鼠移到倉鼠圖片時維持一般箭頭游標，不顯示可點擊的手指游標；雙點／雙擊開始新旅程的功能保留。

**Files touched**:
- `index.html`
- `dev-log.md`

## 2026-08-05 — 移動提示與新旅程操作

**變更**：

1. 再次檢查模式的提示詞改為「準備移動了！還有 n 件物品尚未確認」，完成後顯示「可以移動了！」；一般打包流程的提示詞維持不變。
2. 倉鼠圖支援手機雙點／桌面雙擊，會跳出確認視窗，確認後開始新的旅程。
3. 開始新的旅程會清除勾選、打叉、證件狀態、再次檢查狀態與旅程標題；自訂項目與其他設定保留。
4. 旅程標題欄改用較不容易觸發瀏覽器姓名自動填寫的欄位名稱與自動填寫設定。
5. 本次未修改「沒帶項目是否計入進度」的邏輯。

**Files touched**:
- `index.html`
- `dev-log.md`

## 2026-08-05 — 更新 HamsterGo PWA App Icon

**變更**：

1. 將新的 `hamster_boarding_pass_1024x1024_2.png` 重新命名為 `resources/hamster_boarding_pass_current.png`，作為目前的 icon 原始圖。
2. 由新的原始圖重新產生 PWA icon：
   - `resources/icon-512.png`（512×512）
   - `resources/icon-192.png`（192×192）
3. 將 `resources/old/` 內所有舊圖片加上 `archived-` 前綴，避免與目前使用中的 icon 混淆。
4. `manifest.json` 與 `index.html` 繼續使用 `icon-192.png` 和 `icon-512.png`，不需要更改參照路徑。

**Files touched**:
- `dev-log.md`
- `resources/icon-192.png`
- `resources/icon-512.png`
- `resources/hamster_boarding_pass_current.png`
- `resources/old/*`

## 2026-07-26 — Final controls, recheck behavior, and icon organization

**What changed**:

1. Added a top-level briefcase icon for 「開始新的旅程」 while keeping the footer action; removed the top export icon and kept JSON export inside Settings. The product title no longer includes the hamster emoji.
2. Added the final recheck behavior: the recheck control appears only after packing is complete and the document is stowed; in recheck mode, crossed-out items and baggage toggles are locked, while packed items can be checked or unchecked for the new pass.
3. Added edit-mode recovery for a document marked 「已收妥」, returning it to 「帶了」 without losing the packed state. Section 05 now auto-collapses when complete and supports manual expand/collapse.
4. Refined the recheck icon and kept its source as `resources/recheck.svg`, with a matching inline copy in `index.html` for direct file opening. Each custom SVG has an individual file under `resources/`; the old `resource/` directory was renamed.
5. Disabled autofill for the add-item name field with `name="item"` and `autocomplete="off"`.

**Files touched**:
- `index.html`
- `manifest.json`
- `service-worker.js`
- `README.md`
- `README.en.md`
- `dev-log.md`
- `resources/*.svg`

## 2026-07-26 — Recheck flow, packing controls, and resource icons

**What changed**:

1. Added the final packing flow: the document's 「① 帶了」 state counts toward progress immediately, while 「② 已收好」 is required before the recheck control appears. Edit mode can undo 「已收妥」 without removing the packed state.
2. Added recheck mode for hotel/home transitions: crossed-out items remain locked, blank items can be checked or unchecked, and baggage toggles plus flight instructions are locked or hidden.
3. Added automatic Section 05 collapse when all reminders are checked, with a manual chevron expand/collapse control.
4. Reorganized the top controls into Start New Trip, Add, Edit, Export, and Settings icons; the footer Start New Trip button remains available.
5. Added the normal item quantity field behavior: numbers are plain text outside edit mode, inputs with steppers appear in edit mode, and empty/zero quantities stay blank.
6. Added 「洗漱袋」, 「藥品袋」, and 「充電袋」 as regular checklist items.
7. Reworked the add dialog to a centered, solid modal with custom Add/Cancel buttons, backdrop/Esc closing, and mobile-safe sizing.
8. Renamed `resource/` to `resources/`; each custom SVG now has an individual copy in `resources/`, while inline SVG remains in `index.html` so direct file opening still works.

**Files touched**:
- `index.html`
- `README.md`
- `README.en.md`
- `manifest.json`
- `service-worker.js`
- `resources/*.svg`

## 2026-07-26 — Trip naming, JSON backup, and compact controls

**What changed**:

1. Added a visible trip-title field beside the trip-day input. The title is saved locally and is used as the exported JSON filename.
2. Added JSON travel-data export and import:
   - the header now has an icon-only quick export button
   - the Settings panel contains labelled 「匯出 JSON」 and 「匯入 JSON」 actions under a new 「旅行資料」 heading
   - imported files restore the checklist, custom items, baggage settings, trip title, and other travel state
3. Added four local font-size options in the Settings panel and persisted the selection in the browser.
4. Reworked the top controls: the brand is now `HamsterGo · 倉鼠打包小幫手 🐹`, the gear icon is smaller, and the trip days are a direct 1–30 number input with no spinner arrows or capsule wrapper.
5. Disabled browser autofill for the trip title field and kept the existing localStorage-first behavior.

**Files touched**:
- `index.html`
- `manifest.json`
- `README.md`

## 2026-07-26 — Status prompts, simplified quantities, and reminder-only prep section

**What changed**:

1. The top headline now acts as a simple trip-status prompt instead of a raw percentage label:
   - `🐹 今天要出發了！還有 n 項沒帶。` while packing
   - `🐹 行李整理完成！ ✈️` once the main checklist is done
   - Section 05 is excluded from the main completion math, and crossed-out items (`X`) are not counted as missing
2. Removed the `Boarding Complete` final state/button. The UI now ends at `行李整理完成！ ✈️` and uses `再次檢查` to clear checked items while preserving crossed-out items.
3. Quantity handling was simplified:
   - clothing quantities now render as plain numbers
   - daily contact lenses show numbers again
   - new custom items can choose `不顯示 / 固定數量 / 跟天數走`
   - the quantity editor is now focused on clothing, while custom-item quantities are set at creation time
4. Section 05 was renamed into a reminder-only `TRIP PREP 出發前準備` block with Chinese-only items like clearing the fridge, taking out trash, charging electronics, turning off lights/appliances, and checking documents/flight details.
5. The yellow dot before the hamster in the top status line was removed, and the headline was tightened to avoid clipping on longer two-digit status messages.

6. The edit controls were reorganized:
   - 「編輯」 now sits to the left of 「再次檢查」 in the footer and has a clearer touch target.
   - Editing mode shows one shared add panel at the bottom instead of one add row per section.
   - Users choose a major section first; selecting section 03 reveals its subcategory picker.
7. Added subtle visual separation for custom items, the add panel, and section 05. The 🐹 was removed from the top brand line, while status prompts keep their hamster emoji.
8. Moved HamsterGo images into `resources/`, including the current 192/512 PWA icons and the retained candidate logo `hamstergo-logo-candidate.png`.
9. Updated the Service Worker to use a stable cache name with network-first fetching and cached offline fallback, so future deployments do not require manually incrementing a cache version.

**Files touched**:
- `index.html`
- `manifest.json`
- `service-worker.js`
- `README.md`
- `README.en.md`
- `resources/icon-192.png`
- `resources/icon-512.png`
- `resources/hamstergo-logo-candidate.png`

# Dev Log

開發過程中的重要決定與變更紀錄，新的在最上面。

## 2026-07-14 — 修正新增項目類別選單在手機上貼太緊底部

**問題**：編輯模式下新增項目時，Carry-on 分類會跳出類別選單，在手機上會變成從底部滑出的 bottom sheet（`.cat-select-list.mobile-sheet`）。因為 Carry-on 有 5 個分類，選單較長，最後一個選項「重要物品」會頂到螢幕最下面，跟 Home 指示條/手勢列太貼近。

**原因**：sheet 的下方 padding 只有 `10px + env(safe-area-inset-bottom, 0px)`。`safe-area-inset-bottom` 只有在「加到主畫面、以 standalone PWA 執行」且裝置有底部安全區（例如有 Home 指示條的 iPhone）時才會是非 0 值；用一般手機瀏覽器分頁打開時這個值是 0，所以實際下方留白只有 10px，太窄。

**修改**：把底部 padding 的基礎值從 `10px` 提高到 `24px`（`env(safe-area-inset-bottom, 0px)` 仍疊加在上面），讓最後一個選項在任何情況下都有足夠留白，不再只依賴安全區變數。
- `index.html` → `.cat-select-list.mobile-sheet` 的 `padding` 屬性。

## 2026-07-14 — Carry-on / Checked Baggage 開關與衣物自動歸類

**背景**：原本 Carry-on（手提行李）一律顯示、沒有開關；只有 Checked Baggage（托運行李）有一個手動開關，預設關閉，且衣物永遠放在 Carry-on 底下，不會因為有沒有托運而變動。

**變更**：

1. Carry-on 新增一個獨立開關「這趟有手提行李」，UI 與行為都跟原本的「這趟有托運」開關一致（`index.html` 的 `carryOnSection` / `carryOnToggle`）。
2. 兩個開關的預設值改成跟著國內線／國際線切換：
   - 國內線：手提行李 **開**、托運 **關**
   - 國際線：手提行李 **開**、托運 **開**
   - 切換國內/國際線按鈕時會自動套用上面的預設值，但使用者仍可手動覆寫（例如國內線也可以手動打開托運）。
3. 衣物類（上衣／襪子／內褲／褲子／外套／鞋子 or 拖鞋）改成動態歸類：只要「托運」開關是開的，這一整個分類就會出現在 Checked Baggage 底下；托運關掉時則回到 Carry-on 底下。其他分類（洗漱品和藥品、電子用品、旅行雜物、重要物品）不受影響，永遠跟著 Carry-on 開關走。
   - 實作方式：`getData()` 裡先組好 `clothesCat`，再依 `state.checkedEnabled` 決定 `unshift` 進 `carryCats` 或 `checkedCats`，其餘畫面/進度計算邏輯（`render()`、`allItemIds()`）都是照著 `getData()` 回傳的結構走，不用額外特判衣物。
4. `allItemIds()`（用來算「已確認 X / Y」進度）原本只針對 `checkedEnabled` 特判，現在改成先算出目前真正會顯示的分類 key 集合（`visibleCatKeys`），再用這個集合去篩自訂項目，同時處理 Carry-on 開關關閉、以及衣物分類搬家兩種情況。

**中途來回修正的點**（記錄一下避免之後看 code 誤會）：
- 一開始需求是「國內線兩個開關都關、國際線都開」，後來改成「國內線托運預設開」，最後定案是「國內線手提行李開、托運關；國際線兩個都開」。目前 code 就是最後這個版本，`index.html` 裡 `#flightToggle` 的 click handler 是唯一決定預設值的地方：`carryOnEnabled` 固定 `true`，`checkedEnabled` 等於 `flightType === 'international'`。

**測試方式**：這個 sandbox 沒有 root 權限，裝不了 Playwright/Chromium 需要的系統依賴（`libnss3` 等），沒辦法開真的瀏覽器截圖驗證。改用 `jsdom` 把實際的 `index.html` 整份載進去執行（`runScripts: 'dangerously'`），直接對真正的 DOM 元素 `dispatchEvent(new Event('click'))` 模擬使用者點擊「國際線／國內線」「這趟有手提行李」「這趟有托運」，再檢查對應 section 是否顯示、衣物分類跑到哪個 section 底下。跑過的情境：
1. 國內線初始狀態
2. 切到國際線
3. 切回國內線
4. 國內線手動關閉手提行李
5. 國內線手動開啟托運（驗證衣物搬家）

全部行為符合預期，過程中沒有 console error。
