# HamsterGo · Problems and Follow-up Notes

這份文件記錄目前已確認、但尚未處理的問題。內容以目前程式狀態為準，之後修正功能或文件時可逐項更新。

## Priority 1 · 文件與實際功能不一致

### Cloudflare README 過時

`cloudflare/README.md` 仍寫著目前只有同步碼，且還沒有帳號密碼系統；但 Worker 已經包含：

- `/auth/register`
- `/auth/login`
- `/auth/logout`
- `/auth/me`
- `/me/record`
- `users` 與 `sessions` 資料表 migration

需要決定帳號功能是：

1. 正式啟用並補完整文件；或
2. 保留為實驗功能並明確標示；或
3. 移除帳號 API，只保留同步碼模式。

目前前端帳號欄位被 CSS 隱藏，主要使用流程仍是同步碼模式。

### 版本與 build 顯示來源分散

`version.py` 是目前的版本來源，但 `index.html` 仍有直接寫入的 `Version 1.0` 與 `Build 10`。之後若版本變更，應避免只更新其中一處。

## Priority 1 · 同步與資料安全

### 同步是整份狀態覆蓋

目前上傳與下載的是整份旅程 state，不是逐筆資料合併。兩台裝置同時修改時，後上傳的資料可能覆蓋較早的資料。

需要考慮：

- 遠端版本較新時是否提示使用者
- 是否需要確認後才覆蓋本機資料
- 是否保存上一份同步備份
- 未來是否改成逐筆或欄位級合併

### 自動同步缺少完整衝突處理

目前有延遲自動上傳機制，但沒有完整的遠端版本檢查與衝突解決流程。自動上傳可能覆蓋另一台裝置剛完成的修改。

### Worker 的來源限制過寬

`cloudflare/wrangler.jsonc` 目前使用：

```json
"ALLOWED_ORIGIN": "*"
```

正式部署時應限制為實際使用的網站來源，避免不必要的跨來源存取範圍。

### 舊式同步 endpoint 仍存在

Worker 同時保留以 sync key 作為 URL 路徑的 `/record/<key>` endpoint。同步碼本身等同存取權杖，應評估是否移除這種容易出現在 URL、log 或瀏覽器歷史紀錄中的形式，只保留 Authorization header。

### 舊版明文資料相容性

資料庫 migration 仍保留舊的 `state_json` 欄位，而目前新版下載流程會拒絕 legacy plaintext record。需要決定：

- 是否提供一次性的加密升級流程
- 是否明確放棄舊資料
- 是否移除不再使用的欄位與相容程式碼

## Priority 2 · 架構維護

### `index.html` 責任過多

目前 `index.html` 同時包含：

- HTML markup
- CSS
- UI rendering
- state management
- localStorage
- JSON import/export
- encryption
- cloud sync
- account API calls

未來若繼續增加功能，維護成本會快速上升。可以逐步拆成：

```text
frontend/
  views/
  state/
  storage/
  sync/
```

不需要一次重寫，但新增功能應避免再把所有邏輯放回同一個檔案。

### 桌面偏好與旅程資料分散

桌面版透過 pywebview API 將同步與字體等偏好保存到 macOS Application Support；主要旅程狀態則由頁面端保存。未來應文件化哪些資料存在 native preferences、哪些資料存在 localStorage，以及備份／清除資料時兩者的關係。

## Priority 2 · PWA 與桌面版

### Service Worker 快取策略需要持續檢查

Service Worker 會快取頁面與資源，但使用者可能因快取而暫時看不到最新版本。每次發布需要確認：

- `CACHE_NAME` 是否更新
- 新增資源是否加入快取清單
- 舊版快取是否能正確清除
- GitHub Pages 與桌面版是否載入相同版本

### PWA 與桌面版的資料行為不同

PWA 使用瀏覽器儲存；桌面版使用 pywebview 的頁面環境，另外還有 native preferences。若未來共用更多功能，需要測試兩種環境的 localStorage、檔案匯入匯出與同步行為是否一致。

## Priority 3 · 文件整理

- Root README 已說明目前的本機優先與選擇性同步，但 `cloudflare/README.md` 需要同步更新。
- README 應區分目前可見功能、選擇性同步功能與實驗中的帳號 API。
- 若同步功能正式使用，應補充如何停止同步、如何清除遠端資料，以及如何處理遺失同步碼或加密密碼。
- 若未來進行架構拆分，應同步更新 README 的檔案結構與開發指引。

