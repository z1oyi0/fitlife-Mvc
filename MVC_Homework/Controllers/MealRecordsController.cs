using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using MVC_Homework.Models;

namespace MVC_Homework.Controllers;

[Authorize]
public class MealRecordsController : Controller
{
    private readonly FitLifeDbContext _context;
    public MealRecordsController(FitLifeDbContext context) => _context = context;

    [HttpGet]
    public IActionResult Index(string? searchText, int? pageNumber)
    {
        if (!ModelState.IsValid) return BadRequest("頁碼必須為整數。");
        var result = _context.MealRecords.AsNoTracking().AsQueryable();
        if (!string.IsNullOrEmpty(searchText))
            result = result.Where(x => (x.MealName != null && x.MealName.Contains(searchText))
                || (x.MealType != null && x.MealType.Contains(searchText))
                || (x.Note != null && x.Note.Contains(searchText)));
        const int pageSize = 5;
        int totalPages = Math.Max(1, (int)Math.Ceiling(result.Count() / (double)pageSize));
        int page = Math.Clamp(pageNumber ?? 1, 1, totalPages);
        ViewBag.SearchText = searchText;
        ViewBag.Page = page;
        ViewBag.TotalPages = totalPages;
        // F03: stable ordering and bounded offset, including 0, negatives and huge page numbers.
        return View(result.OrderBy(x => x.Id).Skip((page - 1) * pageSize).Take(pageSize).ToList());
    }

    [HttpGet]
    public IActionResult Create() => View(new MealRecord());

    [HttpPost]
    public IActionResult Create([Bind("MealName,MealType,MealDate,Calories,Note")] MealRecord record)
    {
        if (!ModelState.IsValid) { Response.StatusCode = 400; return View(record); }
        _context.MealRecords.Add(record);
        _context.SaveChanges();
        return RedirectToAction(nameof(Index));
    }

    [HttpGet]
    public IActionResult Edit(int id)
    {
        var record = _context.MealRecords.Find(id);
        return record == null ? NotFound() : View(record);
    }

    [HttpPost]
    public IActionResult Edit([FromRoute] int id, [Bind("Id,MealName,MealType,MealDate,Calories,Note")] MealRecord input)
    {
        if (id != input.Id) return BadRequest("紀錄編號不一致。");
        var record = _context.MealRecords.Find(id);
        if (record == null) return NotFound();
        if (!ModelState.IsValid) { Response.StatusCode = 400; return View(input); }
        record.MealName = input.MealName;
        record.MealType = input.MealType;
        record.MealDate = input.MealDate;
        record.Calories = input.Calories;
        record.Note = input.Note;
        _context.SaveChanges();
        return RedirectToAction(nameof(Index));
    }

    [HttpPost]
    public IActionResult Delete(int id)
    {
        var record = _context.MealRecords.Find(id);
        if (record == null) return NotFound();
        _context.MealRecords.Remove(record);
        _context.SaveChanges();
        return RedirectToAction(nameof(Index));
    }
}
