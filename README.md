# 鄞宗誠醫師網站 Demo

以原始部落格為來源的靜態示範網站，使用 HTML、CSS 與 JavaScript，可部署於 GitHub Pages。

## 內容與範圍

- 收錄原部落格 115 篇文章，擷取日期為 2026-11-11。
- 文章標題只依設計要求統一全形標點。內文為原文文字擷取，沒有生成醫療摘要或修改醫療說法。
- 分類依原站分類頁的文章連結建立，標籤來自 Blogger feed。
- 醫師資料與照片來自原站個人簡介。
- 示範版未收錄文章圖片，文章頁保留原文連結。
- 門診時間、地址、地圖尚待確認，沒有推測或自行補上。
- 聯絡表單只做本機展示，不傳送、不儲存資料。
- 設有 noindex, nofollow，避免示範版與正式內容混淆。正式上線前應重新檢查門診資訊與搜尋設定。

內容為衛教分享，無法取代實際診察。

## 設計

已在 DESKTOP-95MCASJ 使用本機 UI UX Pro Max 的 design-system 搜尋與文字斷行 UX 指引。實際配色、字體、文字規則以提供的網站製作守則為準，相關決策記錄於 design-system。

## 本機執行與驗證

```sh
npm ci
npx playwright install chromium
npm run serve
```

在另一個終端機執行 `npm test`。測試涵蓋指定螢幕寬度、搜尋、篩選、分頁、選單、返回流程、示範表單、WCAG 自動檢查與原文一致性。自動檢查不能取代人工無障礙稽核或臨床審閱。

網站原始碼在 public。推送 main 後，由 GitHub Actions 部署該資料夾，不需要後端服務。

## 來源

- 原站：http://spineexpert.blogspot.com/?m=1
- 原站 feed：http://spineexpert.blogspot.com/feeds/posts/default?alt=json&max-results=150
- 個人簡介：https://www.blogger.com/profile/00538994561338350909
- 每篇文章的原始網址、日期及原標籤記錄於 public/data.json。

原站文章與醫師照片的權利屬於各自權利人，本專案未賦予第三方額外再利用授權。
