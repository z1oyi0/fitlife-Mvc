# FitLife｜健康生活管理系統

**林以甯｜元智大學資訊管理學系｜個人課程作品**

以 C#、ASP.NET Core MVC 與 SQL Server 製作的飲食及運動紀錄網站。專案練習 MVC 分層、Entity Framework Core 資料存取、Razor 頁面與 Chart.js 圖表，包含紀錄的新增、查詢、編輯及刪除程式。

**最新驗證：** 2026-10-22（臺灣時間）已在隔離 SQL Server 與 Chromium 完成實測。35 項檢查中 26 項通過、9 項未通過；正常資料 CRUD 與圖表數值已驗證，但編輯／分頁、存取權限及輸入驗證仍有待修正問題。

[SQL 與瀏覽器實測報告](docs/SQL_BROWSER_VERIFICATION.md) · [本次 Actions 紀錄](https://github.com/z1oyi0/fitlife-Mvc/actions/runs/39666969329) · [先前編譯驗證](docs/VERIFICATION.md) · [安全說明](SECURITY_NOTES.md)

> 本儲存庫提供課程作品原始碼與技術說明，不是公開運作的線上服務。尚未正式部署，不能將部分功能測試通過視為全面安全或可直接上線。

## 個人實作範圍

此專案為個人課程作品，內容包含飲食與運動紀錄的 MVC 頁面、資料模型、資料操作與熱量呈現。下列入口對應目前保留的程式碼；課程實作與後續 AI 輔助驗證的範圍分開記錄。

## 功能與程式入口

| 功能 | 實作內容 | 原始碼 |
|---|---|---|
| 飲食紀錄 | 新增、關鍵字查詢、編輯、刪除，以及每頁 5 筆的清單分頁 | [MealRecordsController.cs](MVC_Homework/Controllers/MealRecordsController.cs) |
| 飲食清單與熱量 | 以 Razor 顯示紀錄，計算目前頁面傳入資料的熱量加總 | [飲食紀錄頁面](MVC_Homework/Views/MealRecords/Index.cshtml) |
| 運動紀錄 | 新增、關鍵字查詢、編輯與刪除 | [ExerciseRecordsController.cs](MVC_Homework/Controllers/ExerciseRecordsController.cs) |
| 運動圖表 | 將傳入頁面的運動紀錄轉為 Chart.js 折線圖資料 | [運動紀錄頁面](MVC_Homework/Views/ExerciseRecords/Index.cshtml) |
| 資料存取 | 使用 EF Core DbContext 對應飲食與運動資料模型 | [FitLifeDbContext.cs](MVC_Homework/Models/FitLifeDbContext.cs) |
| 示範登入 | 使用固定測試帳密及 Session 示範登入、登出流程，尚非正式帳號管理 | [LoginController.cs](MVC_Homework/Controllers/LoginController.cs) |

**統計範圍：** 飲食頁的熱量是目前頁面資料的加總，不是全部歷史紀錄或完整每日飲食總量；運動圖表顯示頁面取得的紀錄，不宣稱已完成獨立的每日彙總分析。

## 技術與資料流程

- **後端：** C#、.NET 8、ASP.NET Core MVC。
- **資料存取：** Entity Framework Core、SQL Server、LINQ 查詢。
- **畫面：** Razor、HTML、CSS、Bootstrap、JavaScript、Chart.js。

```text
瀏覽器提出請求
  → Controller 處理查詢或表單資料
  → EF Core／FitLifeDbContext 存取 SQL Server
  → Controller 將結果傳給 Razor View
  → 頁面顯示清單；運動頁以 Chart.js 呈現圖表
```

```text
MVC_Homework.sln
MVC_Homework/
├── Controllers/              登入、飲食與運動控制器
├── Models/                   資料模型與 FitLifeDbContext
├── Views/                    Razor 頁面與表單
├── wwwroot/                  CSS、JavaScript 與靜態資源
├── Properties/               本機啟動設定
├── Program.cs                服務、資料庫與路由設定
├── MVC_Homework.csproj        .NET 8 專案設定
└── appsettings.example.json  不含帳密的設定範例
```

## 驗證結果

| 項目 | 狀態 |
|---|---|
| NuGet 套件還原、Release 編譯 | 通過；當次編譯摘要 0 警告、0 錯誤 |
| SQL Server 連線、飲食及運動正常 CRUD | 隔離測試資料庫實測通過；未連原學校／正式資料庫 |
| 查詢結果、分頁與熱量 | 一般條件查詢、基本分頁與頁面小計通過；搜尋後翻頁、頁碼防呆與編輯餐別仍有問題 |
| Chart.js 瀏覽器繪製與數值 | 測試的日期與 180／260／320 kcal 均與 SQL Server 一致，查詢及空資料圖表通過 |
| 真實操作截圖 | 已擷取；正常動畫模式的整頁圖表完整，停用動畫的截圖有異常，詳見報告 |
| 基礎安全與輸入驗證 | 發現未登入讀寫、無權杖寫入、GET 刪除及無效數字／負值處理問題，未通過 |
| 正式部署與全面安全性驗證 | 未部署；目前不得視為可安全對外服務 |

完整結果、失敗案例、測試程式及版本見 [SQL Server 與瀏覽器實測報告](docs/SQL_BROWSER_VERIFICATION.md)。這些結果只代表指定測試資料與環境，不是所有輸入、瀏覽器或安全情境的保證。Actions 顯示 failure 是因為檢查確實發現問題，並非忽略失敗後標示成功。

## 操作畫面與測試附件

[本次執行頁面](https://github.com/z1oyi0/fitlife-Mvc/actions/runs/39666969329) 的 `fitlife-sql-browser-evidence` 附件包含實際瀏覽器截圖、逐項 JSON 結果、查詢資料比對與編譯紀錄；不是以生成圖片模擬執行結果。附件保留 14 天，下載可能需要登入 GitHub。

建議查看 `01-home.png`、`03-meal-list.png`、`04-meal-edit.png` 與 `chart-fullpage-allow.png`。所有顯示的飲食及運動內容都是測試資料。

## 本機執行

### 準備環境與資料庫

需要 .NET 8 SDK 及自己的 SQL Server 測試資料庫。[隔離驗證用建表 SQL](https://github.com/z1oyi0/fitlife-Mvc/blob/6b56bd728eb8a2ef3e37b88e5552b6cebe728206/verification/sql-browser/schema.sql) 依 C# 模型重建兩張表，僅用於全新的 `FitLifeVerification` 測試資料庫，不是原資料庫備份，也不要對既有正式資料庫執行。

- [MealRecord.cs](MVC_Homework/Models/MealRecord.cs)：對應 `TableMealRecords1132024`。
- [ExerciseRecord.cs](MVC_Homework/Models/ExerciseRecord.cs)：對應 `TableExerciseRecords1132024`。

資料表名稱保留課程原有命名。不要使用正式環境帳密或個人健康資料進行展示；CI 的一次性容器設定也不代表正式環境已完成權限規劃。

### 還原與編譯

在儲存庫根目錄執行：

```powershell
dotnet restore MVC_Homework.sln
dotnet build MVC_Homework.sln --configuration Release --no-restore
```

### 設定本機連線並啟動

以下以 Windows PowerShell 為例。連線字串中的 `YOUR_...` 均為佔位字，須改成自己的本機測試設定：

```powershell
cd MVC_Homework
dotnet user-secrets init
dotnet user-secrets set "ConnectionStrings:DefaultConnection" "Server=YOUR_SERVER;Database=YOUR_DB;User Id=YOUR_USER;Password=YOUR_PASSWORD;TrustServerCertificate=True;"
$env:ASPNETCORE_ENVIRONMENT = "Development"
dotnet run --configuration Release --no-launch-profile --urls "http://127.0.0.1:5080"
```

在瀏覽器開啟 `http://127.0.0.1:5080/Login/Index`。示範登入設定見登入控制器；僅供本機測試，不可沿用於正式服務。完成資料表設定前，飲食與運動清單或寫入操作可能失敗。

## 已知限制與後續改善

優先修正資料操作的驗證與授權、防 CSRF、GET 刪除及伺服器端輸入驗證，再處理餐別綁定、分頁搜尋條件與頁碼檢查；修正後應重跑同一套測試。詳細結果見 [實測報告](docs/SQL_BROWSER_VERIFICATION.md) 與 [安全說明](SECURITY_NOTES.md)。

本輪新增驗證與更新文件，沒有修改應用程式功能，也不宣稱上述問題已修好。
