using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace MVC_Homework.Models;

[Table("TableMealRecords1132024")]
public class MealRecord
{
    public int Id { get; set; }
    [Required(ErrorMessage = "請填寫食物名稱。"), StringLength(200)]
    public string? MealName { get; set; }
    [RegularExpression("^(早餐|午餐|晚餐|點心|宵夜)$", ErrorMessage = "請選擇有效餐別。")]
    public string? MealType { get; set; }
    public DateTime? MealDate { get; set; }
    [Required(ErrorMessage = "請填寫熱量。")]
    [Range(0, int.MaxValue, ErrorMessage = "熱量必須為非負整數。")]
    public int? Calories { get; set; }
    [StringLength(2000)]
    public string? Note { get; set; }
}
