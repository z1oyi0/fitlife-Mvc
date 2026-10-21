using Microsoft.AspNetCore.Mvc;
using MVC_Homework.Models;
using System.ComponentModel.DataAnnotations.Schema;
using System.Linq;

namespace MVC_Homework.Controllers
{
    [Table("TableExerciseRecords1132024")]
    public class ExerciseRecordsController : Controller
    {
        private readonly FitLifeDbContext _context;
        private bool IsLogin()
        {
            return HttpContext.Session.GetString("User") != null;
        }
        public ExerciseRecordsController(FitLifeDbContext context)
        {
            _context = context;
        }

        public IActionResult Index(string searchText)
        {
            var result = _context.ExerciseRecords.AsQueryable();

            if (!string.IsNullOrEmpty(searchText))
            {
                result = result.Where(x =>
                    (x.ExerciseName != null && x.ExerciseName.Contains(searchText)) ||
                    (x.Note != null && x.Note.Contains(searchText))
                );
            }

            ViewBag.SearchText = searchText;

            return View(result.ToList());
        }

        public IActionResult Create()
        {
            return View();
        }

        [HttpPost]
        public IActionResult Create(ExerciseRecord record)
        {
            _context.ExerciseRecords.Add(record);
            _context.SaveChanges();

            return RedirectToAction("Index");
        }

        public IActionResult Edit(int id)
        {
            var record = _context.ExerciseRecords.Find(id);

            if (record == null)
            {
                return RedirectToAction("Index");
            }

            return View(record);
        }

        [HttpPost]
        public IActionResult Edit(ExerciseRecord record)
        {
            _context.ExerciseRecords.Update(record);
            _context.SaveChanges();

            return RedirectToAction("Index");
        }

        public IActionResult Delete(int id)
        {
            var record = _context.ExerciseRecords.Find(id);

            if (record != null)
            {
                _context.ExerciseRecords.Remove(record);
                _context.SaveChanges();
            }

            return RedirectToAction("Index");
        }
    }
}
