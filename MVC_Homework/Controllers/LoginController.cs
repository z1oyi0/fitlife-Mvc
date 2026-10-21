using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Http;

namespace MVC_Homework.Controllers
{
    public class LoginController : Controller
    {
        public IActionResult Index()
        {
            return View();
        }

        [HttpPost]
        public IActionResult Index(string username, string password)
        {
            if (username == "admin" && password == "1234")
            {
                HttpContext.Session.SetString("User", username);
                return RedirectToAction("Index", "Home");
            }

            ViewBag.Error = "帳號或密碼錯誤";
            return View();
        }

        public IActionResult Logout()
        {
            HttpContext.Session.Clear();
            return RedirectToAction("Index");
        }
    }
}
