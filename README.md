# HamsterGo · 倉鼠出行日

一個純前端的行李打包檢查清單，設計成登機證（boarding pass）的樣式，專為「帶倉鼠出門」的行程設計。可以安裝到手機主畫面，當作一般 App 使用。

## 功能

- **依天數自動計算數量**：襪子、上衣、內褲、隱形眼鏡（含備用）會依你設定的行程天數自動顯示需要帶幾份
- **打勾追蹤進度**：畫面上方會顯示目前已裝箱的比例
- **證件流程**：預設國內線（駕照錢包），可切換國際線（護照）；按下「① 帶了」後，國際線／國內線切換鈕會自動隱藏，按「② 已收好」才算完成
- **編輯模式**：可以在每個分類底下自行新增項目，新增時可選擇是否要「跟天數走」；已新增的項目可以改名或刪除。原始清單項目維持固定，不能刪改
- **通關提醒**：出發前 / 安檢後兩個時間點的證件提醒
- **本機儲存**：勾選狀態、天數設定、自訂項目都存在瀏覽器的 `localStorage`，只留在你自己的裝置上，不會上傳到任何伺服器
- **可安裝成 PWA**：加到手機主畫面後可全螢幕開啟，並透過 Service Worker 做離線快取

## 檔案結構

```
.
├── index.html          # 主要頁面與邏輯
├── manifest.json        # PWA 設定（名稱、圖示、顏色、啟動模式）
├── service-worker.js    # 離線快取邏輯
├── icon-192.png         # App 圖示（192×192）
├── icon-512.png         # App 圖示（512×512）
└── deploy.command       # 雙擊即可 commit + push 到 GitHub 的部署腳本
```

## 本機測試

因為 Service Worker 需要 HTTPS 或 localhost 才能註冊，不能直接雙擊 `index.html` 用 `file://` 打開測試。用任何簡易的本機伺服器起一個就好，例如：

```bash
python3 -m http.server 8000
```

然後瀏覽器打開 `http://localhost:8000`。

## 部署到 GitHub Pages

第一次設定：

1. 建立一個新的 GitHub repository（Public）
2. 在這個資料夾執行 `git init`，並加上這個 repo 的 remote（`git remote add origin <repo網址>`）
3. 把這幾個檔案 commit 並 push 上去（放在 repo 根目錄，不要包在子資料夾裡）
4. 到 repo 的 **Settings → Pages**，Source 選 **Deploy from a branch**，Branch 選 **main** / **root**，儲存
5. 等 1–2 分鐘後，會拿到一個網址：`https://你的帳號.github.io/repo名稱/`
6. 手機瀏覽器打開這個網址 → 加到主畫面，即可像 App 一樣全螢幕使用

之後每次修改完，雙擊 `deploy.command`，輸入這次改了什麼、要不要打版號，就會自動 commit + push。

## 資料儲存說明

所有資料都存在**這支手機、這個瀏覽器**裡（`localStorage`），不會同步到其他裝置，也不會有任何人（包含開發者）看到你的資料。清除瀏覽器資料或換手機都會讓資料重置。

## 客製化

- 想調整清單項目、分類，直接編輯 `index.html` 裡的 `DATA` 這個 JavaScript 陣列
- 想換配色，改 `index.html` 最上面 `:root` 裡的 CSS 變數（`--navy`、`--amber` 等）
- 想換圖示，重新產生 `icon-192.png` / `icon-512.png` 並保持相同檔名即可
