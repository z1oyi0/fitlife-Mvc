# FitLife｜健康生活管理系統

**林以甯｜元智大學資訊管理學系｜個人課程作品**

以 C#、ASP.NET Core MVC 與 SQL Server 製作的飲食及運動紀錄網站。專案練習 MVC 分層、Entity Framework Core 資料存取、Razor 頁面與 Chart.js 圖表，包含紀錄的新增、查詢、編輯及刪除程式。

**驗證摘要：** 2026-10-21 已通過套件還原、Release 編譯、網站啟動與 8 項 HTTP 基本檢查。這次檢查未涵蓋 SQL Server 實際讀寫、瀏覽器圖表或完整安全性測試。

[驗證結果與範圍](docs/VERIFICATION.md) · [GitHub Actions 執行紀錄](https://github.com/z1oyi0/fitlife-Mvc/actions/runs/39611972925) · [已知限制與安全說明](SECURITY_NOTES.md)

> 本儲存庫提供課程作品原始碼與技術說明，並非公開運作的線上服務；正式部署前仍須補強權限控制與完成整合測試。

## 個人實作範圍

此專案為個人課程作品，內容包含飲食與運動紀錄的 MVC 頁面、資料模型、資料操作與熱量呈現。下列入口對應目前保留的程式碼；功能的實作範圍與已執行的測試分開說明。

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
| NuGet 套件還原 | 通過 |
| Release 編譯（含 Razor） | 通過；該次編譯為 0 個警告、0 個錯誤 |
| 網站啟動、登入頁、靜態 CSS、示範登入及登出、首頁、新增表單 | 8 項 HTTP 基本檢查通過 |
| SQL Server 連線、資料新增／修改／刪除、查詢結果正確性 | 未納入上述測試 |
| Chart.js 瀏覽器繪製、數值正確性、操作截圖 | 未納入上述測試 |
| 正式部署及完整安全性驗證 | 尚未完成 |

測試執行於獨立驗證分支，應用程式碼與整理後的課程版本相同；不是對所有功能的測試保證。完整項目、測試版本及來源見 [驗證紀錄](docs/VERIFICATION.md)。

## 本機執行

### 準備環境與資料庫

需要 .NET 8 SDK，以及自己的 SQL Server 測試資料庫。目前未提供資料庫備份、建表 SQL 或種子資料；資料庫操作前須先依下列模型建立相符的資料表，不能只啟動網站就視為完成資料庫設定。

- [MealRecord.cs](MVC_Homework/Models/MealRecord.cs)：對應 `TableMealRecords1132024`。
- [ExerciseRecord.cs](MVC_Homework/Models/ExerciseRecord.cs)：對應 `TableExerciseRecords1132024`。

資料表名稱保留課程原有命名。不要使用正式環境的帳號、密碼或個人健康資料進行展示。

### 還原與編譯

在儲存庫根目錄執行：

```powershell
dotnet restore MVC_Homework.sln
dotnet build MVC_Homework.sln --configuration Release --no-restore
```

### 設定本機連線並啟動

以下以 Windows PowerShell 為例。連線字串中的 `YOUR_...` 均為佔位字，須改成自己的本機測試設定；這不是可直接使用的連線憑證。

```powershell
cd MVC_Homework
dotnet user-secrets init
dotnet user-secrets set "ConnectionStrings:DefaultConnection" "Server=YOUR_SERVER;Database=YOUR_DB;User Id=YOUR_USER;Password=YOUR_PASSWORD;TrustServerCertificate=True;"
$env:ASPNETCORE_ENVIRONMENT = "Development"
dotnet run --configuration Release --no-launch-profile --urls "http://127.0.0.1:5080"
```

在瀏覽器開啟 `http://127.0.0.1:5080/Login/Index`。示範登入設定見登入控制器；僅供本機課程測試，不可沿用於正式服務。完成資料表設定前，飲食與運動清單或寫入操作可能失敗。

## 已知限制與後續改善

目前登入為示範流程，資料操作的授權檢查、防 CSRF、刪除方法、表單驗證及資料庫整合測試仍須補強。公開原始碼不代表網站已安全部署；詳細範圍見 [安全性與限制](SECURITY_NOTES.md)。

後續重點是補齊可重建的測試資料庫、驗證 CRUD 與統計結果，再記錄真實瀏覽器操作畫面。本次文件更新沒有變更應用程式功能。
