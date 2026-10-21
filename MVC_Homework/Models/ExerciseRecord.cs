using System;
using System.ComponentModel.DataAnnotations.Schema;

namespace MVC_Homework.Models
{
    [Table("TableExerciseRecords1132024")]
    public class ExerciseRecord
    {
        public int Id { get; set; }
        public string? ExerciseName { get; set; }
        public DateTime? ExerciseDate { get; set; }
        public int? Duration { get; set; }
        public int? Calories { get; set; }
        public string? Note { get; set; }
    }
}