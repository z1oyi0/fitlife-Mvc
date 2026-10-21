using System.Security.Claims;
using System.Security.Cryptography;
using System.Text;
using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Authentication.Cookies;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace MVC_Homework.Controllers;

// Development-only, single-account demonstration. Not a production identity system.
public class LoginController : Controller
{
    private readonly IConfiguration _configuration;
    private readonly IWebHostEnvironment _environment;
    public LoginController(IConfiguration configuration, IWebHostEnvironment environment)
    {
        _configuration = configuration;
        _environment = environment;
    }

    [AllowAnonymous, HttpGet]
    public IActionResult Index(string? returnUrl = null)
    {
        ViewBag.ReturnUrl = Url.IsLocalUrl(returnUrl) ? returnUrl : null;
        return View();
    }

    [AllowAnonymous, HttpPost]
    public async Task<IActionResult> Index(string? username, string? password, string? returnUrl = null)
    {
        ViewBag.ReturnUrl = Url.IsLocalUrl(returnUrl) ? returnUrl : null;
        string? expectedUser = _configuration["DemoAuth:Username"];
        string? expectedPassword = _configuration["DemoAuth:Password"];
        // Never fall back to the former hardcoded credentials.
        if (!_environment.IsDevelopment() || string.IsNullOrWhiteSpace(expectedUser)
            || string.IsNullOrEmpty(expectedPassword) || expectedPassword.Length < 12)
        {
            Response.StatusCode = StatusCodes.Status503ServiceUnavailable;
            ViewBag.Error = "本機示範登入尚未設定，或目前不是開發環境。";
            return View();
        }
        if (string.IsNullOrEmpty(username) || string.IsNullOrEmpty(password)
            || !FixedEquals(username, expectedUser) || !FixedEquals(password, expectedPassword))
        {
            ViewBag.Error = "帳號或密碼錯誤";
            return View();
        }
        var claims = new[] { new Claim(ClaimTypes.NameIdentifier, expectedUser), new Claim(ClaimTypes.Name, expectedUser) };
        var principal = new ClaimsPrincipal(new ClaimsIdentity(claims, CookieAuthenticationDefaults.AuthenticationScheme));
        await HttpContext.SignInAsync(CookieAuthenticationDefaults.AuthenticationScheme, principal,
            new AuthenticationProperties { IsPersistent = false });
        return Url.IsLocalUrl(returnUrl) ? LocalRedirect(returnUrl!) : RedirectToAction("Index", "Home");
    }

    [Authorize, HttpPost]
    public async Task<IActionResult> Logout()
    {
        await HttpContext.SignOutAsync(CookieAuthenticationDefaults.AuthenticationScheme);
        return RedirectToAction(nameof(Index));
    }

    private static bool FixedEquals(string value, string expected) =>
        CryptographicOperations.FixedTimeEquals(SHA256.HashData(Encoding.UTF8.GetBytes(value)),
            SHA256.HashData(Encoding.UTF8.GetBytes(expected)));
}
