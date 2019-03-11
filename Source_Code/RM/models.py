from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator,MinLengthValidator,MaxLengthValidator
# Create your models here.

class Department(models.Model):
    DepartmentNo = models.IntegerField(primary_key=True, unique= True, null=False)
    DepartmentName_Choices=(
    ('Marketing', 'Marketing'),
    ('HR Management', 'HR Management'),
    ('Production/Engineering', 'Production/Engineering'))

    DepartmentName = models.CharField(
        max_length=50,
        choices=DepartmentName_Choices,
        default="Marketing"
    )

class Candidate(models.Model):
    CandidateID = models.AutoField(primary_key=True, unique= True, null=False)
    Name= models.CharField(max_length=100)
    Major= models.CharField(max_length=50)
    LastDegree_choices= (
    ('Ph.D.', 'Ph.D.'),
    ('Master', 'Master'),
    ('BS', 'BS'))
    LastDegree = models.CharField(
        max_length=20,
        choices=LastDegree_choices,
        default="BS"
    )
	 # minimum for GPA is 0.00 and maximum is 4.00
    GPA= models.FloatField(validators=[
            MinValueValidator(0.00),
            MaxValueValidator(4.00),
        ])
    DateofBirth = models.DateField(auto_now=False, auto_now_add=False)
    Sex_choices= (
    ('Male', 'Male'),
    ('Female', 'Female'))
    Sex = models.CharField(
        max_length=10,
        choices=Sex_choices,
        default="Male"
    )
    YearsExperirence = models.IntegerField(default=0)
    Skills= models.CharField(max_length=200,default="none")
    IsHired= models.BooleanField(default=False)
	
class CandidateSSN(models.Model):
    SSNID = models.AutoField(primary_key=True, unique= True, null=False)
 	 #SSN should be exactly 9 digits
    SSN= models.IntegerField()
    CandidateID=models.ForeignKey('Candidate',on_delete=models.CASCADE)

class AcceptedCandidate(models.Model):
    AccCandidateID = models.AutoField(primary_key=True, unique= True, null=False)
    Assigned= models.BooleanField(default=False)
    SSNID= models.ForeignKey('CandidateSSN',on_delete=models.CASCADE)
    CandidateID=models.ForeignKey('Candidate',on_delete=models.CASCADE)

class Employee(models.Model):
    EmployeeNumber = models.AutoField(primary_key=True, unique= True, null=False)
    Name= models.CharField(max_length=100)
	#if a Department is deleted, the Employees' DepartmentNo would be set to null
    DepartmentNo= models.ForeignKey('Department',on_delete=models.SET_NULL,null=True)
    HiringDate = models.DateField(auto_now=True, auto_now_add=False)
    DateofBirth = models.DateField(auto_now=False, auto_now_add=False)
    Sex_choices= (
    ('Male', 'Male'),
    ('Female', 'Female'))
    Sex = models.CharField(
        max_length=10,
        choices=Sex_choices,
        default="Male"
    )
    AccCandidateID= models.ForeignKey('AcceptedCandidate',on_delete=models.SET_NULL,null=True)
	#ManagerID is a recursive foreign Key.
    ManagerID= models.ForeignKey('self',on_delete=models.SET_NULL,null=True)
    def __str__(self):
        return self.Name
	
class Salary(models.Model):
    SalaryId = models.AutoField(primary_key=True, unique= True, null=False)
    EmployeeNumber = models.ForeignKey('Employee',on_delete=models.CASCADE)
    Month = models.IntegerField(validators=[
            MinValueValidator(1),
            MaxValueValidator(12),
        ])
    Year = models.IntegerField(validators=[
            MinValueValidator(1950),
            MaxValueValidator(2100),
        ])

class SalaryUnit(models.Model):
	SalaryUId = models.AutoField(primary_key=True, unique= True, null=False)
	SalaryId= models.ForeignKey('Salary',on_delete=models.CASCADE)
	IsItIncome= models.BooleanField(default=True)

class Income(models.Model):
	SalaryUId= models.ForeignKey('SalaryUnit',on_delete=models.CASCADE)
	amount= models.IntegerField()
	description= models.CharField(max_length=100)
	
class Deduction(models.Model):
	SalaryUId= models.ForeignKey('SalaryUnit',on_delete=models.CASCADE)
	amount= models.IntegerField()
	description= models.CharField(max_length=100)
	
	
	
	
	