using Microsoft.EntityFrameworkCore;

namespace MVC_Homework.Models
{
    public class FitLifeDbContext : DbContext
    {
        public FitLifeDbContext(DbContextOptions<FitLifeDbContext> options)
            : base(options)
        {
        }

        public DbSet<ExerciseRecord> ExerciseRecords { get; set; }
        public DbSet<MealRecord> MealRecords { get; set; }
    }
}