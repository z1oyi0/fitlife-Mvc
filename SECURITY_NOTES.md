# 公開前安全檢查

這個版本僅為 **去除資料庫帳密的程式碼整理包**，不是已通過安全審核的可部署網站。

- [ ] 更換原始 ZIP 曾包含的 SQL Server 帳號密碼（即使原檔從 Git 移除也要輪換）
- [ ] 不上傳 `appsettings.json`、`appsettings.Development.json`、`.vs`、`bin`、`obj`
- [ ] 改用 ASP.NET Core Identity 或其他正式驗證方案，替換硬編碼示範帳密
- [ ] 為資料頁面的 CRUD Action 加入授權檢查
- [ ] 移除 GET 刪除行為，加入 POST 與防 CSRF 驗證
- [ ] 重新確認公開時是否會暴露學號、教師或其他私人資訊
- [ ] 請自己啟動與測試程式，README 不能當作已完成運行測試的證據
