from django import forms
from .models import Candidate, CandidateSSN,Salary,SalaryUnit,Income,Deduction

class CandidateEntryForm(forms.ModelForm):
	class Meta:
		model = Candidate
		fields = ('Name','Major','LastDegree','GPA','DateofBirth','Sex','YearsExperirence','Skills')
		labels= {'LastDegree':'Last Degree','DateofBirth':'Date of Birth', 'YearsExperirence':'Years Experience'}
class CandidateSSNForm1(forms.ModelForm):
	class Meta:
		model = CandidateSSN
		fields = ('SSN',)
		labels= {'SSN':'Social Security Number',}

class CandidateSSNForm(CandidateSSNForm1):

    Name= forms.CharField()

    class Meta(CandidateSSNForm1.Meta):
        fields = CandidateSSNForm1.Meta.fields + ('Name',)
        labels= CandidateSSNForm1.Meta.labels.update({'Name':'Confirm the candidate name',})

class PayStubForm(forms.ModelForm):
	class Meta:
		model = Salary
		fields = ('EmployeeNumber','Month','Year')
		labels= {'EmployeeNumber':'Choose the employee',}
class IncomeForm(forms.ModelForm):
	class Meta:
		model = Income
		fields = ('amount','description')
class DeductionForm(forms.ModelForm):
	class Meta:
		model = Deduction
		fields = ('amount','description')






