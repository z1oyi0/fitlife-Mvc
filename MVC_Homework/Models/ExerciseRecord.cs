using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace MVC_Homework.Models;

[Table("TableExerciseRecords1132024")]
public class ExerciseRecord
{
    public int Id { get; set; }
    [Required(ErrorMessage = "請填寫運動名稱。"), StringLength(200)]
    public string? ExerciseName { get; set; }
    public DateTime? ExerciseDate { get; set; }
    [Range(0, int.MaxValue, ErrorMessage = "運動時間必須為非負整數。")]
    public int? Duration { get; set; }
    [Required(ErrorMessage = "請填寫熱量。")]
    [Range(0, int.MaxValue, ErrorMessage = "熱量必須為非負整數。")]
    public int? Calories { get; set; }
    [StringLength(2000)]
    public string? Note { get; set; }
}
