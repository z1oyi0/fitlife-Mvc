using Microsoft.AspNetCore.Mvc;
using MVC_Homework.Models;
using System.Linq;

namespace MVC_Homework.Controllers
{
    public class MealRecordsController : Controller
    {
        private readonly FitLifeDbContext _context;
        private bool IsLogin()
        {
            return HttpContext.Session.GetString("User") != null;
        }
        public MealRecordsController(FitLifeDbContext context)
        {
            _context = context;
        }

        public IActionResult Index(string searchText,int? pageNumber)
        {
            var result = _context.MealRecords.AsQueryable();


            if (!string.IsNullOrEmpty(searchText))
            {
                result = result.Where(x =>
                    (x.MealName != null && x.MealName.Contains(searchText)) ||
                    (x.MealType != null && x.MealType.Contains(searchText)) ||
                    (x.Note != null && x.Note.Contains(searchText))
                );
            }
            int pageSize = 5;
            int page = pageNumber ?? 1;

            var data = result
                .Skip((page - 1) * pageSize)
                .Take(pageSize)
                .ToList();

            ViewBag.SearchText = searchText;
            ViewBag.Page = page;

         
            return View(data);
        }

        public IActionResult Create()
        {
            return View();
        }

        [HttpPost]
        public IActionResult Create(MealRecord record)
        {
            _context.MealRecords.Add(record);
            _context.SaveChanges();

            return RedirectToAction("Index");
        }

        public IActionResult Edit(int id)
        {
            var record = _context.MealRecords.Find(id);

            if (record == null)
            {
                return RedirectToAction("Index");
            }

            return View(record);
        }

        [HttpPost]
        public IActionResult Edit(MealRecord record)
        {
            _context.MealRecords.Update(record);
            _context.SaveChanges();

            return RedirectToAction("Index");
        }

        public IActionResult Delete(int id)
        {
            var record = _context.MealRecords.Find(id);

            if (record != null)
            {
                _context.MealRecords.Remove(record);
                _context.SaveChanges();
            }

            return RedirectToAction("Index");
        }
    }
}