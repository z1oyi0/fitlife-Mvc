-- Isolated CI database only. This is reconstructed from the C# models,
-- not an export of the original school database. Never run on production.
SET NOCOUNT ON;
IF DB_ID(N'FitLifeVerification') IS NULL
    CREATE DATABASE FitLifeVerification;
GO
USE FitLifeVerification;
GO
IF DB_NAME() <> N'FitLifeVerification' THROW 50001, 'Unexpected database', 1;
CREATE TABLE dbo.TableMealRecords1132024 (
    Id int IDENTITY(1,1) NOT NULL PRIMARY KEY,
    MealName nvarchar(max) NULL,
    MealType nvarchar(max) NULL,
    MealDate datetime2 NULL,
    Calories int NULL,
    Note nvarchar(max) NULL
);
CREATE TABLE dbo.TableExerciseRecords1132024 (
    Id int IDENTITY(1,1) NOT NULL PRIMARY KEY,
    ExerciseName nvarchar(max) NULL,
    ExerciseDate datetime2 NULL,
    Duration int NULL,
    Calories int NULL,
    Note nvarchar(max) NULL
);
GO
