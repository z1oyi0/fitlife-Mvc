using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using MVC_Homework.Models;

namespace MVC_Homework.Controllers;

[Authorize]
public class ExerciseRecordsController : Controller
{
    private readonly FitLifeDbContext _context;
    public ExerciseRecordsController(FitLifeDbContext context) => _context = context;

    [HttpGet]
    public IActionResult Index(string? searchText)
    {
        var result = _context.ExerciseRecords.AsNoTracking().AsQueryable();
        if (!string.IsNullOrEmpty(searchText))
            result = result.Where(x => (x.ExerciseName != null && x.ExerciseName.Contains(searchText))
                || (x.Note != null && x.Note.Contains(searchText)));
        ViewBag.SearchText = searchText;
        return View(result.OrderBy(x => x.Id).ToList());
    }

    [HttpGet]
    public IActionResult Create() => View(new ExerciseRecord());

    [HttpPost]
    public IActionResult Create([Bind("ExerciseName,ExerciseDate,Duration,Calories,Note")] ExerciseRecord record)
    {
        if (!ModelState.IsValid) { Response.StatusCode = 400; return View(record); }
        _context.ExerciseRecords.Add(record);
        _context.SaveChanges();
        return RedirectToAction(nameof(Index));
    }

    [HttpGet]
    public IActionResult Edit(int id)
    {
        var record = _context.ExerciseRecords.Find(id);
        return record == null ? NotFound() : View(record);
    }

    [HttpPost]
    public IActionResult Edit([FromRoute] int id, [Bind("Id,ExerciseName,ExerciseDate,Duration,Calories,Note")] ExerciseRecord input)
    {
        if (id != input.Id) return BadRequest("紀錄編號不一致。");
        var record = _context.ExerciseRecords.Find(id);
        if (record == null) return NotFound();
        if (!ModelState.IsValid) { Response.StatusCode = 400; return View(input); }
        record.ExerciseName = input.ExerciseName;
        record.ExerciseDate = input.ExerciseDate;
        record.Duration = input.Duration;
        record.Calories = input.Calories;
        record.Note = input.Note;
        _context.SaveChanges();
        return RedirectToAction(nameof(Index));
    }

    [HttpPost]
    public IActionResult Delete(int id)
    {
        var record = _context.ExerciseRecords.Find(id);
        if (record == null) return NotFound();
        _context.ExerciseRecords.Remove(record);
        _context.SaveChanges();
        return RedirectToAction(nameof(Index));
    }
}
