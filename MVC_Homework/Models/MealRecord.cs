using System;
using System.ComponentModel.DataAnnotations.Schema;

namespace MVC_Homework.Models
{
    [Table("TableMealRecords1132024")]
    public class MealRecord
    {
        public int Id { get; set; }
        public string? MealName { get; set; }
        public string? MealType { get; set; }
        public DateTime? MealDate { get; set; }
        public int? Calories { get; set; }
        public string? Note { get; set; }
    }
}

