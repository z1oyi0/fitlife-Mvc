# FitLife 健康生活管理系統｜ASP.NET Core MVC 課程作品

> 此儲存庫整理自課程作業原始碼，用於展示學習成果。**並非正式上線的產品**。此版本已排除原檔案中的資料庫連線憑證、IDE 快取與編譯產物。

## 專案概述

以 ASP.NET Core MVC 與 SQL Server 建構飲食與運動紀錄網站，練習前後端 MVC 分層、資料庫 CRUD 與圖表呈現。依原始程式碼可確認的功能如下：

- 登入頁面與示範性 Session 登入流程（**硬編碼測試帳密，不適用正式網站**）
- 飲食紀錄：新增、列表、文字查詢、編輯、刪除與可見紀錄熱量加總
- 運動紀錄：新增、列表、文字查詢、編輯、刪除
- 以 Chart.js 顯示運動消耗熱量折線圖

## 技術

- C#、.NET 8、ASP.NET Core MVC、Razor Views
- Entity Framework Core、SQL Server
- HTML、CSS、Bootstrap、JavaScript、Chart.js

## 程式架構

```
MVC_Homework/
  Controllers/             MVC 控制器（登入、運動與飲食紀錄）
  Models/                  資料模型與 EF Core DbContext
  Views/                   Razor 檢視與表單
  wwwroot/                 靜態資源
  Program.cs               服務、路由與資料庫設定
  MVC_Homework.csproj
MVC_Homework.sln
```

## 在個人電腦上執行（開發用途）

1. 需安裝 **.NET 8 SDK** 與可使用的 SQL Server 資料庫。
2. 進入 `MVC_Homework/` 目錄（含 `.csproj` 的資料夾）。
3. 使用 .NET Secret Manager 保存**自己的測試資料庫連線字串**，不要寫進 Git：

```bash
dotnet user-secrets init
dotnet user-secrets set "ConnectionStrings:DefaultConnection" "Server=YOUR_SERVER;Database=YOUR_DB;User Id=YOUR_USER;Password=YOUR_PASSWORD;TrustServerCertificate=True;"
dotnet restore
dotnet run
```

4. 原始碼映射到兩個特定資料表 `TableMealRecords1132024`、`TableExerciseRecords1132024`；此整理包**不含建表 SQL、測試資料或資料庫備份**，請在個人的測試資料庫建立符合模型的資料表後再測試。
5. `appsettings.example.json` 為不含憑證的設定檔範例，可視需要複製成 `appsettings.json`；勿將真實密碼提交至 Git。

## 已知限制與待改善事項

- 登入功能使用硬編碼測試帳密，且部分控制器雖定義登入檢查，實際 CRUD Action 未套用授權檢查；**不應公開部署使用**。
- 刪除採 GET 操作，應改為 POST/DELETE 並加上防 CSRF 機制。
- 資料庫連線憑證已從本整理包移除；原始 ZIP 曾含有效格式的憑證，應請管理者更換密碼。
- 目前僅完成靜態原始碼審閱；**尚未在乾淨環境執行整合測試**。
- 資料表名稱仍含課程辨識代號，公開展示前可評估去識別化（需同步調整資料庫資料表）。

## 應徵實習時可以介紹什麼？

說明如何將資料庫紀錄透過 EF Core 讀取到 MVC Controller，再使用 Razor View 呈現清單與圖表。可展示：`
Controllers/MealRecordsController.cs`、`Controllers/ExerciseRecordsController.cs` 與 `Views/ExerciseRecords/Index.cshtml`。

> 註：專案具體除錯歷程與修復步驟須由原作者確認，不應由原始碼推測為已實際發生。
