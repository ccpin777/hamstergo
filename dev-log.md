# Dev Log

開發過程中的重要決定與變更紀錄，新的在最上面。

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
