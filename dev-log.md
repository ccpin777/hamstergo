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
8. Moved HamsterGo images into `resource/`, including the current 192/512 PWA icons and the retained candidate logo `hamstergo-logo-candidate.png`.
9. Updated the Service Worker to use a stable cache name with network-first fetching and cached offline fallback, so future deployments do not require manually incrementing a cache version.

**Files touched**:
- `index.html`
- `manifest.json`
- `service-worker.js`
- `README.md`
- `README.en.md`
- `resource/icon-192.png`
- `resource/icon-512.png`
- `resource/hamstergo-logo-candidate.png`

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
