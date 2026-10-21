# FitLife｜編譯與基本執行驗證

[返回作品首頁](../README.md)

## 驗證依據

本頁整理已完成的 GitHub Actions 執行紀錄，不以原始碼推測測試成功，也不代表後續版本自動具有相同結果。

| 項目 | 紀錄 |
|---|---|
| 執行日期 | 2026-10-21 |
| 工作流程 | FitLife isolated verification |
| 工作 | build-and-smoke |
| 執行結果 | Success |
| 執行環境 | Ubuntu 24.04；.NET SDK 8.0.426 |
| 驗證分支 | `verification/fitlife-cleanup-20261021` |
| 驗證提交 | `816b969e02d95bfaa5a532f490056f3b99befc26` |
| 應用程式基準提交 | `3269c8523810d4625184a069a6a20c388a1ff41b` |

來源：[執行紀錄](https://github.com/z1oyi0/fitlife-Mvc/actions/runs/39611972925)、[工作與日誌](https://github.com/z1oyi0/fitlife-Mvc/actions/runs/39611972925/job/119262886511)、[當次驗證腳本](https://github.com/z1oyi0/fitlife-Mvc/blob/816b969e02d95bfaa5a532f490056f3b99befc26/.github/workflows/verify-fitlife.yml)。

驗證提交只比基準提交新增 `.github/workflows/verify-fitlife.yml`，未修改應用程式：[版本差異](https://github.com/z1oyi0/fitlife-Mvc/compare/3269c8523810d4625184a069a6a20c388a1ff41b...816b969e02d95bfaa5a532f490056f3b99befc26)。

## 還原、編譯及啟動

1. `dotnet restore MVC_Homework.sln`：完成套件還原。
2. `dotnet build MVC_Homework.sln --configuration Release --no-restore`：編譯成功，日誌為 0 個編譯警告、0 個編譯錯誤。
3. 應用程式在 Development 環境啟動，監聽 `http://127.0.0.1:5080`。

「0 個警告」僅指該次編譯摘要；執行環境仍有開發用 Data Protection 金鑰儲存與 Actions 執行器版本等警告，不能將編譯結果解讀為安全審查通過。

## 8 項 HTTP 基本檢查

| 編號 | 操作 | 實際檢查 | 結果 |
|---|---|---|---|
| 1 | `GET /Login/Index` | HTTP 200，回應含 `form` | 通過 |
| 2 | `GET /css/site.css` | HTTP 200 | 通過 |
| 3 | `POST /Login/Index`，錯誤測試帳密 | HTTP 200 | 通過 |
| 4 | `POST /Login/Index`，既有示範帳密 | HTTP 302 | 通過 |
| 5 | `GET /Home/Index` | HTTP 200 | 通過 |
| 6 | `GET /MealRecords/Create` | HTTP 200 | 通過 |
| 7 | `GET /ExerciseRecords/Create` | HTTP 200 | 通過 |
| 8 | `GET /Login/Logout` | HTTP 302 | 通過 |

測試使用 CookieJar 保留同一段操作中的 Cookie，且不自動跟隨重新導向。除了第 1 項確認回應含表單文字，其餘主要檢查 HTTP 狀態碼；這是基本啟動／頁面可達性檢查，不是完整功能或登入安全驗證。

## 未涵蓋的範圍

- 未連接 SQL Server，也沒有使用正式資料庫憑證。
- 未送出新增、編輯或刪除紀錄的資料庫操作。
- 未核對搜尋、分頁、熱量加總與圖表數值是否符合測試資料。
- 未啟動完整瀏覽器驗證 JavaScript／Chart.js 的實際繪製。
- 未完成使用者隔離、存取權限、防 CSRF、效能或安全性測試。
- 未產出真實操作截圖或 Demo 影片。

## 後續測試項目（尚未執行）

| 項目 | 驗證方向 |
|---|---|
| SQL Server 連線與資料表 | 使用本機測試資料庫，確認兩個模型對應的表及欄位可讀寫 |
| 飲食及運動 CRUD | 新增、查詢、編輯、刪除後重新讀取，核對資料庫中的結果 |
| 查詢與分頁 | 檢查空結果、關鍵字、第一頁與最後一頁，以及不合理頁碼 |
| 熱量加總 | 對照目前頁面紀錄的加總，區分頁面小計與全資料集總計 |
| 圖表 | 使用可核對的測試紀錄，確認橫軸、數值及空資料情況 |
| 安全性 | 在修正驗證、授權與請求處理後，加入對應的正反向測試 |

## 整理紀錄

課程原始程式保留為個人作品；後續作品集文件修訂、重複檔整理與驗證工作流程建立使用 AI 協助。本頁記錄的是 2026-10-21 的實際驗證結果，並非課程開發當時的除錯歷程。2026-10-22 的文件整理未改動應用程式，也未重新執行上述工作流程。
